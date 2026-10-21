"""Bangun index.html mandiri dari CSV dan source web. Tanpa paket tambahan."""
import csv
import json
import base64
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from peta import bangun_template_peta, muat_geojson, titik_wilayah
with (ROOT / 'data' / 'indikator_jatim.csv').open(encoding='utf-8-sig', newline='') as handle:
    rows = list(csv.DictReader(handle))
for row in rows:
    for key, value in row.items():
        if key != 'kabupaten_kota':
            row[key] = float(value) if '.' in value else int(value)
assert len(rows) == 38
assert len({(r['kabupaten_kota'], r['tahun']) for r in rows}) == len(rows)
html = (ROOT / 'scripts' / 'index.template.html').read_text(encoding='utf-8')
for marker, path in [('/* INLINE_CSS */','dashboard.css'), ('/* INLINE_ANALYTICS */','analytics.js'), ('/* INLINE_MAP_UI */','map.js'), ('/* INLINE_UI */','dashboard.js')]:
    html = html.replace(marker, (ROOT / 'scripts' / path).read_text(encoding='utf-8'))
html = html.replace('INLINE_DATA', json.dumps(rows, ensure_ascii=False).replace('</', '<\\/'))
geo = muat_geojson()
points = titik_wilayah(geo)
assert set(points) == {r['kabupaten_kota'] for r in rows}, 'Nama wilayah CSV dan GeoJSON tidak cocok'
def script_json(value):
    return json.dumps(value, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
html = html.replace('INLINE_MAP_TEMPLATE', script_json(bangun_template_peta(geo)))
html = html.replace('INLINE_MAP_POINTS', script_json(points))
logo = ROOT / 'assets' / 'duckdb-logo.svg'
if logo.exists():
    logo_uri = 'data:image/svg+xml;base64,' + base64.b64encode(logo.read_bytes()).decode('ascii')
    html = html.replace('INLINE_DUCKDB_LOGO_URI', logo_uri)
(ROOT / 'index.html').write_text(html, encoding='utf-8')
print('index.html dibuat: 38 wilayah, grafik dan peta interaktif dengan aset lokal disematkan.')
