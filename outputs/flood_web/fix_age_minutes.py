import sys, re
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# We need to replace the entire ageMinutes function
pattern = r"const timestamp=(.*?)(?=const STALE)"
match = re.search(pattern, html, flags=re.DOTALL)
if match:
    old_code = match.group(0)
    new_code = """const timestamp=t=>t?new Date(t).getTime():NaN;
const ageMinutes=r=>{
  const source = r.Ingested_At || r.updated_at_source || r.observed_at_th || r.fetched_at_th;
  if (!source) return NaN;
  const t = timestamp(source);
  return t ? (timestamp(DATA.loadedAt) - t) / 60000 : NaN;
};
"""
    html = html.replace(old_code, new_code.replace('\n', ' '))
    print("Fixed ageMinutes function")
else:
    print("Could not find ageMinutes function")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
