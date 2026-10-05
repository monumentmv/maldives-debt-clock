# Maldives National Debt Clock

A live estimate of Maldives public and publicly guaranteed debt, built from the
[MMA Statistics Database](https://database.mma.gov.mv).

## Files

- `index.html`: the debt clock
- `fuel.html`: monthly fuel imports, with crisis periods
- `budget.html`: weekly budget figures from the Ministry of Finance, with every year since 2019 to compare
- `revenue.html`: taxes, fees and rents collected by MIRA since 2010, and the part paid in US dollars
- `methodology.html`: how every figure is calculated
- `about.html`: about and contact form (set `WEB3FORMS_KEY` near the bottom of the file)
- `assets/site.css`, `assets/site.js`: shared styles, header toggles and charts
- `population.json`: the citizen population estimate. Update it once a year when the
  Department of National Registration publishes a new year-end figure.
- `fetch_data.py`: downloads the latest figures from the MMA API into `data.json`
- `fetch_wfd.py`: checks the Ministry of Finance for new Weekly Fiscal Developments reports, reads them (with `wfd_extract.py`), adds them to `data/wfd/` and writes `budget.json`
- `wfd_extract.py`: reads the tables in a Weekly Fiscal Developments PDF. Also works on its own to download and extract every report to your computer
- `data/wfd/`: the weekly dataset, one row per report (`wfd_headline.csv`), every table row (`wfd_long.csv`), and which reports were read (`processed.csv`)
- `data.html`: the data page, with downloads of everything in one Excel or CSV file
- `build_master.py`: combines MMA, MIRA and Ministry of Finance data into one clean dataset in `data/master/`, and builds the Excel and CSV downloads, published as the `data-latest` release
- `fetch_mira.py`: checks MIRA's website every morning and downloads new versions of its revenue files into `inputs/mira/`
- `build_revenue.py`: reads the MIRA spreadsheets in `inputs/mira/` and writes `revenue.json`
- `inputs/mira/`: MIRA's monthly revenue files, kept up to date by `fetch_mira.py`
- `.github/workflows/update-data.yml`: runs both scripts every morning, and whenever a file in `inputs/` changes

The MMA API token lives only in the `MMA_TOKEN` repository secret.

## Run locally

```
export MMA_TOKEN="your-token"
pip install requests openpyxl pdfplumber
python fetch_data.py
python build_revenue.py
python fetch_wfd.py
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
