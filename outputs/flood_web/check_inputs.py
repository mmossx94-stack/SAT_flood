import sys
import re
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    print("Inputs:", re.findall(r'<input[^>]+id=[\'"]?([^\'" >]+)[\'"]?', html))
    print("Selects:", re.findall(r'<select[^>]+id=[\'"]?([^\'" >]+)[\'"]?', html))
