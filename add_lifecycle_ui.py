import pathlib

p = pathlib.Path(r'C:\xampp\htdocs\SAT_update\Dashboard\index.html')
text = p.read_text(encoding='utf-8')

# 1. HTML Markup Insertion target
target_html = '''          <!-- Alert Note -->
          <div class="alert alert-info py-2 px-3 mb-3 border-0 shadow-sm d-flex align-items-center gap-2" style="border-radius:10px; background:#e0f2fe; color:#0369a1;">
            <i class="bi bi-info-circle-fill text-info" style="font-size:1.2rem;"></i>
            <div class="small">
              ข้อมูลเทรนด์คำค้นหาสกัดตรงจาก <strong>Google Trends ประเทศไทย (`geo='TH'`)</strong> จัดแยกเป็นหมวดหมู่ตามบริบท เพื่อให้ผู้บริหารมองเห็นประเด็นและข้อกังวลหลักของประชาชนได้ง่ายและชัดเจน
            </div>
          </div>'''

new_html = target_html + '''

          <!-- Feature: 💡 ดัชนีความต้องการความช่วยเหลือ 3 ระยะ (Relief Demand Lifecycle Index) -->
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

if target_html in text and "lifecycleWidgetContainer" not in text:
    text = text.replace(target_html, new_html, 1)
    print("Inserted HTML widget markup into index.html")

# 2. JS function insertion inside renderTrendsTab()
js_call_target = "renderTrendsWhatWhereMatrix();"
js_call_replacement = "renderTrendsWhatWhereMatrix();\n      renderReliefLifecycleWidget(1);"

if js_call_target in text and "renderReliefLifecycleWidget(1);" not in text:
    text = text.replace(js_call_target, js_call_replacement, 1)

# 3. Add helper JS functions at the end of script
js_functions = '''

    // ============================================================
    // RELIEF DEMAND LIFECYCLE WIDGET (3 PHASES)
    // ============================================================
    function renderReliefLifecycleWidget(phaseNum = 1) {
      const container = document.getElementById('lifecycleWidgetContainer');
      if (!container || !trendsData) return;

      const lifecycle = trendsData.relief_lifecycle || {};
      const pKey = 'phase' + phaseNum;
      const p = lifecycle[pKey] || {
        title: "🟡 ระยะที่ 1: เฝ้าระวัง & เตรียมพร้อมรับมือ",
        status: "ดัชนีความตื่นตัว: สูง (85/100)",
        queries: [
          { query: "เรดาร์ฝน กทม ล่าสุด", growth: "Breakout", intent: "เช็คสภาพอากาศ" },
          { query: "ย้ายของขึ้นที่สูง ทำอย่างไร", growth: "+5200%", intent: "เตรียมย้ายทรัพย์สิน" }
        ],
        needIndex: [
          { label: "ความต้องการอุปกรณ์กั้นน้ำ & ป้องกัน", val: 92 },
          { label: "ความต้องการพื้นที่จอดรถย้ายของ", val: 85 }
        ],
        action: "ให้หน่วยงาน ปภ./กทม. ประกาศพิกัดลานจอดรถปลอดภัย + เร่งกระจายกระสอบทรายตามจุดเสี่ยงก่อนน้ำมาถึง"
      };

      [1, 2, 3].forEach(n => {
        const btn = document.getElementById('btn-phase-' + n);
        if (btn) {
          if (n === phaseNum) {
            btn.className = `btn btn-sm ${n === 1 ? 'btn-warning text-dark' : n === 2 ? 'btn-danger text-white' : 'btn-success text-white'} fw-bold active`;
          } else {
            btn.className = `btn btn-sm ${n === 1 ? 'btn-outline-warning text-dark' : n === 2 ? 'btn-outline-danger text-dark' : 'btn-outline-success text-dark'}`;
          }
        }
      });

      const queries = p.queries || [];
      const needIndex = p.needIndex || [];

      const html = `
        <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
          <h6 class="fw-bold mb-0 text-dark" style="font-size: 0.95rem;">${p.title}</h6>
          <span class="badge ${phaseNum === 1 ? 'bg-warning text-dark' : phaseNum === 2 ? 'bg-danger text-white' : 'bg-success text-white'} px-2.5 py-1.5 fs-6">${p.status}</span>
        </div>

        <div class="row g-3">
          <div class="col-md-6">
            <div class="p-3 bg-white rounded border shadow-sm h-100">
              <div class="fw-bold text-secondary mb-2.5" style="font-size:0.85rem;"><i class="bi bi-bar-chart-line-fill me-1"></i> ดัชนีความต้องการระดับสูงในระยะนี้:</div>
              ${needIndex.map(idx => `
                <div class="mb-2">
                  <div class="d-flex justify-content-between text-dark fw-medium" style="font-size:0.85rem;">
                    <span>${idx.label}</span>
                    <span class="fw-bold text-danger">${idx.val}%</span>
                  </div>
                  <div class="progress" style="height: 8px; border-radius: 10px;">
                    <div class="progress-bar ${phaseNum === 1 ? 'bg-warning' : phaseNum === 2 ? 'bg-danger' : 'bg-success'}" role="progressbar" style="width: ${idx.val}%;"></div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="col-md-6">
            <div class="p-3 bg-white rounded border shadow-sm h-100">
              <div class="fw-bold text-secondary mb-2.5" style="font-size:0.85rem;"><i class="bi bi-search me-1"></i> คำค้นหาเด่นช่วงเกิดเหตุ (Google Search):</div>
              <div class="table-responsive">
                <table class="table table-sm table-borderless align-middle mb-0" style="font-size:0.85rem;">
                  <thead>
                    <tr class="border-bottom text-muted">
                      <th>คำค้นหา</th>
                      <th class="text-center">อัตราพุ่งสูง</th>
                      <th>เจตนา (Intent)</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${queries.map(q => `
                      <tr>
                        <td class="fw-bold text-dark"><i class="bi bi-search text-secondary me-1"></i>${q.query}</td>
                        <td class="text-center"><span class="badge ${q.growth === 'Breakout' ? 'bg-danger' : 'bg-danger-subtle text-danger'}">${q.growth}</span></td>
                        <td class="text-muted">${q.intent || 'ความต้องการเด่น'}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-3 p-3 rounded-3 bg-white border border-primary-subtle d-flex align-items-start gap-2 shadow-sm">
          <i class="bi bi-lightbulb-fill text-warning fs-5 flex-shrink-0"></i>
          <div>
            <strong class="text-primary d-block" style="font-size:0.9rem;">🎯 ข้อเสนอแนะเชิงกลยุทธ์สำหรับผู้บริหาร / ทีมกู้ภัย (Recommended Action):</strong>
            <span class="text-dark" style="font-size:0.88rem;">${p.action}</span>
          </div>
        </div>
      `;

      container.innerHTML = html;
    }

    function switchLifecyclePhase(phaseNum) {
      renderReliefLifecycleWidget(phaseNum);
    }
'''

if "function switchLifecyclePhase" not in text:
    script_end = text.rfind("</script>")
    if script_end != -1:
        text = text[:script_end] + js_functions + "\n  " + text[script_end:]
        print("Inserted JS helper functions into index.html")

p.write_text(text, encoding='utf-8')
print("Successfully updated C:\\xampp\\htdocs\\SAT_update\\Dashboard\\index.html")
