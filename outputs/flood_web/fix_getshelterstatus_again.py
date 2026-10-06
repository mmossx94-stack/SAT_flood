import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

func_def = "const getShelterStatus = r => { let s=String(r.status_source||'').trim(); return s==='เปิดให้บริการ/ว่าง'?'ว่าง':s==='ใกล้เต็ม'?'ใกล้เต็ม':s==='เต็ม'?'เต็ม':'ไม่ทราบ'; };\n"

if "function renderShelterMap(){" in html and "getShelterStatus = r =>" not in html:
    html = html.replace("function renderShelterMap(){", func_def + "function renderShelterMap(){")
    print("Injected function definition!")
else:
    print("Could not inject")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
