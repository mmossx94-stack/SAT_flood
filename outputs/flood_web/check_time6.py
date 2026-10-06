import sys
import re
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    match = re.search(r'function date\(', html)
    if match:
        idx = match.start()
        print(html[idx:idx+250])
    else:
        print("Not found")
