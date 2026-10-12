// Draws the land outline once into assets/worldmap.json for the home page's lenders map.
// Equirectangular, so the page can place any point with simple arithmetic: x = tx + s*rad(lon - lon0), y = ty - s*rad(lat).
import fs from "fs";
import { geoEquirectangular, geoPath } from "d3-geo";
import { feature } from "topojson-client";
const W = 1000, lonMin = -112, lonMax = 162, latTop = 66, latBottom = -38;
const lon0 = (lonMin + lonMax) / 2, rad = d => d * Math.PI / 180;
const s = W / rad(lonMax - lonMin), tx = W / 2, ty = s * rad(latTop), H = Math.round(ty + s * rad(-latBottom));
const proj = geoEquirectangular().rotate([-lon0, 0]).scale(s).translate([tx, ty]).clipExtent([[0, 0], [W, H]]).precision(0.5);
const path = geoPath(proj);
const round = d => d.replace(/\d+\.\d+/g, m => (+m).toFixed(1));
const countries = feature(JSON.parse(fs.readFileSync("node_modules/world-atlas/countries-110m.json")), "countries");
const land = feature(JSON.parse(fs.readFileSync("node_modules/world-atlas/land-110m.json")), "land");
const WANT = ["China", "India", "Saudi Arabia", "United Arab Emirates", "Kuwait", "Japan", "France", "Belgium", "United States of America",
  "Germany", "Netherlands", "Oman", "Pakistan", "Maldives", "Italy", "Luxembourg", "Finland", "Austria", "Philippines", "Hungary", "Sri Lanka", "Denmark", "Switzerland"];
const out = { w: W, h: H, s, tx, ty, lon0, land: round(path(land)), countries: {} };
for (const f of countries.features) if (WANT.includes(f.properties.name)) { const d = path(f); if (d) out.countries[f.properties.name] = round(d); }
fs.writeFileSync(process.argv[2], JSON.stringify(out));
console.log("size", W, H, "KB", Math.round(JSON.stringify(out).length / 1024), "countries", Object.keys(out.countries).length);
