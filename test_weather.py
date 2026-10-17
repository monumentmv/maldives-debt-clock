import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch

import requests
import fetch_weather as weather


class WeatherTests(unittest.TestCase):
    def report(self, raw):
        return {'icaoId': 'VRMM', 'rawOb': raw, 'obsTime': datetime.now(timezone.utc).timestamp()}

    def test_current_conditions_ignore_trends_and_vicinity(self):
        for raw in ('VRMM 171200Z 24012KT SCT020 TEMPO TSRA BKN010',
                    'VRMM 171200Z 24012KT VCTS SCT020'):
            with self.subTest(raw=raw):
                w = weather.metar([self.report(raw)])
                self.assertEqual((w['cloud'], w['rain'], w['thunder']), (2, 0, False))

    def test_weather_intensity(self):
        for raw, expected in [('CAVOK', (0, 0, False)), ('-RA BKN018', (3, 1, False)),
                              ('+TSRA OVC010', (4, 3, True))]:
            with self.subTest(raw=raw):
                w = weather.metar([self.report('VRMM 171200Z 24012KT ' + raw)])
                self.assertEqual((w['cloud'], w['rain'], w['thunder']), expected)

    def test_model_is_identified_and_converts_wind(self):
        w = weather.model({'current': {'time': '2026-10-17T12:00', 'weather_code': 95,
                                      'cloud_cover': 100, 'wind_speed_10m': 18.52}})
        self.assertEqual(w['wind_kt'], 10)
        self.assertEqual(w['rain'], 2)
        self.assertIn('model estimate', w['src'])

    def test_missing_clouds_rejected(self):
        with self.assertRaises(ValueError):
            weather.metar([self.report('VRMM 171200Z 24012KT 9999')])

    def test_unavailable_sources_preserve_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(weather, 'OUT', Path(tmp) / 'weather.json'):
            weather.OUT.write_text('existing')
            with patch.object(weather.requests, 'get', side_effect=requests.ConnectionError('offline')):
                with self.assertRaises(SystemExit):
                    weather.main()
            self.assertEqual(weather.OUT.read_text(), 'existing')

    def test_stale_airport_falls_back_to_fresh_model(self):
        old = self.report('VRMM 171200Z 24012KT CAVOK')
        old['obsTime'] = (datetime.now(timezone.utc) - timedelta(hours=3)).timestamp()
        model = {'current': {'time': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M'),
                            'weather_code': 61, 'cloud_cover': 90}}
        with tempfile.TemporaryDirectory() as tmp, patch.object(weather, 'OUT', Path(tmp) / 'weather.json'):
            responses = [Mock(json=Mock(return_value=[old])), Mock(json=Mock(return_value=model))]
            with patch.object(weather.requests, 'get', side_effect=responses):
                weather.main()
            self.assertIn('Open-Meteo', weather.OUT.read_text())


if __name__ == '__main__':
    unittest.main()
