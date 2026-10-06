import sys
import re

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

print("Unified filter classes:", len(re.findall(r'unified-filter', html)))
print("Filter button:", len(re.findall(r'ตัวกรอง', html)))
