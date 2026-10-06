import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

for line in html.split('\n'):
    if 'L.marker' in line:
        print(line[:300])
