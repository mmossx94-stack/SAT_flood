import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_code = "function ageMinutes(r){\n if('Report_Date' in r){if(!r.Report_Date || /T00:00(?::00(?:\\.0+)?)?(?:Z|[+-]\\d{2}:?\\d{2})?$/.test(r.Report_Date))return NaN;return (timestamp(r.Ingested_At)-timestamp(r.Report_Date))/60000}\n const source=r.observed_at_th||r.updated_at_source;\n return (timestamp(r.fetched_at_th)-timestamp(source))/60000;\n}"

new_code = """function ageMinutes(r){
  const source = r.Ingested_At || r.updated_at_source || r.observed_at_th || r.fetched_at_th;
  if (!source) return NaN;
  const t = timestamp(source);
  return t ? (timestamp(DATA.loadedAt) - t) / 60000 : NaN;
}"""

if old_code in html:
    html = html.replace(old_code, new_code)
    print("Replaced!")
else:
    print("Not found!")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
