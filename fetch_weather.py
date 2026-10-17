"""Save fresh Hulhulé weather for the home-page sky. No credentials required."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests

OUT = Path(__file__).with_name('weather.json')
METAR = 'https://aviationweather.gov/api/data/metar?ids=VRMM&format=json&hours=3'
MODEL = ('https://api.open-meteo.com/v1/forecast?latitude=4.19&longitude=73.53'
         '&current=temperature_2m,weather_code,cloud_cover,wind_speed_10m&timezone=GMT')
MAX_AGE = 2 * 60 * 60
COVER = {'SKC': 0, 'CLR': 0, 'NSC': 0, 'NCD': 0, 'FEW': 1, 'SCT': 2, 'BKN': 3, 'OVC': 4, 'VV': 4}


def describe(cloud, rain, thunder):
    if thunder:
        return 'thunderstorm'
    return ['', 'light rain', 'rain', 'heavy rain'][rain] if rain else [
        'clear', 'mostly clear', 'partly cloudy', 'mostly cloudy', 'overcast'][cloud]


def metar(data):
    reports = [m for m in data if m.get('icaoId') == 'VRMM' and m.get('rawOb') and m.get('obsTime')]
    if not reports:
        raise ValueError('no dated VRMM report')
    m = max(reports, key=lambda m: m['obsTime'])
    raw = m['rawOb']
    # Ignore trends and forecasts after the current observation.
    current = re.split(r'\b(?:TEMPO|BECMG|NOSIG)\b', raw)[0]
    layers = re.findall(r'\b(FEW|SCT|BKN|OVC|VV)\d{3}', current)
    cloud = max((COVER[c] for c in layers), default=0)
    if not layers and not re.search(r'\b(?:CAVOK|SKC|CLR|NSC|NCD)\b', current):
        layers = [c.get('cover') for c in m.get('clouds') or []]
        known = [COVER[c] for c in layers if c in COVER]
        if not known:
            raise ValueError('unknown cloud conditions')
        cloud = max(known)
    rain, thunder = 0, False
    for token in current.split():
        if not re.fullmatch(r'[-+]?(?:[A-Z]{2})+', token) or token.startswith(('VC', 'RE')):
            continue
        thunder |= 'TS' in token
        if 'RA' in token or 'DZ' in token:
            rain = max(rain, 3 if token.startswith('+') else 1 if token.startswith('-') or 'DZ' in token else 2)
    if rain or thunder:
        cloud = max(cloud, 3)
    return dict(at=datetime.fromtimestamp(m['obsTime'], timezone.utc).isoformat(),
                src='Velana International Airport METAR (VRMM)', temp=m.get('temp'),
                wind_kt=m.get('wspd'), cloud=cloud, rain=rain, thunder=thunder,
                text=describe(cloud, rain, thunder), raw=raw)


def model(data):
    c = data['current']
    code, cover = c['weather_code'], c['cloud_cover']
    if not isinstance(code, (int, float)) or not isinstance(cover, (int, float)):
        raise ValueError('missing model conditions')
    rain = 3 if code in (65, 67, 82) else 2 if code in (63, 66, 81) else 1 if code in (51, 53, 55, 56, 57, 61, 80) else 0
    thunder = code in (95, 96, 99)
    cloud = 0 if cover < 15 else 1 if cover < 40 else 2 if cover < 70 else 3 if cover < 90 else 4
    if thunder:
        rain = max(rain, 2)
    if rain:
        cloud = max(cloud, 3)
    wind = c.get('wind_speed_10m')
    return dict(at=datetime.fromisoformat(c['time']).replace(tzinfo=timezone.utc).isoformat(),
                src='Open-Meteo model estimate at Hulhulé', temp=c.get('temperature_2m'),
                wind_kt=round(wind / 1.852) if isinstance(wind, (int, float)) else None,
                cloud=cloud, rain=rain, thunder=thunder, text=describe(cloud, rain, thunder))


def main():
    for url, parse in ((METAR, metar), (MODEL, model)):
        try:
            response = requests.get(url, timeout=30, headers={'User-Agent': 'mvdebtclock.org weather'})
            response.raise_for_status()
            weather = parse(response.json())
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(weather['at'])).total_seconds()
            if not -300 <= age <= MAX_AGE:
                raise ValueError('observation outside two-hour freshness window')
            pending = OUT.with_suffix('.json.tmp')
            pending.write_text(json.dumps(weather, ensure_ascii=False) + '\n', encoding='utf-8')
            pending.replace(OUT)
            print(f"Saved {weather['text']} from {weather['src']} at {weather['at']}")
            return
        except (requests.RequestException, ValueError, KeyError, TypeError) as error:
            print(f'Weather source unavailable: {error}')
    raise SystemExit('No fresh weather available; existing weather.json preserved.')


if __name__ == '__main__':
    main()
