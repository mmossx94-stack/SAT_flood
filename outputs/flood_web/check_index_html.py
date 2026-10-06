import sys
with open("outputs/flood_web/index.html", "r", encoding="utf-8") as f:
    html = f.read()
    print("Search index:", html.find('id="search"'))
    print("StatusFilter index:", html.find('id="statusFilter"'))
    print("TableSort index:", html.find('id="tableSort"'))
