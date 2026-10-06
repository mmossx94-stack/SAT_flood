import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('function renderShelterTable')
    end = html.find('</table>', idx)
    print(html[idx:end+100])
