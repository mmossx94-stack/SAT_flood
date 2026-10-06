import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the Carto tileLayer
html = re.sub(r"L\.tileLayer\(.*?\)\.addTo\(map\);", "", html)

# Make background white
html = html.replace(
    "map=L.map('map',{scrollWheelZoom:false}).setView([13.7,100.5],6);",
    "map=L.map('map',{scrollWheelZoom:false}).setView([13.7,100.5],6); document.getElementById('map').style.background = '#ffffff';"
)

# Render PROVINCES_GEOJSON for both tabs
html = html.replace(
    "if (window.PROVINCES_GEOJSON && state.tab === 'national') {",
    "if (window.PROVINCES_GEOJSON) {"
)

# For Bangkok tab, color Bangkok and make other provinces white or transparent with border
html = html.replace(
    "const disaster = DATA.disasters.filter(r => r.Province === prov && r.Report_Date.startsWith(state.date));",
    "const disaster = DATA.disasters.filter(r => r.Province === prov && r.Report_Date.startsWith(state.date));\n            if (state.tab === 'bkk' && prov !== 'กรุงเทพมหานคร') return { color: '#ddd', weight: 1, fillColor: '#f9f9f9', fillOpacity: 1 };"
)

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Removed basemap completely")
