import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find("function time")
    if idx != -1:
        end = html.find("}", idx)
        print(html[idx:end+1])
    else:
        idx = html.find("const time=")
        end = html.find(";", idx)
        print(html[idx:end+1])
