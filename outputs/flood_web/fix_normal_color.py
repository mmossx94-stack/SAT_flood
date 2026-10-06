import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_status = "ปกติ:{rank:1,color:'transparent'}"
new_status = "ปกติ:{rank:1,color:'#22c55e'}"

if old_status in html:
    html = html.replace(old_status, new_status)
    print("Replaced ปกติ color to green")
else:
    print("Could not find ปกติ status")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
