@echo off
REM Collects every month and year from the police website once, on this computer.
REM Afterwards, upload data\police\crime_monthly.csv to GitHub. From then on the daily update only adds new months.
python -m pip install playwright
python -m playwright install chromium
python fetch_police.py --all
python build_priorities.py
pause
