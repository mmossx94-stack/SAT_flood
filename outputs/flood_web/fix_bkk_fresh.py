import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_code = "for(const name of districts)summaries.set(name,districtWaterSummary(rows.filter(r=>String(r.district_or_area??'').replace(/^เขต/,'').trim()===name)));"
new_code = "for(const name of districts)summaries.set(name,districtWaterSummary(rows.filter(r=>String(r.district_or_area??'').replace(/^เขต/,'').trim()===name&&quality(r)==='ภายใน 24 ชั่วโมง')));"

if old_code in html:
    html = html.replace(old_code, new_code)
    print("Replaced district summary logic")
else:
    print("Could not find old_code")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
