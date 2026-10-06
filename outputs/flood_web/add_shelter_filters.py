import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Insert CSS
css = """
.filter-pill { cursor: pointer; display: inline-flex; align-items: center; margin-bottom:0 !important; }
.filter-pill input { display: none; }
.filter-pill span { padding: 3px 10px; border: 1px solid #d1d5db; border-radius: 12px; font-size: 12px; background: white; color: #6b7280; transition: all 0.2s; }
.filter-pill input:checked + span { background: #f1f5f9; border-color: #94a3b8; color: #0f172a; font-weight: 500; }
.filter-pill input[value="เต็ม"]:checked + span { background: #fee2e2; border-color: #fca5a5; color: #991b1b; }
.filter-pill input[value="ใกล้เต็ม"]:checked + span { background: #ffedd5; border-color: #fdba74; color: #9a3412; }
.filter-pill input[value="เปิดให้บริการ/ว่าง"]:checked + span { background: #dcfce7; border-color: #86efac; color: #166534; }
</style>
"""
html = html.replace("</style>", css, 1)

# 2. Modify bkkMapTools HTML
old_tools = '<label><input type="checkbox" id="showShelterPins" checked> แสดงหมุดศูนย์พักพิง</label>'
new_tools = """<label><input type="checkbox" id="showShelterPins" checked> แสดงหมุดศูนย์พักพิง</label>
 <div id="shelterFilters" style="display:flex; gap:6px; flex-wrap:wrap; border-left:1px solid #ddd; padding-left:10px;">
  <label class="filter-pill"><input type="checkbox" class="shelter-status-filter" value="เปิดให้บริการ/ว่าง" checked> <span>ว่าง</span></label>
  <label class="filter-pill"><input type="checkbox" class="shelter-status-filter" value="ใกล้เต็ม" checked> <span>ใกล้เต็ม</span></label>
  <label class="filter-pill"><input type="checkbox" class="shelter-status-filter" value="เต็ม" checked> <span>เต็ม</span></label>
  <label class="filter-pill"><input type="checkbox" class="shelter-status-filter" value="ไม่ทราบสถานะ" checked> <span>ไม่ทราบ</span></label>
 </div>"""
if old_tools in html:
    html = html.replace(old_tools, new_tools)
    print("Replaced map tools HTML")
else:
    print("Could not find map tools HTML")

# 3. Add Event Listeners for new checkboxes
old_listeners = "$('showHealthRegions').addEventListener('change',renderHealthRegions);$('showStationPins').addEventListener('change',renderMap);$('showShelterPins').addEventListener('change',renderMap);"
new_listeners = old_listeners + "document.querySelectorAll('.shelter-status-filter').forEach(el=>el.addEventListener('change',render));"
if old_listeners in html:
    html = html.replace(old_listeners, new_listeners)
    print("Added event listeners")
else:
    print("Could not find old listeners")

# 4. Modify currentShelters array building in render()
old_array = "currentShelters=bkk?DATA.shelters.filter(r=>!state.district||r.district===state.district):[];"
new_array = "const activeShelterFilters=new Set(Array.from(document.querySelectorAll('.shelter-status-filter:checked')).map(el=>el.value)); currentShelters=bkk?DATA.shelters.filter(r=>(!state.district||r.district===state.district)&&activeShelterFilters.has(String(r.status_source||'ไม่ทราบสถานะ').trim())):[];"
if old_array in html:
    html = html.replace(old_array, new_array)
    print("Modified currentShelters building")
else:
    print("Could not find old array building")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
