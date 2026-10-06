import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_html = """<section class="panel hidden" id="shelterMapPanel"><div class="panel-head"><div><h2>แผนที่ศูนย์พักพิง กรุงเทพมหานคร</h2><p class="sub" id="shelterMapSubtitle"></p></div><span class="badge" id="shelterMapCount"></span></div><div id="shelterMap" class="map" aria-label="แผนที่ศูนย์พักพิง กรุงเทพมหานคร"></div><div class="map-legend" id="shelterStatusLegend"></div><div class="map-source" id="shelterMapSource"></div></section>"""

new_html = """
<div class="split-layout hidden" id="shelterMapPanel">
  <section class="panel map-panel" style="display: flex; flex-direction: column;">
    <div class="panel-head" style="flex: 0 0 auto;">
      <div><h2>แผนที่ศูนย์พักพิง กรุงเทพมหานคร</h2><p class="sub" id="shelterMapSubtitle">ทุกเขต กทม. · แสดงร่วมกับสถานะระดับน้ำ</p></div>
    </div>
    
    <div class="map-tools" id="shelterMapTools" style="flex: 0 0 auto; display: flex; gap: 12px; align-items: center; padding: 12px 24px; border-bottom: 1px solid #e2e8f0; background: #fff;">
      <div style="display:flex; gap:8px; align-items:center;">
        <label style="display:flex; align-items:center; gap:6px; cursor:pointer; font-size:13px; color:#334155; user-select:none; white-space:nowrap;">
          <input type="checkbox" class="filter-pill-checkbox" data-filter="ว่าง" checked>
          <span class="filter-pill pill-green">ว่าง</span>
        </label>
        <label style="display:flex; align-items:center; gap:6px; cursor:pointer; font-size:13px; color:#334155; user-select:none; white-space:nowrap;">
          <input type="checkbox" class="filter-pill-checkbox" data-filter="ใกล้เต็ม" checked>
          <span class="filter-pill pill-orange">ใกล้เต็ม</span>
        </label>
        <label style="display:flex; align-items:center; gap:6px; cursor:pointer; font-size:13px; color:#334155; user-select:none; white-space:nowrap;">
          <input type="checkbox" class="filter-pill-checkbox" data-filter="เต็ม" checked>
          <span class="filter-pill pill-red">เต็ม</span>
        </label>
        <label style="display:flex; align-items:center; gap:6px; cursor:pointer; font-size:13px; color:#334155; user-select:none; white-space:nowrap;">
          <input type="checkbox" class="filter-pill-checkbox" data-filter="ไม่ทราบ" checked>
          <span class="filter-pill pill-gray">ไม่ทราบ</span>
        </label>
      </div>
      <div style="flex: 1;"></div>
      <button onclick="shelterMap.fitBounds(L.latLngBounds([13.4, 100.3], [14.0, 100.9]), {padding:[20,20]})" style="white-space:nowrap; padding:6px 12px; border:1px solid #cbd5e1; border-radius:6px; background:#fff; cursor:pointer; font-size:13px; color:#475569;">จัดแผนที่ให้พอดี</button>
    </div>

    <div id="shelterMap" class="map" aria-label="แผนที่ศูนย์พักพิง กรุงเทพมหานคร" style="flex: 1 1 auto; height: 100%;"></div>
    
    <div style="flex: 0 0 auto; padding: 16px 24px; background: #fff; border-top: 1px solid #e2e8f0;">
      <div class="map-legend" id="shelterMapLegend2" style="padding:0; border:0; background:transparent"></div>
      <div class="map-legend" id="shelterStatusLegend" style="padding-top:12px; border:0; background:transparent"></div>
      <p class="map-source" id="shelterMapNote" style="margin-top:12px"></p>
      <div class="map-source" id="shelterMapSource" style="margin-top:16px"></div>
    </div>
  </section>

  <section class="panel">
    <div class="panel-head">
      <div><h2>รายชื่อศูนย์พักพิง</h2><p class="sub" id="shelterSideSub"></p></div>
    </div>
    <div class="panel-body" id="shelterSideBody" style="max-height: 520px; overflow-y: auto; padding-right: 12px; padding-left: 12px;"></div>
  </section>
</div>
"""

if old_html in html:
    html = html.replace(old_html, new_html)
    print("Replaced layout!")
else:
    print("Could not find old layout")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
