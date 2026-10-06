import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# I will just replace the entire vulnerable JS block
old_js = """const affectedProvs = new Set(reports.filter(r => r.Current_Status === 'กำลังประสบภัย').map(r => r.Province)).size;
$('vulnerable').innerHTML=card('จังหวัดที่ประสบภัย',fmt(affectedProvs),'จังหวัด')+[['เด็ก 0-4 ปี',sum(v,'เด็ก 0-4 ปี')],['หญิงตั้งครรภ์',sum(v,'หญิงตั้งครรภ์')],['ผู้สูงอายุ 60 ปีขึ้นไป',sum(v,'ผู้สูงอายุ 60 ปีขึ้นไป')]].map(([t,n])=>card(t,fmt(n),'คน')).join('');
const vulHeaders = ['จังหวัด', 'เขตสุขภาพ', 'เด็ก 0-4 ปี', 'หญิงตั้งครรภ์', 'ผู้สูงอายุ 60 ปีขึ้นไป', 'รวมกลุ่มเปราะบาง'];
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
$('vulTable').innerHTML = table(vulHeaders, vulRows);"""

new_js = """const affectedProvs = new Set(reports.filter(r => r.Current_Status === 'กำลังประสบภัย').map(r => r.Province)).size;
$('vulnerable').innerHTML=card('จังหวัดที่ประสบภัย',fmt(affectedProvs),'จังหวัด')+[['เด็ก 0-4 ปี',sum(v,'children')],['หญิงตั้งครรภ์',sum(v,'pregnant')],['ผู้สูงอายุ 60 ปีขึ้นไป',sum(v,'elderly')]].map(([t,n])=>card(t,fmt(n),'คน')).join('');
const vulHeaders = ['จังหวัด', 'เขตสุขภาพ', 'เด็ก 0-4 ปี', 'หญิงตั้งครรภ์', 'ผู้สูงอายุ 60 ปีขึ้นไป', 'รวมกลุ่มเปราะบาง'];
const vulRows = v.slice().sort((a,b)=>((b.children||0)+(b.pregnant||0)+(b.elderly||0))-((a.children||0)+(a.pregnant||0)+(a.elderly||0))).map(r => {
  const c = (r.children||0) + (r.pregnant||0) + (r.elderly||0);
  return [
    `<button class="linkbutton" data-province="${esc(r.province)}">${esc(r.province)}</button>`,
    esc(r.region||'-'),
    `<div style="text-align:right">${fmt(r.children||0)}</div>`,
    `<div style="text-align:right">${fmt(r.pregnant||0)}</div>`,
    `<div style="text-align:right">${fmt(r.elderly||0)}</div>`,
    `<div style="text-align:right;font-weight:bold">${fmt(c)}</div>`
  ];
});
$('vulTable').innerHTML = table(vulHeaders, vulRows);"""

if old_js.replace('\n', ' ') in html:
    html = html.replace(old_js.replace('\n', ' '), new_js.replace('\n', ' '))
    print("Fixed keys")
else:
    print("Could not find block to fix")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
