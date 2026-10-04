# Maldives National Debt Clock

A live estimate of Maldives public and publicly guaranteed debt, built from the
[MMA Statistics Database](https://database.mma.gov.mv).

## Files

- `index.html`: the debt clock
- `fuel.html`: monthly fuel imports, with crisis periods
- `methodology.html`: how every figure is calculated
- `about.html`: about and contact form (set `WEB3FORMS_KEY` near the bottom of the file)
- `assets/site.css`, `assets/site.js`: shared styles, header toggles and charts
- `population.json`: the citizen population estimate. Update it once a year when the
  Department of National Registration publishes a new year-end figure.
- `fetch_data.py`: downloads the latest figures from the MMA API into `data.json`
- `.github/workflows/update-data.yml`: runs that script every morning

The MMA API token lives only in the `MMA_TOKEN` repository secret.

## Run locally

```
export MMA_TOKEN="your-token"
pip install requests
python fetch_data.py
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
