import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = """const allowedStatuses = new Set(Array.from(document.querySelectorAll('.shelter-filter:checked')).map(cb=>cb.dataset.filter));
 const filteredShelters = currentShelters.filter(r=>allowedStatuses.has(getStatus(r)));"""
 
new_str = """const bkkShelters = DATA.shelters.filter(r=>(!state.district||r.district===state.district));
 const allowedStatuses = new Set(Array.from(document.querySelectorAll('.shelter-filter:checked')).map(cb=>cb.dataset.filter));
 const filteredShelters = bkkShelters.filter(r=>allowedStatuses.has(getStatus(r)));"""

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Made shelter map filters independent!")
else:
    print("Could not find old string")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
