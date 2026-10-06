import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# The broken text to replace
broken_text = """const sortedDistricts=Array.from(distStats.entries()).filter(([_,s])=>s.วิกฤต>0||s.เตือนภัย>0||s.ปกติ>0).sort((a,b) => (b.r?.Affected_Households||0) - (a.r?.Affected_Households||0));   $('areaTable').innerHTML="""

# The replacement code
replacement = """const sortedDistricts = Array.from(distStats.entries())
    .filter(([_,s]) => s.วิกฤต > 0 || s.เตือนภัย > 0 || s.ปกติ > 0)
    .sort((a,b) => b[1].วิกฤต - a[1].วิกฤต || b[1].เตือนภัย - a[1].เตือนภัย || b[1].ปกติ - a[1].ปกติ);
    
  $('sideBody').innerHTML = table(['เขต', 'วิกฤต', 'เตือนภัย', 'ปกติ', 'เก่า >24ชม.'], sortedDistricts.map(([d, s]) => {
    const old = currentStations.filter(r => r.district_or_area === d && quality(r) !== 'ภายใน 24 ชั่วโมง').length;
    return [
      `<button class="linkbutton" data-district="${esc(d)}">${esc(d)}</button>`,
      s.วิกฤต ? `<span class="badge" style="background:#dc2626;color:#fff">${s.วิกฤต}</span>` : '-',
      s.เตือนภัย ? `<span class="badge" style="background:#ea580c;color:#fff">${s.เตือนภัย}</span>` : '-',
      s.ปกติ ? `<span class="badge" style="background:#16a34a;color:#fff">${s.ปกติ}</span>` : '-',
      old ? `<span class="badge" style="background:#64748b;color:#fff">${old}</span>` : '-'
    ];
  }));
} else {
  $('sideTitle').textContent = 'ตารางสรุปผลกระทบ ปภ.';
  $('sideSub').textContent = state.province || state.region || 'จัดอันดับตามจำนวนครัวเรือนเดือดร้อน';
  const headers = ['จังหวัด', 'อำเภอ', 'ตำบล', 'ครัวเรือน', 'เสียชีวิต'];
  const sortedRows = allowed.map(p => reports.find(x => x.Province === p))
    .filter(r => r && r.Current_Status === 'กำลังประสบภัย')
    .sort((a,b) => (b.Affected_Households||0) - (a.Affected_Households||0));
  $('sideBody').innerHTML = table(headers, sortedRows.map(r => [
    `<button class="linkbutton" data-province="${esc(r.Province)}">${esc(r.Province)}</button>`,
    `<div style="max-width:120px;white-space:normal;font-size:13px">${esc(r.District_Names || (r.Affected_Districts_Count ?? '-'))}</div>`,
    `<div style="text-align:right">${esc(r.Affected_Subdistricts_Count ?? '-')}</div>`,
    `<div style="text-align:right;font-weight:bold;color:#991b1b">${fmt(r.Affected_Households)}</div>`,
    `<div style="text-align:right">${r.Casualties_Deaths == null ? '-' : fmt(r.Casualties_Deaths)}</div>`
  ]));
}

$('areaTable').innerHTML="""

if broken_text in js:
    js = js.replace(broken_text, replacement)
    with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("Recreated sideBody rendering successfully!")
else:
    print("Broken text not found.")
