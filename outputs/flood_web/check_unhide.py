import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('shelterMapPanel')
    if idx != -1:
        end = html.find(';', html.find("('shelterMapPanel')", idx))
        print(html[max(0, idx-100):end+50])
