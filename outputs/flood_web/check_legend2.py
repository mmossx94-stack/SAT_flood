import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find('ล้นตลิ่ง')
while idx != -1:
    print("MATCH:", html[max(0, idx-100):min(len(html), idx+100)])
    idx = html.find('ล้นตลิ่ง', idx+1)
