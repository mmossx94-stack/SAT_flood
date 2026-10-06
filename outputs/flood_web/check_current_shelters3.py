import sys
import re
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    match = re.search(r'currentShelters\s*=\s*', html[html.find('function render()'):])
    if match:
        idx = html.find('function render()') + match.end()
        end = html.find(';', idx)
        print(html[idx:end+1])
