import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# Remove the appended code at the very end
js = js.split("let bkkVulChartInstance = null;")[0]

# Insert it right before the last }catch(error){
vul_code = """
let bkkVulChartInstance = null;
function renderBkkVulChart() {
    if (state.tab !== 'bkk') return;
    const bkkReports = getReports().filter(r => r.Province === 'กรุงเทพมหานคร');
    const households = bkkReports.length ? sum(bkkReports, 'Affected_Households') : null;
    $('bkkAffectedHouseholds').textContent = households !== null ? fmt(households) : '-';
    
    const vulData = DATA.vulnerable.filter(r => r.province === 'กรุงเทพมหานคร' && (!state.district || String(r.district||'').replace(/^เขต/,'').trim() === state.district));
    
    if (!vulData.length || failed('Vulnerable_group')) {
        $('vulChartEmpty').classList.remove('hidden');
        if (bkkVulChartInstance) { bkkVulChartInstance.destroy(); bkkVulChartInstance = null; }
        return;
    }
    $('vulChartEmpty').classList.add('hidden');
    
    const groups = ['ผู้สูงอายุ', 'ผู้ป่วยติดเตียง', 'หญิงตั้งครรภ์', 'เด็กเล็ก'];
    const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b'];
    const sums = groups.map(g => sum(vulData, g));
    
    if (bkkVulChartInstance) {
        bkkVulChartInstance.data.datasets[0].data = sums;
        bkkVulChartInstance.update();
    } else {
        const ctx = document.getElementById('vulChart').getContext('2d');
        bkkVulChartInstance = new window.Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: groups,
                datasets: [{
                    data: sums,
                    backgroundColor: colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right', labels: { boxWidth: 12, font: { size: 11 } } },
                    tooltip: { callbacks: { label: (ctx) => ' ' + ctx.label + ': ' + fmt(ctx.raw) + ' คน' } }
                }
            }
        });
    }
}

function renderVulnerable() {
    if (state.tab === 'bkk') return;
    if (failed('Vulnerable_group')) return;
    const allowed = allowedProvinces();
    const rows = DATA.vulnerable.filter(r => allowed.includes(r.province));
    const grouped = new Map();
    for (const r of rows) {
        if (!grouped.has(r.province)) grouped.set(r.province, { province: r.province, region: r.region });
        const obj = grouped.get(r.province);
        for (const k of ['ผู้สูงอายุ', 'ผู้ป่วยติดเตียง', 'หญิงตั้งครรภ์', 'เด็กเล็ก']) {
            obj[k] = (obj[k] || 0) + (r[k] || 0);
        }
    }
    const finalRows = Array.from(grouped.values()).sort((a,b) => (b['ผู้สูงอายุ']||0) - (a['ผู้สูงอายุ']||0));
    const headers = ['จังหวัด', 'เขตสุขภาพ', 'ผู้สูงอายุ', 'ผู้ป่วยติดเตียง', 'หญิงตั้งครรภ์', 'เด็กเล็ก'];
    $('vulTable').innerHTML = table(headers, finalRows.map(r => [
        `<button class="linkbutton" data-province="${esc(r.province)}">${esc(r.province)}</button>`,
        esc(r.region),
        fmt(r['ผู้สูงอายุ']),
        fmt(r['ผู้ป่วยติดเตียง']),
        fmt(r['หญิงตั้งครรภ์']),
        fmt(r['เด็กเล็ก'])
    ]));
}
"""

js = js.replace("}catch(error){document.getElementById('pageTitle')", vul_code + "\n}catch(error){document.getElementById('pageTitle')")

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
