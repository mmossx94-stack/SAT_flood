import sys
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    print("Search:", 'id="search"' in html)
    print("StatusFilter:", 'id="statusFilter"' in html)
    print("TableSort:", 'id="tableSort"' in html)
