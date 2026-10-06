import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find('L.marker([r.latitude')
start = html.rfind('function', 0, idx)
end = html.find('}', idx) + 1
print(html[start:end])
