import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 2. Modify bkkMapTools HTML
old_tools = '<label><input type="checkbox" id="showShelterPins" checked>แสดงหมุดศูนย์พักพิง</label>'
new_tools = """<label><input type="checkbox" id="showShelterPins" checked>แสดงหมุดศูนย์พักพิง</label>
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

# 3. Add Event Listeners
# Let's just find `$('showShelterPins')` and add our listener after it.
old_listener = "$('showShelterPins')?.addEventListener('change',renderMap);"
new_listener = "$('showShelterPins')?.addEventListener('change',renderMap); document.querySelectorAll('.shelter-status-filter').forEach(el=>el.addEventListener('change',render));"
if old_listener in html:
    html = html.replace(old_listener, new_listener)
    print("Added event listeners")
else:
    # try another format
    idx = html.find("('showShelterPins')")
    if idx != -1:
        end = html.find(';', idx)
        old_l = html[idx-2:end+1]
        html = html.replace(old_l, old_l + "document.querySelectorAll('.shelter-status-filter').forEach(el=>el.addEventListener('change',render));")
        print("Added event listeners fallback")
    else:
        print("Could not find old listeners")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
