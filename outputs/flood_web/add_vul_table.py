import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add vulTable to HTML
old_html = '<div class="vulnerable" id="vulnerable"></div><p class="mini-note">ยังไม่ใช่จำนวนผู้ได้รับผลกระทบจริง • ไฟล์ไม่ได้ระบุวันอ้างอิงฐานประชากร • ไม่รวมแถว “รวมทั้งหมด” ซ้ำ</p></div>'
new_html = '<div class="vulnerable" id="vulnerable"></div><div class="table-wrap" id="vulTable" style="margin-top:20px;"></div><p class="mini-note" style="margin-top:12px;">ยังไม่ใช่จำนวนผู้ได้รับผลกระทบจริง • ไฟล์ไม่ได้ระบุวันอ้างอิงฐานประชากร • ไม่รวมแถว “รวมทั้งหมด” ซ้ำ</p></div>'
if old_html in html:
    html = html.replace(old_html, new_html)
    print("Added vulTable HTML")
else:
    print("Could not find vulnerable HTML")

# 2. Add box and table generation to JS
# Find the line: const v=DATA.vulnerable.filter...
old_js = "$('vulnerable').innerHTML=[['เด็ก 0-4 ปี',sum(v,'เด็ก 0-4 ปี')],['หญิงตั้งครรภ์',sum(v,'หญิงตั้งครรภ์')],['ผู้สูงอายุ 60 ปีขึ้นไป',sum(v,'ผู้สูงอายุ 60 ปีขึ้นไป')]].map(([t,n])=>card(t,fmt(n),'คน')).join('');"
new_js = """const affectedProvs = new Set(reports.filter(r => r.Current_Status === 'กำลังประสบภัย').map(r => r.Province)).size;
$('vulnerable').innerHTML=card('จังหวัดที่ประสบภัย',fmt(affectedProvs),'จังหวัด')+[['เด็ก 0-4 ปี',sum(v,'เด็ก 0-4 ปี')],['หญิงตั้งครรภ์',sum(v,'หญิงตั้งครรภ์')],['ผู้สูงอายุ 60 ปีขึ้นไป',sum(v,'ผู้สูงอายุ 60 ปีขึ้นไป')]].map(([t,n])=>card(t,fmt(n),'คน')).join('');
const vulHeaders = ['จังหวัด', 'เขตสุขภาพ', 'เด็ก 0-4 ปี', 'หญิงตั้งครรภ์', 'ผู้สูงอายุ 60 ปีขึ้นไป', 'รวม'];
const vulRows = v.slice().sort((a,b)=>((b['เด็ก 0-4 ปี']||0)+(b['หญิงตั้งครรภ์']||0)+(b['ผู้สูงอายุ 60 ปีขึ้นไป']||0))-((a['เด็ก 0-4 ปี']||0)+(a['หญิงตั้งครรภ์']||0)+(a['ผู้สูงอายุ 60 ปีขึ้นไป']||0))).map(r => {
  const c = (r['เด็ก 0-4 ปี']||0) + (r['หญิงตั้งครรภ์']||0) + (r['ผู้สูงอายุ 60 ปีขึ้นไป']||0);
  return [
    `<button class="linkbutton" data-province="${esc(r.province)}">${esc(r.province)}</button>`,
    esc(r.region||'-'),
    `<div style="text-align:right">${fmt(r['เด็ก 0-4 ปี']||0)}</div>`,
    `<div style="text-align:right">${fmt(r['หญิงตั้งครรภ์']||0)}</div>`,
    `<div style="text-align:right">${fmt(r['ผู้สูงอายุ 60 ปีขึ้นไป']||0)}</div>`,
    `<div style="text-align:right;font-weight:bold">${fmt(c)}</div>`
  ];
});
$('vulTable').innerHTML = table(vulHeaders, vulRows);
"""

if old_js in html:
    html = html.replace(old_js, new_js.replace('\n', ''))
    print("Added vulTable JS")
else:
    print("Could not find JS logic")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
