import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = """<div class="map-tools" id="shelterMapTools" style="flex: 0 0 auto; display: flex; gap: 12px; align-items: center; padding: 12px 24px; border-bottom: 1px solid #e2e8f0; background: #fff;">
      <div style="display:flex; gap:8px; align-items:center;">
        <label style="display:flex; align-items:center; gap:6px; cursor:pointer; font-size:13px; color:#334155; user-select:none; white-space:nowrap;">
          <input type="checkbox" class="filter-pill-checkbox shelter-filter" data-filter="ว่าง" checked>
          <span class="filter-pill pill-green">ว่าง</span>
        </label>
        <label style="display:flex; align-items:center; gap:6px; cursor:pointer; font-size:13px; color:#334155; user-select:none; white-space:nowrap;">
          <input type="checkbox" class="filter-pill-checkbox shelter-filter" data-filter="ใกล้เต็ม" checked>
          <span class="filter-pill pill-orange">ใกล้เต็ม</span>
        </label>
        <label style="display:flex; align-items:center; gap:6px; cursor:pointer; font-size:13px; color:#334155; user-select:none; white-space:nowrap;">
          <input type="checkbox" class="filter-pill-checkbox shelter-filter" data-filter="เต็ม" checked>
          <span class="filter-pill pill-red">เต็ม</span>
        </label>
        <label style="display:flex; align-items:center; gap:6px; cursor:pointer; font-size:13px; color:#334155; user-select:none; white-space:nowrap;">
          <input type="checkbox" class="filter-pill-checkbox shelter-filter" data-filter="ไม่ทราบ" checked>
          <span class="filter-pill pill-gray">ไม่ทราบ</span>
        </label>
      </div>"""

new_str = """<div class="map-tools" id="shelterMapTools" style="flex: 0 0 auto; display: flex; gap: 12px; align-items: center; padding: 12px 24px; border-bottom: 1px solid #e2e8f0; background: #fff;">
      <div style="display:flex; gap:8px; align-items:center;">
        <label class="filter-pill"><input type="checkbox" class="shelter-filter" data-filter="ว่าง" value="เปิดให้บริการ/ว่าง" checked><span>ว่าง</span></label>
        <label class="filter-pill"><input type="checkbox" class="shelter-filter" data-filter="ใกล้เต็ม" value="ใกล้เต็ม" checked><span>ใกล้เต็ม</span></label>
        <label class="filter-pill"><input type="checkbox" class="shelter-filter" data-filter="เต็ม" value="เต็ม" checked><span>เต็ม</span></label>
        <label class="filter-pill"><input type="checkbox" class="shelter-filter" data-filter="ไม่ทราบ" value="ไม่ทราบสถานะ" checked><span>ไม่ทราบ</span></label>
      </div>"""

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Fixed pills html!")
else:
    print("Could not find old pills html!")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
