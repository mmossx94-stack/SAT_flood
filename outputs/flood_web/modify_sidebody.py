import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_side = """$('sideBody').innerHTML=metric('ศูนย์พักพิงในชุดข้อมูล',fmt(currentShelters.length)+' แห่ง')+metric('ความจุตามรายงาน',currentShelters.length?fmt(sum(currentShelters,'capacity'))+' คน':'ไม่มีข้อมูล')+metric('เต็ม / ใกล้เต็ม ตามสถานะต้นทาง',fmt(currentShelters.filter(r=>['เต็ม','ใกล้เต็ม'].includes(r.status_source)).length)+' แห่ง')+metric('ผู้พักเกินความจุที่ระบุ',badge(fmt(over.length)+' แห่ง',over.length?'bad':''))+metric('มีพิกัดพร้อมแสดง',fmt(coords.length)+' / '+fmt(currentShelters.length)+' แห่ง')+'<p class="mini-note">ที่ว่างใช้ยอดต้นทาง ไม่คำนวณจากความจุรวมลบผู้พัก เพราะมีบางศูนย์รับผู้พักเกินความจุ</p>';"""

new_side = """$('sideBody').innerHTML = '<table class="data-table"><thead><tr style="position: sticky; top: 0; background: #f8fafc; z-index: 1;"><th>เขต</th><th>ชื่อศูนย์</th><th>สถานะ</th><th class="num" style="white-space:nowrap">รองรับ (คน)</th></tr></thead><tbody>' + currentShelters.map(r => { const st = r.status_source || 'ไม่ทราบ'; const c = st === 'เต็ม' ? '#dc2626' : (st === 'ใกล้เต็ม' ? '#ea580c' : (st === 'เปิดให้บริการ/ว่าง' ? '#16a34a' : '#6b7280')); return `<tr><td>${esc(r.district || '-')}</td><td>${esc(r.shelter_name || '-')}</td><td style="color:${c}; white-space:nowrap; font-weight:500; font-size:12px;">${esc(st)}</td><td class="num">${fmt(r.capacity)}</td></tr>`; }).join('') + (currentShelters.length ? '' : '<tr><td colspan="4" style="text-align:center;color:#666">ไม่มีศูนย์พักพิง</td></tr>') + '</tbody></table>';"""

if old_side in html:
    html = html.replace(old_side, new_side)
    print("Replaced sideBody JS")
else:
    print("Could not find old sideBody JS")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
