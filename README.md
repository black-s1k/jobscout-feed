# Job Scout class feed

**Students:** get the script at **[black-s1k.github.io/jobscout-feed](https://black-s1k.github.io/jobscout-feed/)** and follow the **[setup guide](https://black-s1k.github.io/jobscout-feed/guide.html)** (also in [SETUP.md](SETUP.md)).

<img src="qr.png" alt="QR code for the script page" width="140">

Fresh job postings for the Job Scout Google Sheet, refreshed every 30 minutes by GitHub Actions.

Google's servers are blocked by Indeed and Job Bank, so this repo collects them instead and publishes one file per field. Every Job Scout sheet reads the file for its field and applies its own filters for level, work style, location and freshness.

| File | Field in the sheet |
|---|---|
| `feed/tech.json` | Tech & Data |
| `feed/finance.json` | Finance & Accounting |
| `feed/health.json` | Healthcare & Nursing |
| `feed/business.json` | Business & Marketing |
| `feed/eng.json` | Engineering & Science |
| `feed/edu.json` | Education, Government & Non-profit |
| `feed/any.json` | Any field |

`feed/status.json` shows when the feed last updated and how many jobs each board returned.

**Sources:** Indeed Canada and LinkedIn (through [JobSpy](https://github.com/speedyapply/JobSpy)), and Government of Canada Job Bank. Searches are around Toronto, ON (80 km), posted in the last 48 hours. Jobs stay in the feed for 72 hours.

**Free:** public repos get unlimited GitHub Actions minutes. If GitHub pauses the schedule after 60 days without activity, open the **Actions** tab and turn the workflow back on.

**Run it yourself:** `pip install -r requirements.txt`, then `python feed.py` (or `python feed.py tech` for one field).
