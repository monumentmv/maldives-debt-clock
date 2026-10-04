# Maldives Debt Clock

A live estimate of Maldives public and publicly guaranteed debt, built from the
[MMA Statistics Database](https://database.mma.gov.mv).

- `index.html` is the whole website (no build step).
- `fetch_data.py` pulls the latest figures from the MMA API and writes `data.json`.
- `.github/workflows/update-data.yml` runs that script every day and commits the result.

The API token lives only in a GitHub secret. It is never in the code or the website.

## Series used

| ID   | Series |
|------|--------|
| 4514 | Total outstanding public & publicly guaranteed debt (MVR) |
| 4515–4520 | Domestic / external, central government / guaranteed |
| 4522 | Total outstanding debt, % of GDP |
| 79   | Population |
| 4039 | MVR per US dollar |
| 5226 | Quarterly interest paid on central government external debt (USD) |

## How the clock ticks

Start from the latest quarterly total, then add debt at the average pace of the
last four quarters, per second. Each new official release resets it.

## Run locally

```
export MMA_TOKEN="your-token"
pip install requests
python fetch_data.py
python -m http.server
```
Then open http://localhost:8000
