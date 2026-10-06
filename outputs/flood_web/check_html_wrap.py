import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('id="shelterMapPanel"')
    end = html.find('</div>', html.find('</section>', idx) + 10)
    print(html[idx-50:end+150])
