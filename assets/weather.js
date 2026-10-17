// The scene uses only fresh reports; failed refreshes never extend an observation's life.
window.MVWeather = (() => {
  const hero = document.getElementById('hero');
  const sky = document.getElementById('sky');
  const rain = document.createElement('div');
  rain.className = 'weather-rain';
  sky.appendChild(rain);
  for (let i = 0; i < 40; i++) {
    const drop = document.createElement('i');
    drop.style.left = `${(i * 17.3) % 100}%`;
    drop.style.animationDelay = `${-(i % 9) / 10}s`;
    rain.appendChild(drop);
  }
  const label = document.createElement('span');
  label.className = 'weather-label';
  label.hidden = true;
  hero.appendChild(label);
  let report = null;
  function current() {
    if (!report) return null;
    const age = Date.now() - Date.parse(report.at);
    return Number.isFinite(age) && age >= -300000 && age <= 7200000 ? report : null;
  }
  function render() {
    const w = current();
    hero.dataset.weatherCloud = w ? w.cloud : '';
    hero.dataset.weatherRain = w ? w.rain : '0';
    hero.dataset.weatherThunder = w ? String(w.thunder) : 'false';
    const wind = w && Number.isFinite(w.wind_kt) ? Math.max(0, Math.min(50, w.wind_kt)) : 0;
    hero.style.setProperty('--weather-cloud-speed', `${140 / (1 + wind / 12)}s`);
    hero.style.setProperty('--weather-wave-speed', `${14 / (1 + wind / 30)}s`);
    label.hidden = !w;
    if (w) {
      const time = new Date(w.at).toLocaleTimeString('en-GB', { timeZone: 'Indian/Maldives', hour: '2-digit', minute: '2-digit' });
      const estimated = w.src.startsWith('Open-Meteo') ? ' (estimated)' : '';
      label.textContent = `Hulhulé · ${Number.isFinite(w.temp) ? `${Math.round(w.temp)}°C · ` : ''}${w.text}${estimated} · ${time} MVT`;
      label.title = `${w.src}; updated ${w.at}`;
    }
    window.MVSky?.draw();
  }
  async function refresh() {
    try {
      const response = await fetch('weather.json', { cache: 'no-store', signal: AbortSignal.timeout(10000) });
      if (!response.ok) throw new Error('Weather unavailable');
      const w = await response.json();
      if (![0, 1, 2, 3, 4].includes(w.cloud) || ![0, 1, 2, 3].includes(w.rain) ||
          typeof w.thunder !== 'boolean' || typeof w.src !== 'string' || typeof w.text !== 'string') {
        throw new Error('Invalid weather');
      }
      report = w;
    } catch { /* A valid previous observation remains usable until it expires. */ }
    render();
  }
  setInterval(refresh, 5 * 60 * 1000);
  setInterval(render, 30000);
  refresh();
  return { current };
})();
