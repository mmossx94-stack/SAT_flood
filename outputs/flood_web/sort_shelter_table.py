import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_side = "$('sideBody').innerHTML = '<table class=\"data-table\"><thead><tr style=\"position: sticky; top: 0; background: #f8fafc; z-index: 1;\"><th>เขต</th><th>ชื่อศูนย์</th><th>สถานะ</th><th class=\"num\" style=\"white-space:nowrap\">รองรับ (คน)</th></tr></thead><tbody>' + currentShelters.map(r => {"

new_side = """$('sideBody').innerHTML = '<table class="data-table"><thead><tr style="position: sticky; top: 0; background: #f8fafc; z-index: 1;"><th>เขต</th><th>ชื่อศูนย์</th><th>สถานะ</th><th class="num" style="white-space:nowrap">รองรับ (คน)</th></tr></thead><tbody>' + [...currentShelters].sort((a,b)=>{const rank=s=>s==='เต็ม'?1:(s==='ใกล้เต็ม'?2:(s==='เปิดให้บริการ/ว่าง'?3:4));const d=rank(a.status_source)-rank(b.status_source);if(d!==0)return d;return (a.district||'').localeCompare(b.district||'','th')||(a.shelter_name||'').localeCompare(b.shelter_name||'','th')}).map(r => {"""

if old_side in html:
    html = html.replace(old_side, new_side)
    print("Replaced sideBody JS to add sorting")
else:
    print("Could not find old sideBody JS")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
