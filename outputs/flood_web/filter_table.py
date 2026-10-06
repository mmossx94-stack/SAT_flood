import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_js = "  const rows=allowed.map(p=>{const r=reports.find(x=>x.Province===p),v=DATA.vulnerable.find(x=>x.province===p);return {p,r,region:v?.region||'ไม่มีข้อมูล'}}).sort((a,b)=>{"

new_js = "  const rows=allowed.map(p=>{const r=reports.find(x=>x.Province===p),v=DATA.vulnerable.find(x=>x.province===p);return {p,r,region:v?.region||'ไม่มีข้อมูล'}}).filter(row => row.r && row.r.Current_Status === 'กำลังประสบภัย').sort((a,b)=>{"

if old_js in html:
    html = html.replace(old_js, new_js)
    print("Filtered table rows")
else:
    print("Could not find the row mapping JS")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
