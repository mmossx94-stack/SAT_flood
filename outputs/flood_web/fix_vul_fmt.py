import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = "$('vulnerable').innerHTML=card('จังหวัดที่ประสบภัย',fmt(affectedProvs),'จังหวัด')+[['เด็ก 0-4 ปี',sum(v,'children')],['หญิงตั้งครรภ์',sum(v,'pregnant')],['ผู้สูงอายุ 60 ปีขึ้นไป',sum(v,'elderly')]].map(([t,n])=>card(t,fmt(n),'คน')).join('');"
new_str = "$('vulnerable').innerHTML=card('จังหวัดที่ประสบภัย',affectedProvs,'จังหวัด','')+[['เด็ก 0-4 ปี',sum(v,'children')],['หญิงตั้งครรภ์',sum(v,'pregnant')],['ผู้สูงอายุ 60 ปีขึ้นไป',sum(v,'elderly')]].map(([t,n])=>card(t,n,'คน','')).join('');"

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Fixed fmt calls in card")
else:
    print("Could not find the string")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
