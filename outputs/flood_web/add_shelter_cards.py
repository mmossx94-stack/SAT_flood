import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. HTML Additions
old_html1 = '<div class="hidden" id="shelterMapPanel" style="display: flex; gap: 24px; align-items: stretch; margin-bottom: 24px">'
new_html1 = """<div class="cards hidden" id="shelterCards" style="margin-top: 32px; margin-bottom: 24px;"></div>
<div class="hidden" id="shelterMapPanel" style="display: flex; gap: 24px; align-items: stretch; margin-bottom: 24px">"""
if old_html1 in html:
    html = html.replace(old_html1, new_html1)
    print("Added shelterCards HTML")
else:
    print("Could not find shelterMapPanel start")

old_html2 = '<h2>รายชื่อศูนย์พักพิง</h2>'
new_html2 = '<h2>ศูนย์พักพิงที่เต็ม / ใกล้เต็ม</h2>'
if old_html2 in html:
    html = html.replace(old_html2, new_html2)
    print("Changed right panel title")

old_html3 = '</div>\n  </section>\n</div>\n\n<div class="section-title">'
new_html3 = """</div>
  </section>
</div>

<section class="panel hidden" id="allSheltersPanel" style="margin-bottom: 32px;">
  <div class="panel-head">
    <div><h2>รายชื่อศูนย์พักพิงทั้งหมด</h2><p class="sub">ทุกสถานะ เรียงตามความหนาแน่นและตัวอักษร</p></div>
  </div>
  <div class="panel-body" id="allSheltersBody" style="max-height: 500px; overflow-y: auto; padding: 0 12px 12px 12px;"></div>
</section>

<div class="section-title">"""
if 'id="shelterSideBody"' in html:
    # Just insert allSheltersPanel before <div class="section-title">
    idx = html.find('<div class="section-title">', html.find('id="shelterSideBody"'))
    html = html[:idx] + """<section class="panel hidden" id="allSheltersPanel" style="margin-bottom: 32px;">
  <div class="panel-head">
    <div><h2>รายชื่อศูนย์พักพิงทั้งหมด</h2><p class="sub">ทุกสถานะ เรียงตามสถานะการเข้าพัก</p></div>
  </div>
  <div class="panel-body" id="allSheltersBody" style="max-height: 500px; overflow-y: auto; padding: 0 12px 12px 12px;"></div>
</section>\n\n""" + html[idx:]
    print("Added allSheltersPanel HTML")
else:
    print("Could not insert allSheltersPanel")


# 2. JS Additions
# In render() function:
old_render = "$('shelterMapPanel').classList.toggle('hidden',!bkk);"
new_render = "$('shelterMapPanel').classList.toggle('hidden',!bkk);\n$('shelterCards').classList.toggle('hidden',!bkk);\n$('allSheltersPanel').classList.toggle('hidden',!bkk);"
if old_render in html:
    html = html.replace(old_render, new_render)
    print("Added toggle hidden to render()")


# In renderShelterMap:
old_js1 = """const bkkShelters = DATA.shelters.filter(r=>(!state.district||r.district===state.district));
 const allowedStatuses = new Set(Array.from(document.querySelectorAll('.shelter-filter:checked')).map(cb=>cb.dataset.filter));
 const filteredShelters = bkkShelters.filter(r=>allowedStatuses.has(getShelterStatus(r)));"""

new_js1 = """const bkkShelters = DATA.shelters.filter(r=>(!state.district||r.district===state.district));
 const allowedStatuses = new Set(Array.from(document.querySelectorAll('.shelter-filter:checked')).map(cb=>cb.dataset.filter));
 const filteredShelters = bkkShelters.filter(r=>allowedStatuses.has(getShelterStatus(r)));
 
 const totalShelters = bkkShelters.length;
 const fullShelters = bkkShelters.filter(r => getShelterStatus(r) === 'เต็ม').length;
 const almostFullShelters = bkkShelters.filter(r => getShelterStatus(r) === 'ใกล้เต็ม').length;
 
 let noShelterOrFullDistricts = 0;
 const targetDistricts = state.district ? [state.district] : districts;
 for (const d of targetDistricts) {
   const sInD = DATA.shelters.filter(r => r.district === d);
   if (sInD.length === 0) {
     noShelterOrFullDistricts++;
   } else {
     if (sInD.every(r => getShelterStatus(r) === 'เต็ม')) noShelterOrFullDistricts++;
   }
 }
 
 $('shelterCards').innerHTML = 
   card('ศูนย์พักพิงทั้งหมด', totalShelters, 'แห่ง', state.district ? `ในเขต${state.district}` : 'ใน กทม.') +
   card('ศูนย์ที่เต็มแล้ว', fullShelters, 'แห่ง', 'ไม่สามารถรับผู้พักเพิ่มได้', true) +
   card('ศูนย์ที่ใกล้เต็ม', almostFullShelters, 'แห่ง', 'ต้องเฝ้าระวังพิเศษ', true) +
   card('เขตที่ไม่มีศูนย์/เต็มหมด', noShelterOrFullDistricts, 'เขต', `จาก ${targetDistricts.length} เขต`);
"""
if old_js1 in html:
    html = html.replace(old_js1, new_js1)
    print("Added cards logic to renderShelterMap")

old_js2 = "renderShelterTable(filteredShelters);"
new_js2 = "renderShelterTable(filteredShelters.filter(r => ['เต็ม', 'ใกล้เต็ม'].includes(getShelterStatus(r))));\n renderAllSheltersTable(bkkShelters);"
if old_js2 in html:
    html = html.replace(old_js2, new_js2)
    print("Updated table calls in renderShelterMap")


# Add new renderAllSheltersTable function
new_func = """
function renderAllSheltersTable(shelters) {
  const sorted = [...shelters].sort((a,b) => {
    const rank = s => s==='เต็ม'?3 : s==='ใกล้เต็ม'?2 : s==='ว่าง'?1 : 0;
    const diff = rank(getShelterStatus(b)) - rank(getShelterStatus(a));
    if(diff !== 0) return diff;
    return (a.district||'').localeCompare(b.district||'','th');
  });
  
  const rowsHtml = sorted.map(s => {
    const st = getShelterStatus(s);
    const stColor = st==='เต็ม'?'#dc2626':st==='ใกล้เต็ม'?'#ea580c':st==='ว่าง'?'#16a34a':'#64748b';
    return `<tr>
      <td>${esc(s.district||'ไม่ระบุ')}</td>
      <td>${esc(s.shelter_name)}</td>
      <td class="num">${fmt(s.capacity)}</td>
      <td class="num">${fmt(s.occupied)}</td>
      <td style="color:${stColor}; font-weight:600">${esc(st)}</td>
    </tr>`;
  }).join('');
  
  $('allSheltersBody').innerHTML = `<table class="data-table">
    <thead>
      <tr style="position: sticky; top: 0; background: #fff; z-index: 1;">
        <th>เขต</th>
        <th>ชื่อศูนย์พักพิง</th>
        <th class="num">ความจุ (คน)</th>
        <th class="num">ผู้ใช้บริการ (คน)</th>
        <th>สถานะ</th>
      </tr>
    </thead>
    <tbody>
      ${rowsHtml || '<tr><td colspan="5" style="text-align:center;color:#666">ไม่มีศูนย์พักพิงในพื้นที่นี้</td></tr>'}
    </tbody>
  </table>`;
}
"""

if 'function renderAllSheltersTable' not in html:
    html = html.replace('function renderShelterTable', new_func + '\nfunction renderShelterTable')
    print("Added renderAllSheltersTable function")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
