import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the tileLayer
old_layer = "L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a>',maxZoom:18}).addTo(map);"
new_layer = "L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{attribution:'&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors &copy; <a href=\"https://carto.com/attributions\">CARTO</a>',subdomains:'abcd',maxZoom:20}).addTo(map); document.getElementById('map').style.background = '#ffffff';"

if old_layer in html:
    html = html.replace(old_layer, new_layer)
else:
    # try regex just in case
    html = re.sub(
        r"L\.tileLayer\('https://\{s\}\.tile\.openstreetmap\.org.*?\.addTo\(map\);",
        new_layer,
        html
    )

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Basemap updated to CartoDB Positron")
