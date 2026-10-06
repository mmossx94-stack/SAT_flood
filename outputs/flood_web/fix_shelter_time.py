import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_source = """const shelterTime = currentShelters.map(r=>r.Ingested_At).filter(x=>x).sort().pop();"""
new_source = """const shelterTime = currentShelters.map(r=>r.Ingested_At||r.updated_at_source||r.fetched_at_th).filter(x=>x).sort().pop();"""

if old_source in html:
    html = html.replace(old_source, new_source)
    print("Fixed shelter time!")
else:
    print("Could not find old shelter time")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
