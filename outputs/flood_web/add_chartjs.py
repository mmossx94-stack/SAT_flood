import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_head = """<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">"""
new_head = """<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>"""

if old_head in html and "chart.js" not in html:
    html = html.replace(old_head, new_head)
    print("Added Chart.js script")
else:
    print("Chart.js already present or could not find anchor")

old_panel = """<div class="panel" style="flex: 1;">
      <div class="panel-head"><div><h2>กลุ่มเปราะบาง</h2><p class="sub" id="vulSub"></p></div></div>
      <div class="panel-body" id="vulTable" style="max-height: 400px; overflow-y: auto;"></div>
    </div>"""

new_panel = """<div class="panel" style="flex: 1; display: flex; flex-direction: column;">
      <div class="panel-head"><div><h2>กลุ่มเปราะบาง และผลกระทบ</h2><p class="sub" id="vulSub"></p></div></div>
      <div class="panel-body" style="flex: 1; display: flex; flex-direction: row; gap: 16px; align-items: center; justify-content: center; padding-bottom: 12px; padding-top: 12px; min-height: 200px;">
        <div style="flex: 3; position: relative; height: 100%; min-height: 180px;">
          <canvas id="vulChart"></canvas>
          <div id="vulChartEmpty" class="hidden" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); color:#94a3b8; font-size:13px;">ไม่มีข้อมูลกลุ่มเปราะบาง</div>
        </div>
        <div style="flex: 2; display: flex; flex-direction: column; gap: 12px;">
          <div class="stat-box" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:16px; text-align:center;">
            <div style="font-size:12px; color:#475569; margin-bottom:8px; font-weight:600;">ครัวเรือนที่ได้รับผลกระทบ</div>
            <div style="font-size:28px; font-weight:700; color:#dc2626; line-height:1;" id="vulHouseholds">-</div>
            <div style="font-size:11px; color:#64748b; margin-top:8px;">จากข้อมูล ปภ.</div>
          </div>
        </div>
      </div>
      <div style="padding: 0 16px 16px 16px; font-size: 11px; color: #94a3b8; text-align: center; border-top: 1px solid #f1f5f9; padding-top: 12px; margin-top: auto;">
        <b>ที่มาของข้อมูล:</b> ระบบคลังข้อมูลด้านการแพทย์และสุขภาพ (HDC) กระทรวงสาธารณสุข<br/>และ กรมป้องกันและบรรเทาสาธารณภัย (ปภ.)
      </div>
    </div>"""

if old_panel in html:
    html = html.replace(old_panel, new_panel)
    print("Replaced panel HTML")
else:
    print("Could not find old panel HTML")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
