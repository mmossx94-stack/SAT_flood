import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace:
# else{$('sideTitle').textContent='พื้นที่มีครัวเรือนได้รับผลกระทบสูง';$('sideSub').textContent='ทุกอันดับตามรายงานในขอบเขตที่เลือก · หน่วย: ครัวเรือน';$('sideBody').innerHTML=bars(reports.slice().sort((a,b)=>b.Affected_Households-a.Affected_Households).map(r=>({name:r.Province,value:r.Affected_Households})));}
# with new table logic

old_code = "else{$('sideTitle').textContent='พื้นที่มีครัวเรือนได้รับผลกระทบสูง';$('sideSub').textContent='ทุกอันดับตามรายงานในขอบเขตที่เลือก · หน่วย: ครัวเรือน';$('sideBody').innerHTML=bars(reports.slice().sort((a,b)=>b.Affected_Households-a.Affected_Households).map(r=>({name:r.Province,value:r.Affected_Households})));}"

new_code = r"""else{
  $('sideTitle').textContent='ตารางสรุปผลกระทบ ปภ.';
  $('sideSub').textContent='จัดอันดับตามจำนวนครัวเรือนเดือดร้อน';
  const h=['จังหวัด','อำเภอ','ตำบล','ครัวเรือน','เสียชีวิต','แนวโน้ม'];
  const r=reports.slice().sort((a,b)=>(b.Affected_Households||0)-(a.Affected_Households||0));
  const t=`<div style="overflow-x:auto; padding-bottom:8px;"><table style="width:100%; white-space:nowrap; text-align:left; border-collapse:collapse; font-size:13px;">
    <thead><tr style="border-bottom:2px solid #dce6e8; color:#627880;">${h.map((x,i)=>`<th style="padding:8px 4px;${i>=2&&i<=4?'text-align:right':''}">${x}</th>`).join('')}</tr></thead>
    <tbody>${r.map(x=>`<tr style="border-bottom:1px solid #eff4f5;">
      <td style="padding:8px 4px;font-weight:600;"><button class="linkbutton" data-province="${esc(x.Province)}">${esc(x.Province)}</button></td>
      <td style="padding:8px 4px;max-width:120px;overflow:hidden;text-overflow:ellipsis;" title="${esc(x.District_Names||x.Affected_Districts_Count||'-')}">${esc(x.District_Names||x.Affected_Districts_Count||'-')}</td>
      <td style="padding:8px 4px;text-align:right">${esc(x.Affected_Subdistricts_Count||'-')}</td>
      <td style="padding:8px 4px;text-align:right;font-weight:600;color:#991b1b;">${fmt(x.Affected_Households)}</td>
      <td style="padding:8px 4px;text-align:right">${fmt(x.Casualties_Deaths)}</td>
      <td style="padding:8px 4px;">${badge(x.Water_Level_Trend,x.Water_Level_Trend==='เพิ่มขึ้น'?'warn':x.Water_Level_Trend==='ลดลง'?'good':'')}</td>
    </tr>`).join('')}</tbody>
  </table></div>`;
  $('sideBody').innerHTML=t;
}"""

if old_code in html:
    html = html.replace(old_code, new_code.replace('\n', ''))
    print("Updated right side bar chart to table")
else:
    print("Could not find the old bar chart code block")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
