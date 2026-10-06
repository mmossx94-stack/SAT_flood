import sys
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    print("search:", 'id="search"' in html)
    print("tableSort:", 'id="tableSort"' in html)
