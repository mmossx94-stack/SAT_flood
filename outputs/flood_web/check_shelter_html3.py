import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('id="shelterMap"')
    if idx == -1: print("shelterMap Not found"); sys.exit(0)
    print(html[max(0, idx-200):idx+800])
