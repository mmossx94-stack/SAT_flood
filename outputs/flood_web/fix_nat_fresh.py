import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_code = "for(const name of uniq(rows.map(r=>r.province).filter(Boolean)))summaries.set(name,districtWaterSummary(rows.filter(r=>r.province===name)));"
new_code = "for(const name of uniq(rows.map(r=>r.province).filter(Boolean)))summaries.set(name,districtWaterSummary(rows.filter(r=>r.province===name&&quality(r)==='ภายใน 24 ชั่วโมง')));"

if old_code in html:
    html = html.replace(old_code, new_code)
    print("Replaced national summary logic")
else:
    print("Could not find old_code")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
