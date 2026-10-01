"""Job Scout class feed.

Runs on GitHub Actions. For each field it searches the big job boards that block
Google's servers (Indeed, Glassdoor, Google Jobs, LinkedIn through JobSpy, plus
Government of Canada Job Bank) and writes feed/<field>.json. Every student's
Job Scout sheet reads the file for its field and applies its own filters.

Jobs are kept for 72 hours, merged across runs, so a run where a board blocks
us doesn't empty the feed.
"""
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from html import unescape
from pathlib import Path
from urllib.parse import quote_plus

import requests

LOCATION = "Toronto, ON"
PROVINCE = "ON"
KEEP_HOURS = 72
RESULTS_PER_SEARCH = {"indeed": 60, "linkedin": 30}
OUT = Path(__file__).parent / "feed"

# Same fields as the sheet's "Your field" dropdown. Searches are broad on purpose:
# each sheet filters by its own keywords, level and location afterwards.
FIELDS = {
    "tech": ["software developer", "data analyst", "IT support", "software engineer intern", "business intelligence", "cybersecurity", "QA tester"],
    "finance": ["accountant", "financial analyst", "bank", "accounting co-op", "bookkeeper", "payroll", "audit"],
    "health": ["registered nurse", "personal support worker", "pharmacy assistant", "medical office assistant", "lab technician", "dental assistant", "physiotherapy"],
    "business": ["marketing coordinator", "sales representative", "human resources", "administrative assistant", "customer service", "social media", "operations coordinator"],
    "eng": ["engineer", "engineering technician", "lab technician", "engineering co-op", "mechanical engineer", "civil engineer", "quality technician"],
    "edu": ["teacher", "program coordinator", "social worker", "research assistant", "early childhood educator", "tutor", "community support worker"],
    "any": ["co-op student", "summer student", "intern", "entry level", "student", "junior", "assistant"],
}
# Glassdoor, Google Jobs and ZipRecruiter fail inside JobSpy for Canada (checked Oct 1 2026).
JOBSPY_SITES = ["indeed", "linkedin"]
SITE_LABEL = {"indeed": "Indeed", "linkedin": "LinkedIn", "glassdoor": "Glassdoor", "google": "Google Jobs", "zip_recruiter": "ZipRecruiter"}
PROVINCES = {"ON": "Ontario", "BC": "British Columbia", "AB": "Alberta", "QC": "Quebec", "MB": "Manitoba", "SK": "Saskatchewan",
             "NS": "Nova Scotia", "NB": "New Brunswick", "NL": "Newfoundland and Labrador", "PE": "Prince Edward Island"}


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def clean(s):
    s = "" if s is None else str(s)
    return "" if s.lower() in ("nan", "none", "nat") else re.sub(r"\s+", " ", unescape(s)).strip()


def jobspy_search(site, term):
    from jobspy import scrape_jobs
    df = scrape_jobs(
        site_name=[site],
        search_term=term,
        google_search_term=f"{term} jobs near {LOCATION} since yesterday",
        location=LOCATION,
        distance=50,
        results_wanted=RESULTS_PER_SEARCH[site],
        hours_old=48,
        country_indeed="Canada",
        verbose=0,
    )
    jobs = []
    for r in df.to_dict("records"):
        posted = r.get("date_posted")
        posted = posted.isoformat() if hasattr(posted, "isoformat") else clean(posted)
        if not posted:
            continue  # no date, can't tell fresh from stale
        loc = ", ".join(p for p in (clean(r.get("city")), clean(r.get("state"))) if p) or clean(r.get("location"))
        if r.get("is_remote") is True and "remote" not in loc.lower():
            loc = f"{loc} (remote)".strip()
        jobs.append({
            "title": clean(r.get("title")),
            "company": clean(r.get("company")),
            "location": loc,
            "posted": posted,
            "link": clean(r.get("job_url_direct")) if site == "google" and clean(r.get("job_url_direct")) else clean(r.get("job_url")),
            "source": SITE_LABEL.get(site, site),
        })
    return jobs


def jobbank_search(term):
    url = ("https://www.jobbank.gc.ca/jobsearch/feed/jobSearchRSSfeed?sort=D&searchstring="
           + quote_plus(term) + f"&fprov={PROVINCE}")
    r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0 (JobScout class feed)"})
    r.raise_for_status()
    jobs = []
    for e in r.text.split("<entry>")[1:]:
        pick = lambda pat: (re.search(pat, e, re.S) or [None, ""])[1].strip()
        title = clean(pick(r"<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>"))
        where = clean(pick(r"Location:</strong>\s*([^<]+)<"))
        where = re.sub(r"\s*\((\w\w)\)", lambda m: f", {PROVINCES.get(m.group(1), m.group(1))};", where).rstrip("; ").replace(";", " ·")
        link = pick(r'<link[^>]*href="([^"]+)"')
        if title and link:
            jobs.append({
                "title": title[:1].upper() + title[1:],
                "company": clean(pick(r"Employer:</strong>\s*([^<]+)<")),
                "location": f"{where}, Canada" if where else "Canada",
                "posted": pick(r"<updated>([^<]+)</updated>"),
                "link": link,
                "source": "Job Bank",
            })
    return jobs


def posted_time(p):
    """Datetime for a posted value; date-only values count as noon that day."""
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p):
            return datetime.fromisoformat(p).replace(hour=12, tzinfo=timezone(timedelta(hours=-4)))
        d = datetime.fromisoformat(p.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def run_field(field, terms):
    found, stats = [], {}
    for term in terms:
        for site in JOBSPY_SITES:
            try:
                jobs = jobspy_search(site, term)
            except Exception as e:  # one blocked board shouldn't stop the rest
                log(f"  {field} · {site} · {term}: {type(e).__name__}: {str(e)[:120]}")
                jobs = []
            stats[SITE_LABEL[site]] = stats.get(SITE_LABEL[site], 0) + len(jobs)
            found += jobs
            time.sleep(1)
        try:
            jobs = jobbank_search(term)
        except Exception as e:
            log(f"  {field} · jobbank · {term}: {type(e).__name__}: {str(e)[:120]}")
            jobs = []
        stats["Job Bank"] = stats.get("Job Bank", 0) + len(jobs)
        found += jobs
    return field, found, stats


def merge(field, fresh):
    path = OUT / f"{field}.json"
    old = json.loads(path.read_text())["jobs"] if path.exists() else []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=KEEP_HOURS)
    by_link = {}
    for j in old + fresh:  # newer runs win
        t = posted_time(j.get("posted", ""))
        if j.get("link") and j.get("title") and t and t >= cutoff:
            by_link[j["link"]] = j
    jobs = sorted(by_link.values(), key=lambda j: posted_time(j["posted"]), reverse=True)
    return jobs


def main():
    only = sys.argv[1:] or list(FIELDS)
    OUT.mkdir(exist_ok=True)
    started = datetime.now(timezone.utc)
    status = {"updated": started.isoformat(timespec="seconds"), "fields": {}}
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda f: run_field(f, FIELDS[f]), only))
    for field, fresh, stats in results:
        jobs = merge(field, fresh)
        (OUT / f"{field}.json").write_text(json.dumps({"updated": status["updated"], "jobs": jobs}, ensure_ascii=False, indent=0))
        status["fields"][field] = {"found_this_run": stats, "in_feed": len(jobs)}
        log(f"{field}: {sum(stats.values())} found this run {stats} · {len(jobs)} in feed")
    status["seconds"] = round((datetime.now(timezone.utc) - started).total_seconds())
    (OUT / "status.json").write_text(json.dumps(status, indent=1))


if __name__ == "__main__":
    main()
