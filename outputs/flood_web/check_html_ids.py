import sys, re
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    print("search:", bool(re.search(r'id=[\'"]?search[\'"]?', html)))
    print("statusFilter:", bool(re.search(r'id=[\'"]?statusFilter[\'"]?', html)))
    print("tableSort:", bool(re.search(r'id=[\'"]?tableSort[\'"]?', html)))
