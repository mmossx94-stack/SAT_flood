import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Modify HTML
old_html = '<table class="summary-table"><tbody id="shelterSummary"></tbody></table>'
new_html = '<div class="table-responsive" style="max-height: 520px; overflow-y: auto;"><table class="data-table"><thead><tr style="position: sticky; top: 0; background: #f8fafc; z-index: 1;"><th>เขต</th><th>ชื่อศูนย์</th><th>สถานะ</th><th class="num" style="white-space:nowrap">รองรับ (คน)</th></tr></thead><tbody id="shelterSummary"></tbody></table></div>'
if old_html in html:
    html = html.replace(old_html, new_html)
    print("Replaced HTML")
else:
    print("Could not find HTML")

# 2. Modify JS
old_js = """$('shelterSummary').innerHTML=
 `<tr><td>ศูนย์พักพิงในชุดข้อมูล</td><td class="num"><b>${fmt(currentShelters.length)} แห่ง</b></td></tr>`+
 `<tr><td>ความจุตามรายงาน</td><td class="num"><b>${fmt(cap)} คน</b></td></tr>`+
 `<tr><td>เต็ม / ใกล้เต็ม ตามสถานะต้นทาง</td><td class="num"><b>${fmt(fullShelters)} แห่ง</b></td></tr>`+
 (overCap?`<tr style="background:#fee2e2;color:#991b1b"><td>ผู้พักเกินความจุที่ระบุ</td><td class="num"><b>${fmt(overCap)} แห่ง</b></td></tr>`:'')+
 `<tr><td>มีพิกัดพร้อมแสดง</td><td class="num"><b>${fmt(pts.length)} / ${fmt(currentShelters.length)} แห่ง</b></td></tr>`;"""

new_js = """
$('shelterSummary').innerHTML = currentShelters.map(r => {
  const st = r.status_source || 'ไม่ทราบ';
  const c = st === 'เต็ม' ? '#dc2626' : (st === 'ใกล้เต็ม' ? '#ea580c' : (st === 'เปิดให้บริการ/ว่าง' ? '#16a34a' : '#6b7280'));
  return `<tr>
    <td>${esc(r.district || '-')}</td>
    <td>${esc(r.shelter_name || '-')}</td>
    <td style="color:${c}; white-space:nowrap; font-weight:500;">${esc(st)}</td>
    <td class="num">${fmt(r.capacity)}</td>
  </tr>`;
}).join('') || '<tr><td colspan="4" style="text-align:center;color:#666">ไม่มีศูนย์พักพิงในพื้นที่นี้</td></tr>';
"""
if old_js in html:
    html = html.replace(old_js, new_js)
    print("Replaced JS")
else:
    print("Could not find JS")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
