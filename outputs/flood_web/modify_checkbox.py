import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_checkbox = '<input type="checkbox" id="showShelterPins" checked>'
new_checkbox = '<input type="checkbox" id="showShelterPins">'

if old_checkbox in html:
    html = html.replace(old_checkbox, new_checkbox)
    print("Replaced checkbox!")
else:
    print("Could not find old checkbox")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
