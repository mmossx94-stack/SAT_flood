import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    if 'filter-pill-checkbox' in html[:html.find('</style>')]:
        print("Found filter-pill-checkbox in CSS")
    else:
        print("NOT FOUND in CSS")
