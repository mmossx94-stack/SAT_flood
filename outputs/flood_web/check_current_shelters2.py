import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('currentShelters=')
    if idx == -1: print("Not found"); sys.exit(0)
    end = html.find(';', idx)
    print(html[idx:end+1])
