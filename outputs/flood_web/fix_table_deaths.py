import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_td = '<td style="padding:8px 4px;text-align:right">${fmt(x.Casualties_Deaths)}</td>'
new_td = '<td style="padding:8px 4px;text-align:right">${x.Casualties_Deaths==null?"-":fmt(x.Casualties_Deaths)}</td>'

if old_td in html:
    html = html.replace(old_td, new_td)
    print("Updated Deaths column to show - instead of ไม่มีข้อมูล")
else:
    print("Could not find the deaths td")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
