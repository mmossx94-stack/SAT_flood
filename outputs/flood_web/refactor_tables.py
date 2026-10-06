import re

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Fix renderAreas
# Remove tableSort logic
js = re.sub(r"let sortKey = state\.tableSort \|\| 'households';\s*", "", js)
js = re.sub(r"if \(\$\('tableSort'\)\) \$\('tableSort'\)\.value = sortKey;\s*", "", js)
# Simplify the sort block: just sort by households descending as default
# The current sort block is a huge if/else. Let's just replace it.
sort_regex = r"\.sort\(\(a,b\)=>\{.*?return \(b\.r\?\.Affected_Households\|\|0\)-\(a\.r\?\.Affected_Households\|\|0\);\s*\}\);"
js = re.sub(sort_regex, ".sort((a,b) => (b.r?.Affected_Households||0) - (a.r?.Affected_Households||0));", js, flags=re.DOTALL)

# 2. Fix renderStations
# Remove term and status filtering
js = re.sub(r"let term=\$\('search'\)\.value\.trim\(\),status=\$\('statusFilter'\)\.value;", "", js)
# Replace the filter: filter(r=>(!term||...)&&(!status||...)) with just the default array
# wait, the original code is:
# const rows=currentStations.filter(r=>(!term||(r.station_name+' '+r.district_or_area).includes(term))&&(!status||r.flood_status_source===status)).sort((a,b)=>{
js = re.sub(r"const rows=currentStations\.filter\(r=>\(!term.*?===status\)\)\.sort", "const rows=currentStations.sort", js)

# 3. There is a line updating statusFilter options:
# const previous=$('statusFilter').value;opts('statusFilter',uniq(currentStations.map(r=>r.flood_status_source).filter(Boolean)),'ทุกสถานะต้นทาง');if(Array.from($('statusFilter').options).some(o=>o.value===previous))$('statusFilter').value=previous;
js = re.sub(r"const previous=\$\('statusFilter'\)\.value;opts\('statusFilter'.*?\$\('statusFilter'\)\.value=previous;", "", js, flags=re.DOTALL)

# Save dashboard.js
with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove tableSort select
html = re.sub(r'<select id="tableSort".*?</select>', '', html, flags=re.DOTALL)
# Remove any leftover table-tools if any
# We already removed one, let's just make sure
html = re.sub(r'<div class="table-tools">.*?</div>', '', html, flags=re.DOTALL)

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Refactored dashboard.js and template.html to rely on paginateTables")
