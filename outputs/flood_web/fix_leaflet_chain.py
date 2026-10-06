import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove the leaflet.heat script tag that was erroneously added at the top
html = html.replace(
    '<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>',
    ""
)

# 2. Also remove the leaflet.js script tag if we accidentally added it in head
html = html.replace(
    '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n',
    ""
)

# 3. Change the dynamic script loader to chain leaflet.heat BEFORE calling renderMap
old_loader = "const mapScript=document.createElement('script');mapScript.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';mapScript.onload=renderMap;"
new_loader = (
    "const mapScript=document.createElement('script');"
    "mapScript.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';"
    "mapScript.onload=()=>{"
      "const heatScript=document.createElement('script');"
      "heatScript.src='https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js';"
      "heatScript.onload=renderMap;"
      "heatScript.onerror=renderMap;"
      "document.head.appendChild(heatScript);"
    "};"
)

if old_loader in html:
    html = html.replace(old_loader, new_loader)
    print("Patched Leaflet chain loader")
else:
    print("ERROR: Could not find old loader")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
