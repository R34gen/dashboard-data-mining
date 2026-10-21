"""Uji integrasi Streamlit: python scripts/verify_streamlit.py."""
import json
import re
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def map_data(app):
    html = app.get("iframe")[0].proto.srcdoc
    return json.loads(re.search(r"const DATA = (.*);", html).group(1))


app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
assert not app.exception, list(app.exception)
assert [m.value for m in app.metric[:3]] == ["25.521", "294.886", "4.282.023"]
assert len(map_data(app)) == 38
app.radio(key="peta_indikator").set_value("Murid").run()
app.radio(key="peta_jenjang").set_value("SMA").run()
app.checkbox(key="peta_warna_ipm").check().run()
app.sidebar.multiselect[0].set_value(["Kota"]).run()
assert len(map_data(app)) == 9
app.sidebar.multiselect[1].set_value(["Kota Surabaya"]).run()
data = map_data(app)
assert len(data) == 1 and data[0]["nilai"] == 57135
details = dict(data[0]["rincian"])
assert details["Jenjang"] == "SMA"
assert details["Guru"] == "3.359" and details["Sekolah"] == "139"
assert not app.exception, list(app.exception)
app.sidebar.multiselect[0].set_value([]).run()
assert not app.exception, list(app.exception)
assert any("Tidak ada wilayah" in item.value for item in app.info)
print("PASS Streamlit: KPI, 38 wilayah, filter kota/SMA/murid, popup Surabaya, pewarnaan IPM, hasil kosong.")
