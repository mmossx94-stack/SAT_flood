import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# Make renderAreas self-sufficient
js = js.replace("function renderAreas(reports,allowed){", """function renderAreas(){
  const bkk = state.tab === 'bkk';
  const all = getReports();
  const allowed = allowedProvinces();
  const reports = all.filter(r => bkk ? r.Province === 'กรุงเทพมหานคร' : allowed.includes(r.Province));
""")

# Call it in finishRender
bad = "paginateTables();requestAnimationFrame(updateTableHints);"
good = "renderAreas(); paginateTables();requestAnimationFrame(updateTableHints);"
js = js.replace(bad, good)

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
print("Fixed renderAreas!")
