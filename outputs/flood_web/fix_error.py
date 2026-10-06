import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("$('shelterPanel').classList.toggle('hidden',!bkk);", "")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Removed old JS reference to shelterPanel")
