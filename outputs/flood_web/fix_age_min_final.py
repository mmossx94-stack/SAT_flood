import sys, re
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

pattern = r"function ageMinutes\(r\)\{.*?\n const source=r\.observed_at_th\|\|r\.updated_at_source;\n return \(timestamp\(r\.fetched_at_th\)-timestamp\(source\)\)/60000\}"

new_code = """function ageMinutes(r){
  const source = r.Ingested_At || r.updated_at_source || r.observed_at_th || r.fetched_at_th;
  if (!source) return NaN;
  const t = timestamp(source);
  return t ? (timestamp(DATA.loadedAt) - t) / 60000 : NaN;
}"""

match = re.search(pattern, html, flags=re.DOTALL)
if match:
    html = html.replace(match.group(0), new_code)
    print("Fixed ageMinutes")
else:
    print("Could not find ageMinutes")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
