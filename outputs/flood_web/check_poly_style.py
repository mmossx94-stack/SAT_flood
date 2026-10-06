import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('function renderDistrictWaterMap')
    end = html.find('onEachFeature', idx)
    print(html[idx:end])
