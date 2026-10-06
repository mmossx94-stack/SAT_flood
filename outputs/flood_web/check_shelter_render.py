import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('function renderMap')
    print("renderMap found:", idx != -1)
    idx2 = html.find('shelterMap')
    print(html[idx2-50:idx2+500])
