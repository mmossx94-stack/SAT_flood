import sys
import re
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    match = re.search(r'(?:const|let|var|function)\s+time\b', html)
    if match:
        idx = match.start()
        print(html[idx:idx+150])
    else:
        print("Not found")
