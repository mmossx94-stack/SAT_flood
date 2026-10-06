import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find('shelter-pin')
start = html.rfind('currentShelters.forEach', 0, idx)
end = html.find('});', idx) + 3

print(html[start:end])
