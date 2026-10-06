import pathlib

paths = [
    pathlib.Path(r'C:\xampp\htdocs\SAT_update\Dashboard\index.html'),
    pathlib.Path(r'f:\2569_น้ำท่วม\SAT\Dashboard\index.html')
]

lifecycle_html_block = '''          <!-- Feature: 💡 ดัชนีความต้องการความช่วยเหลือ 3 ระยะ (Relief Demand Lifecycle Index) -->
          <div class="row g-3 mb-4">
            <div class="col-12">
              <div class="modern-card p-3 shadow-sm border-0" style="border-top: 4px solid #f59e0b !important;">
                <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                  <div>
                    <h6 class="fw-bold mb-0 text-dark" style="font-size: 1.05rem;">
                      <i class="bi bi-diagram-3-fill text-warning me-1"></i> 💡 ดัชนีความต้องการความช่วยเหลือ 3 ระยะ (Relief Demand Lifecycle Index)
                    </h6>
                    <small class="text-muted"><i class="bi bi-info-circle me-1"></i> วิเคราะห์ความต้องการและข้อเสนอแนะเชิงกลยุทธ์จาก Google Trends ตามช่วงเวลาเกิดภัยพิบัติ</small>
                  </div>
                  <div class="btn-group btn-group-sm" role="group" id="lifecyclePhaseBtnGroup">
                    <button type="button" class="btn btn-warning fw-bold text-dark active" id="btn-phase-1" onclick="switchLifecyclePhase(1)">🟡 ระยะ 1: เฝ้าระวัง & เตรียมตัว</button>
                    <button type="button" class="btn btn-outline-danger" id="btn-phase-2" onclick="switchLifecyclePhase(2)">🔴 ระยะ 2: วิกฤต & อพยพด่วน</button>
                    <button type="button" class="btn btn-outline-success" id="btn-phase-3" onclick="switchLifecyclePhase(3)">🟢 ระยะ 3: ฟื้นฟู & ยื่นเยียวยา</button>
                  </div>
                </div>

                <div id="lifecycleWidgetContainer" class="bg-light p-3 rounded-3 border">
                  <!-- Rendered via JS -->
                </div>
              </div>
            </div>
          </div>'''

# Action box to remove from JS
old_action_box = '''        <div class="mt-3 p-3 rounded-3 bg-white border border-primary-subtle d-flex align-items-start gap-2 shadow-sm">
          <i class="bi bi-lightbulb-fill text-warning fs-5 flex-shrink-0"></i>
          <div>
            <strong class="text-primary d-block" style="font-size:0.9rem;">🎯 ข้อเสนอแนะเชิงกลยุทธ์สำหรับผู้บริหาร / ทีมกู้ภัย (Recommended Action):</strong>
            <span class="text-dark" style="font-size:0.88rem;">${p.action}</span>
          </div>
        </div>'''

for p in paths:
    if p.exists():
        text = p.read_text(encoding='utf-8')
        
        # 1. Remove html block from top position if present
        if lifecycle_html_block in text:
            text = text.replace(lifecycle_html_block, '', 1)
        
        # 2. Insert html block at bottom of pills-trends (before End tab-content)
        insert_marker = '<!-- End tab-content -->'
        if insert_marker in text and lifecycle_html_block not in text:
            # Insert before pills-trends main-content closing div
            end_trends_pos = text.find(insert_marker)
            # find last </div></div> before insert_marker
            last_divs = text.rfind('</div>\n      </div>', 0, end_trends_pos)
            if last_divs != -1:
                text = text[:last_divs] + lifecycle_html_block + '\n\n' + text[last_divs:]

        # 3. Remove action box from renderReliefLifecycleWidget JS function
        if old_action_box in text:
            text = text.replace(old_action_box, '')

        p.write_text(text, encoding='utf-8')
        print(f"Updated {p}")
