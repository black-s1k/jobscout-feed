# Job Scout Setup Guide

Job Scout is a Google Sheet that finds new job postings for you. It checks employer career sites, Indeed, LinkedIn, Job Bank and more, keeps only jobs posted in the last 24 hours, and lists them in one place with a link to apply.

**What you need:** a Google account and a laptop. Setup takes about 15 minutes.

**Cost:** free. Nothing to install, and no coding.

**Get the script:** open **black-s1k.github.io/jobscout-feed** on your laptop and click **Copy the script**.

---

## Part 1: Create your sheet

1. Open a new browser tab and go to **sheets.new**. A blank Google Sheet opens.
2. Click **Untitled spreadsheet** at the top left and rename it **Job Scout**.

## Part 2: Add the script

1. In the sheet's menu, click **Extensions > Apps Script**. A new tab opens with a code editor.
2. Click **Untitled project** at the top left, type **Job Scout**, then click **Rename**.
3. Open **black-s1k.github.io/jobscout-feed** and click **Copy the script**.
4. Go back to the Apps Script tab and click inside the code area.
5. Select everything that is already there (**Cmd+A** or **Ctrl+A**), then paste (**Cmd+V** or **Ctrl+V**). The old code is replaced.
6. Save with **Cmd+S** or **Ctrl+S**. You should see "Saved to Drive".

**Important:** do not press the **Run** button in the editor. Everything is done from the sheet's own menu.

## Part 3: Turn it on

1. Go back to the tab with your sheet and reload the page (**Cmd+R** or **Ctrl+R**).
2. Wait about 15 seconds. A new menu called **Job Scout** appears next to **Help**.
3. The sheet builds its tabs by itself: **Jobs**, **Fresh 24h**, **Companies** and **Settings**.

If the tabs do not appear, click **Job Scout > Set up tabs**.

## Part 4: Tell it what you are looking for

Open the **Settings** tab. The yellow cells are the ones to fill in.

| Setting | What to choose |
|---|---|
| Your field | Pick your field from the dropdown. This fills in your keywords and adds 20 to 40 Canadian employers to the Companies tab. |
| Your subfield | Optional. Narrows your field, for example Finance > Accounting and audit. |
| Your level | Co-op / Internship, Entry level, and so on. You get jobs at your level and one level above. |
| Work style | In person or hybrid (default), remote within Canada, or anything. |
| Your province | Two letters, for example ON. |
| Locations | Places you would work, separated by commas. Default: Toronto, Ontario. Add Canada to accept jobs anywhere in Canada. |
| Exclude keywords | Optional. Words you never want in a job title, for example: senior, manager. |

You can change any of these at any time. The next refresh uses the new values.

## Part 5: Your first refresh

1. Click **Job Scout > Refresh jobs now**.
2. A box says **Authorization required**. Click **OK** and choose your Google account.
3. Google shows "Google hasn't verified this app". This is normal for a script you added yourself. Click **Advanced**, then **Go to Job Scout (unsafe)**.
4. Tick **Select all**, then click **Continue**.
5. Click **Job Scout > Refresh jobs now** again. The first click only gave permission.
6. Wait about a minute. New jobs appear in the **Jobs** tab, newest at the top.

**About the permissions:** the script only works inside this one sheet. It reads your Gmail only to look for job alert emails under one label (Part 7), and it sends you an email when new jobs arrive. You can read every line of the code under **Extensions > Apps Script**.

## Part 6: Read your results

**Tabs**

| Tab | What it shows |
|---|---|
| Jobs | Every job found, newest first. |
| Fresh 24h | Only jobs posted in the last 24 hours. |
| Companies | The employers whose career sites are checked directly. |
| Settings | Your choices, plus **Last refresh**, which shows what was checked and any problems. |

**Columns in the Jobs tab**

| Column | Meaning |
|---|---|
| Posted | When the employer posted the job. |
| Company, Title, Location | The job itself. |
| Source | Where it was found: an employer site, Indeed, LinkedIn, Job Bank and so on. |
| Link | Click to open the posting and apply. |
| Found | When your sheet found it. |
| Status | Use the dropdown to track it: New, Applied, Not interested. Closed is set for you when a job is taken down. |
| Notes | Anything you want to remember. |

