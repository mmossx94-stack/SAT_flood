import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_title = "$('sideTitle').textContent='ความพร้อมศูนย์พักพิง';$('sideSub').textContent=state.district||'ข้อมูล '+uniq(DATA.shelters.map(r=>r.district)).length+' เขต จาก 50 เขต กทม.';"
new_title = "$('sideTitle').textContent='สรุปสถานีระดับน้ำรายเขต';$('sideSub').textContent=state.district||'เรียงตามเขตที่มีสถานีวิกฤตมากที่สุด (24 ชม.)';"

if old_title in html:
    html = html.replace(old_title, new_title)
else:
    print("Could not find old title")
    sys.exit(1)

old_body = """$('sideBody').innerHTML = '<table class="data-table"><thead><tr style="position: sticky; top: 0; background: #f8fafc; z-index: 1;"><th>เขต</th><th>ชื่อศูนย์</th><th>สถานะ</th><th class="num" style="white-space:nowrap">รองรับ (คน)</th></tr></thead><tbody>' + [...currentShelters].sort((a,b)=>{const rank=s=>s==='เต็ม'?1:(s==='ใกล้เต็ม'?2:(s==='เปิดให้บริการ/ว่าง'?3:4));const d=rank(a.status_source)-rank(b.status_source);if(d!==0)return d;return (a.district||'').localeCompare(b.district||'','th')||(a.shelter_name||'').localeCompare(b.shelter_name||'','th')}).map(r => { const st = r.status_source || 'ไม่ทราบ'; const c = st === 'เต็ม' ? '#dc2626' : (st === 'ใกล้เต็ม' ? '#ea580c' : (st === 'เปิดให้บริการ/ว่าง' ? '#16a34a' : '#6b7280')); return `<tr><td>${esc(r.district || '-')}</td><td>${esc(r.shelter_name || '-')}</td><td style="color:${c}; white-space:nowrap; font-weight:500; font-size:12px;">${esc(st)}</td><td class="num">${fmt(r.capacity)}</td></tr>`; }).join('') + (currentShelters.length ? '' : '<tr><td colspan="4" style="text-align:center;color:#666">ไม่มีศูนย์พักพิง</td></tr>') + '</tbody></table>';"""

new_body = """const distStats=new Map();for(const r of currentStations){if(quality(r)!=='ภายใน 24 ชั่วโมง')continue;const d=r.district_or_area||'ไม่ระบุ',st=canonicalWaterStatus(r.flood_status_source);if(!distStats.has(d))distStats.set(d,{วิกฤต:0,เตือนภัย:0,ปกติ:0});const stat=distStats.get(d);if(st==='วิกฤต')stat.วิกฤต++;else if(st==='เตือนภัย')stat.เตือนภัย++;else if(st==='ปกติ')stat.ปกติ++;}const sortedDistricts=Array.from(distStats.entries()).filter(([_,s])=>s.วิกฤต>0||s.เตือนภัย>0||s.ปกติ>0).sort((a,b)=>{if(b[1].วิกฤต!==a[1].วิกฤต)return b[1].วิกฤต-a[1].วิกฤต;if(b[1].เตือนภัย!==a[1].เตือนภัย)return b[1].เตือนภัย-a[1].เตือนภัย;return a[0].localeCompare(b[0],'th');});$('sideBody').innerHTML='<table class="data-table"><thead><tr style="position: sticky; top: 0; background: #f8fafc; z-index: 1;"><th>เขต</th><th class="num" style="color:#dc2626">วิกฤต</th><th class="num" style="color:#ea580c">เตือนภัย</th><th class="num" style="color:#16a34a">ปกติ</th></tr></thead><tbody>'+sortedDistricts.map(([d,s])=>`<tr><td>${esc(d)}</td><td class="num" style="color:${s.วิกฤต?'#dc2626':'#999'}; font-weight:${s.วิกฤต?600:400}">${s.วิกฤต}</td><td class="num" style="color:${s.เตือนภัย?'#ea580c':'#999'}; font-weight:${s.เตือนภัย?600:400}">${s.เตือนภัย}</td><td class="num" style="color:${s.ปกติ?'#16a34a':'#999'}">${s.ปกติ}</td></tr>`).join('')+(sortedDistricts.length?'':'<tr><td colspan="4" style="text-align:center;color:#666">ไม่มีข้อมูลสถานีที่อัปเดตใน 24 ชม.</td></tr>')+'</tbody></table>';"""

if old_body in html:
    html = html.replace(old_body, new_body)
    print("Replaced body!")
else:
    print("Could not find old body")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
