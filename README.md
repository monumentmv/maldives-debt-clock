# Maldives National Debt Clock

A live estimate of Maldives public and publicly guaranteed debt, built from the
[MMA Statistics Database](https://database.mma.gov.mv).

## Files

- `index.html`: the debt clock
- `fuel.html`: monthly fuel imports, with crisis periods
- `budget.html`: weekly budget figures from the Ministry of Finance, with every year since 2019 to compare
- `revenue.html`: taxes, fees and rents collected by MIRA since 2010, and the part paid in US dollars
- `priorities.html`: interest costs set against spending on policing, justice and the offices that protect families, children and human rights, and other big services, with cases reported to the police
- `methodology.html`: how every figure is calculated
- `about.html`: about and contact form, which sends messages to a Google Form (see below)
- `assets/site.css`, `assets/site.js`: shared styles, header toggles and charts
- `population.json`: the citizen population estimate. Update `base` and `base_date` once a year when the
  Department of National Registration publishes a new year-end figure.
- `fetch_data.py`: downloads the latest figures from the MMA API into `data.json`
- `fetch_wfd.py`: checks the Ministry of Finance for new Weekly Fiscal Developments reports, reads them (with `wfd_extract.py`), adds them to `data/wfd/` and writes `budget.json`
- `wfd_extract.py`: reads the tables in a Weekly Fiscal Developments PDF. Also works on its own to download and extract every report to your computer
- `data/wfd/`: the weekly dataset, one row per report (`wfd_headline.csv`), every table row (`wfd_long.csv`), and which reports were read (`processed.csv`)
- `build_master.py`: combines MMA, MIRA, Ministry of Finance and police data into one clean dataset in `data/master/`, and builds the Excel and CSV downloads into `downloads/` whenever the data changes
- `fetch_police.py`: reads the Maldives Police Service crime statistics page every morning (with a headless browser) into `data/police/crime_monthly.csv`. If the page can't be read, the existing figures stay
- `build_priorities.py`: builds `priorities.json` for the priorities page from every weekly budget report since 2019 and the police figures
- `downloads/`: the Excel and CSV downloads linked from the data page
- `fetch_mira.py`: checks MIRA's website every morning and downloads new versions of its revenue files into `inputs/mira/`
- `build_revenue.py`: reads the MIRA spreadsheets in `inputs/mira/` and writes `revenue.json`
- `inputs/mira/`: MIRA's monthly revenue files, kept up to date by `fetch_mira.py`
- `.github/workflows/update-data.yml`: runs all the scripts every morning, and whenever a script or a file in `inputs/` changes

The MMA API token lives only in the `MMA_TOKEN` repository secret.

## Run locally

```
export MMA_TOKEN="your-token"
pip install requests openpyxl pdfplumber playwright
python -m playwright install chromium
python fetch_data.py
python build_revenue.py
python fetch_wfd.py
python fetch_police.py
python build_priorities.py
python build_master.py
python -m http.server
```
Then open http://localhost:8000

## Contact form (Google Form)

The form on `about.html` sends messages into a Google Form.

1. Create a Google Form with four **Short answer** questions (use **Paragraph** for the last one):
   Name, Email, Topic, Message. Leave "Collect email addresses" off and don't require sign-in.
2. In the form, open the **⋮** menu and choose **Get pre-filled link**.
   Type `NAME`, `EMAIL`, `TOPIC` and `MESSAGE` into the four boxes, click **Get link**, then **Copy link**.
3. In `about.html`, replace `PASTE-YOUR-GOOGLE-FORM-PREFILLED-LINK` with that link.
4. In the form's **Responses** tab, open **⋮** and turn on **Get email notifications for new responses**.

## What visitors can open

`functions/_middleware.js` serves only the files the site needs: the pages, `assets/`, the JSON files the
pages read, `data/master/`, `data/police/crime_monthly.csv` and `downloads/`. Everything else in the repo,
including the scripts, `inputs/`, `data/wfd/`, this README and the workflow, returns "Not found".
If you add a new page or data file, add it to the `PUBLIC` list in that file.

## After changing the shared files

Every page loads `assets/site.css` and `assets/site.js` with a version tag, for example `site.js?v=20261006b`.
Whenever you change either file, change the tag on every page (find and replace across the `.html` files),
so visitors never get a new page with an old script. `_headers` tells Cloudflare not to keep old copies for long.
