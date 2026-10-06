import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find("leaflet@1.9.4/dist/leaflet.js")
print("leaflet.js at:", idx)
ctx = html[idx-100:idx+200]
print(ctx)
