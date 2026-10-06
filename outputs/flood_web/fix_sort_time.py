import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_sort = """    const timeA = new Date(a.updated_at_source || a.Ingested_At).getTime() || 0;
    const timeB = new Date(b.updated_at_source || b.Ingested_At).getTime() || 0;"""

new_sort = """    const timeA = new Date(a.observed_at_th || a.updated_at_source || a.Ingested_At).getTime() || 0;
    const timeB = new Date(b.observed_at_th || b.updated_at_source || b.Ingested_At).getTime() || 0;"""

if old_sort in html:
    html = html.replace(old_sort, new_sort)
    print("Fixed time parsing for sort!")
else:
    print("Could not find sort logic")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
