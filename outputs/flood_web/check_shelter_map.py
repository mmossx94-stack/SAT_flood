import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('const shelterMap =')
    if idx == -1: idx = html.find('L.map(')
    end = html.find(';', idx+100)
    print(html[max(0, idx-50):end+150])
