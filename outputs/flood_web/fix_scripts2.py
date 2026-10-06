import re

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Problem: leaflet.heat is loaded at the TOP (line 1) before leaflet.js
# But leaflet.js is loaded INLINE inside the main JS somewhere (dynamically)
# Let me find where leaflet.js is dynamically loaded

idx = html.find("leaflet@1.9.4/dist/leaflet.js")
print("leaflet.js at:", idx)
print("Context:", repr(html[idx-100:idx+200]))