## Part 7: Make it yours

**Add a dream company**

1. Go to the company's careers site and click on any one job posting.
2. Copy that page's link. Use a single job's link, not the careers home page.
3. In the **Companies** tab, add a new row: the company name in column A and the link in column B.
4. Click **Job Scout > Refresh jobs now**. The **Last check** column shows whether it worked.

**Add your job alert emails (optional)**

1. On LinkedIn or Indeed, create a job alert for your field and city, with email turned on.
2. When the first alert email arrives in Gmail, open it.
3. Click the three-dot menu at the top right of the email and choose **Filter messages like these**.
4. Click **Create filter**, tick **Apply the label**, choose **New label**, name it **job-alerts**, and click **Create filter**.
5. From now on, Job Scout reads those alerts on every refresh.

**Turn on autopilot**

Click **Job Scout > Turn auto-refresh ON**. The sheet then checks for new jobs every 15 minutes, even when your laptop is closed, and emails you when something new appears. Use **Turn auto-refresh OFF** to stop it.

**Optional free add-ons**

Each of these needs a free account. Paste the key into the matching row in **Settings**. Each row has a link to the page where you get the key.

| Add-on | What it adds |
|---|---|
| Apify | More LinkedIn results. Uses free monthly credit. |
| Firecrawl | Reads careers pages that the sheet cannot read on its own. |
| Adzuna | A job search covering every field. |

---

## Where the jobs come from

| Source | What it covers | Sign-up |
|---|---|---|
| Employer career sites | 80+ Canadian employers: banks, hospitals, retailers, utilities, universities, tech companies | None |
| Big employer feeds | Rogers, Bell, TELUS, Hydro One, OPG, Toronto Hydro, Canada Post, Purolator, Bombardier, University of Toronto, Halton Region | None |
| Amazon and Randstad Canada | Every Canadian Amazon job, and thousands of Randstad jobs | None |
| Indeed, LinkedIn and Job Bank | Collected every 30 minutes by the class scraper on GitHub, because these sites block Google's servers | None |
| LinkedIn public search | Searched directly with your field and level | None |
| Job alert emails | LinkedIn, Indeed and Glassdoor alerts in your Gmail | Your own alerts |
| Apify, Firecrawl, Adzuna | Optional extras | Free key |

## How the list stays clean

- **Fresh only:** a job is added only if it was posted in the last 24 hours, based on the real posting date.
- **No duplicates:** the same job found on several sites is added once.
- **Closed jobs:** if an employer takes a job down, its row is marked Closed.
- **Cleanup:** rows older than 14 days are deleted, unless their Status is Applied.
- **No flooding:** at most 10 new jobs per company per refresh. The rest arrive on later refreshes.
- **Right level:** senior, manager, director and executive roles are dropped unless you choose that level.

---

## Troubleshooting

| Problem | What to do |
|---|---|
| No Job Scout menu | Make sure you saved the script (Cmd+S or Ctrl+S), then reload the sheet and wait 15 seconds. |
| The menu is there but nothing happens | That click was the permission step. Click the menu item again. |
| "Syntax error" message | The paste was incomplete. In Apps Script, select all, paste the script again, save, and reload the sheet. |
| You pressed Run in the editor | No harm done. Go back to the sheet and use the Job Scout menu. |
| "Authorization required" keeps coming back | Go through the permission steps again and make sure you tick Select all. |
| 0 new jobs | Open Settings and read **Last refresh**. Try changing Max job age to 48, or remove some Exclude keywords. |
| A company row says "not found" | You pasted the careers home page. Open one job and paste that job's link instead. |
| A company row says "needs a Firecrawl key" | That site uses a system the sheet cannot read. Add a free Firecrawl key, or choose another company. |
| Jobs from the wrong city | Check **Locations** in Settings. Remove Canada if it is there. |
| Too many emails | Click **Job Scout > Turn auto-refresh OFF**, or set **Email me new jobs** to no. |

## Good to know

- Job Scout finds jobs. You still read each posting, tailor your resume and apply yourself.
- The class job feed searches around Toronto. If you are elsewhere, set your Locations and add job alerts for your city.
- Your sheet is private to you, and your keys stay in your own Settings tab.
