# MIRA revenue files

MIRA's two monthly revenue spreadsheets, the total revenue collection and the USD revenue collection.

`fetch_mira.py` downloads them automatically every morning from MIRA's Revenue Series page
(https://www.mira.gov.mv/Publications/Categories/310) and replaces these copies when MIRA publishes
a new version. `build_revenue.py` then rebuilds `revenue.json`.

You can still upload a file here by hand if needed. Keep only one of each kind, or the update stops
with a message saying which file to remove.
