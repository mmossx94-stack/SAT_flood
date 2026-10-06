import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Increase map height
html = html.replace('.map{height:385px;', '.map{height:600px;')
html = html.replace('.map{height:320px}', '.map{height:450px}') # for mobile

# Decrease marker radius
# Stations: radius:3 -> radius:2 (since 1.5 might be too small and cause rendering issues, wait Leaflet allows float. Let's use 2)
# Or wait, I will use regex just in case there are spacing differences.

# Replace station radius
html = re.sub(
    r"radius:\s*3\s*,",
    "radius: 1.5,",
    html
)

# Replace shelter radius
html = re.sub(
    r"radius:\s*8\s*,",
    "radius: 4,",
    html
)
html = re.sub(
    r"weight:\s*3\s*",
    "weight: 1.5",
    html
)


with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated sizes")
