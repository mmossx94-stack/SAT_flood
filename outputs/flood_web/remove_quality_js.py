import sys
import re
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace $('quality').innerHTML=...;
html = re.sub(r"\$\('quality'\)\.innerHTML=.*?;", "", html, flags=re.DOTALL)
# Replace $('actions').innerHTML=...;
html = re.sub(r"\$\('actions'\)\.innerHTML=.*?;", "", html, flags=re.DOTALL)

# Find function renderShelterTable(shelters) but there's also the old renderShelterTable logic somewhere?
# I'll just write it back.
with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Removed quality and actions via regex.")
