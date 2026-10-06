import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find('id="shelterSummary"')
    print(html[idx-150:idx+50])
    
    idx2 = html.find("('shelterSummary').innerHTML")
    end2 = html.find(";", idx2)
    print(html[idx2-50:end2+50])
