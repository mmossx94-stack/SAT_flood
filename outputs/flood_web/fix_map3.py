with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make the dots bigger and more visible (heatmap style)
import re

content = re.sub(
    r"L\.circleMarker\(\[r\.latitude,r\.longitude\],\{radius:\s*[\d\.]+,fillColor:c,color:'#[a-zA-Z0-9]+',weight:[\d\.]+,fillOpacity:1\}\)",
    "L.circleMarker([r.latitude,r.longitude],{radius:6,fillColor:c,color:'#000',weight:0.5,fillOpacity:0.9})",
    content
)

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated station dot size")
