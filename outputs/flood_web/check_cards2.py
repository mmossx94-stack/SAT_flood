import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find("innerHTML=")
    while idx != -1:
        if "card(" in html[idx:idx+150]:
            print(html[idx-30:idx+400])
        idx = html.find("innerHTML=", idx+1)
