import sys
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    print("CSV:", html.find('CSV'))
