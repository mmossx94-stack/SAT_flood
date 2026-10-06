import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = """const allowedStatuses = new Set(Array.from(document.querySelectorAll('.shelter-filter:checked')).map(cb=>cb.dataset.filter));
 const filteredShelters = currentShelters.filter(r=>allowedStatuses.has(canonicalShelterStatus(r.occupied,r.capacity)));"""

new_str = """const getStatus = r => { let s=String(r.status_source||'').trim(); return s==='เปิดให้บริการ/ว่าง'?'ว่าง':s==='ใกล้เต็ม'?'ใกล้เต็ม':s==='เต็ม'?'เต็ม':'ไม่ทราบ'; };
 const allowedStatuses = new Set(Array.from(document.querySelectorAll('.shelter-filter:checked')).map(cb=>cb.dataset.filter));
 const filteredShelters = currentShelters.filter(r=>allowedStatuses.has(getStatus(r)));"""

html = html.replace(old_str, new_str)

old_str2 = """const sa = canonicalShelterStatus(a.occupied, a.capacity);
    const sb = canonicalShelterStatus(b.occupied, b.capacity);"""
new_str2 = """const sa = getStatus(a);
    const sb = getStatus(b);"""

html = html.replace(old_str2, new_str2)

old_str3 = """const st = canonicalShelterStatus(s.occupied, s.capacity);"""
new_str3 = """const st = getStatus(s);"""

html = html.replace(old_str3, new_str3)

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
