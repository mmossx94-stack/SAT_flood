import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('const fullShelters')
    end = html.find('</div>`;', idx)
    print(html[max(0, idx-100):end+50])
