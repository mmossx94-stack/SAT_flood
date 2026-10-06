import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_js = """   const vGroups = [
     { key: 'เด็ก 0-4 ปี', val: sum(vBkk, 'children'), color: '#3b82f6' },
     { key: 'หญิงตั้งครรภ์', val: val = sum(vBkk, 'pregnant'), color: '#f59e0b' },
     { key: 'ผู้สูงอายุ 60 ปีขึ้นไป', val: sum(vBkk, 'elderly'), color: '#10b981' }
   ].filter(g => g.val > 0);
   
   if (window.vulChartInstance) { window.vulChartInstance.destroy(); }
   const ctx = document.getElementById('vulChart');
   if (ctx && vGroups.length > 0) {
     $('vulChartEmpty').classList.add('hidden');
     window.vulChartInstance = new Chart(ctx, {
       type: 'doughnut',
       data: {
         labels: vGroups.map(g => g.key),
         datasets: [{ data: vGroups.map(g => g.val), backgroundColor: vGroups.map(g => g.color), borderWidth: 1, borderColor: '#ffffff' }]
       },
       options: {
         responsive: true, maintainAspectRatio: false, cutout: '60%',
         plugins: {
           legend: { position: 'right', labels: { boxWidth: 12, font: { family: "'IBM Plex Sans Thai', sans-serif", size: 12 } } },
           tooltip: { titleFont: { family: "'IBM Plex Sans Thai', sans-serif" }, bodyFont: { family: "'IBM Plex Sans Thai', sans-serif" } }
         }
       }
     });
   } else if (ctx) {"""

new_js = """   const vGroups = [
     { key: 'เด็ก 0-4 ปี', val: sum(vBkk, 'children'), color: '#3b82f6' },
     { key: 'หญิงตั้งครรภ์', val: sum(vBkk, 'pregnant'), color: '#f59e0b' },
     { key: 'ผู้สูงอายุ 60 ปีขึ้นไป', val: sum(vBkk, 'elderly'), color: '#10b981' }
   ].filter(g => g.val > 0);
   
   if (window.vulChartInstance) { window.vulChartInstance.destroy(); }
   const ctx = document.getElementById('vulChart');
   if (ctx && vGroups.length > 0) {
     $('vulChartEmpty').classList.add('hidden');
     window.vulChartInstance = new Chart(ctx, {
       type: 'doughnut',
       data: {
         labels: vGroups.map(g => `${g.key} (${fmt(g.val)} คน)`),
         datasets: [{ data: vGroups.map(g => g.val), backgroundColor: vGroups.map(g => g.color), borderWidth: 1, borderColor: '#ffffff' }]
       },
       options: {
         responsive: true, maintainAspectRatio: false, cutout: '65%',
         plugins: {
           legend: { position: 'right', labels: { boxWidth: 12, font: { family: "'IBM Plex Sans Thai', sans-serif", size: 13 } } },
           tooltip: { titleFont: { family: "'IBM Plex Sans Thai', sans-serif" }, bodyFont: { family: "'IBM Plex Sans Thai', sans-serif" } }
         }
       },
       plugins: [{
         id: 'centerText',
         beforeDraw: function(chart) {
           const cx = chart.ctx;
           const width = chart.chartArea.right - chart.chartArea.left;
           const height = chart.chartArea.bottom - chart.chartArea.top;
           cx.restore();
           const total = chart.config.data.datasets[0].data.reduce((a, b) => a + b, 0);
           const totalStr = fmt(total);
           cx.textBaseline = "middle";
           cx.fillStyle = "#334155";
           cx.font = "bold 24px 'IBM Plex Sans Thai', sans-serif";
           const textX = chart.chartArea.left + (width - cx.measureText(totalStr).width) / 2;
           const textY = chart.chartArea.top + (height / 2) - 8;
           cx.fillText(totalStr, textX, textY);
           cx.fillStyle = "#64748b";
           cx.font = "12px 'IBM Plex Sans Thai', sans-serif";
           const subText = "รวม (คน)";
           const subTextX = chart.chartArea.left + (width - cx.measureText(subText).width) / 2;
           cx.fillText(subText, subTextX, textY + 22);
           cx.save();
         }
       }]
     });
   } else if (ctx) {"""

if old_js in html:
    html = html.replace(old_js, new_js)
    print("Successfully added chart totals logic!")
else:
    print("Could not find chart JS block!")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
