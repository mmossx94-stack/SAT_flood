import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# Fix BKK Vul Chart
old_bkk = """
    const groups = ['ผู้สูงอายุ', 'ผู้ป่วยติดเตียง', 'หญิงตั้งครรภ์', 'เด็กเล็ก'];
    const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b'];
    const sums = groups.map(g => sum(vulData, g));
"""
new_bkk = """
    const groups = ['ผู้สูงอายุ', 'หญิงตั้งครรภ์', 'เด็กเล็ก'];
    const colors = ['#3b82f6', '#10b981', '#f59e0b'];
    const sums = [sum(vulData, 'elderly'), sum(vulData, 'pregnant'), sum(vulData, 'children')];
    if (sums.every(x => !x)) {
        $('vulChartEmpty').classList.remove('hidden');
        if (bkkVulChartInstance) { bkkVulChartInstance.destroy(); bkkVulChartInstance = null; }
        return;
    }
"""
js = js.replace(old_bkk.strip(), new_bkk.strip())

# Fix National Vul Table
old_nat = """
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
"""
new_nat = """
        for (const k of ['elderly', 'pregnant', 'children']) {
            obj[k] = (obj[k] || 0) + (r[k] || 0);
        }
    }
    const finalRows = Array.from(grouped.values()).sort((a,b) => (b.elderly||0) - (a.elderly||0));
    const headers = ['จังหวัด', 'เขตสุขภาพ', 'ผู้สูงอายุ', 'หญิงตั้งครรภ์', 'เด็กเล็ก'];
    $('vulTable').innerHTML = table(headers, finalRows.map(r => [
        `<button class="linkbutton" data-province="${esc(r.province)}">${esc(r.province)}</button>`,
        esc(r.region),
        fmt(r.elderly),
        fmt(r.pregnant),
        fmt(r.children)
    ]));
"""
js = js.replace(old_nat.strip(), new_nat.strip())

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
