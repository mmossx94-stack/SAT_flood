import json,re
from pathlib import Path
from pyproj import Transformer
p=Path(__file__).parent
rows=json.loads((p/'shelter_live.json').read_text(encoding='utf8'))
schools=json.loads((p/'bma_school.json').read_text(encoding='utf8'))
t=Transformer.from_crs('EPSG:32647','EPSG:4326',always_xy=True)
def norm(s):return re.sub(r'[\s()\u200b]','',s)
def base(s):return norm(re.sub(r'\([^)]*\)','',s))
out=[]
for r in rows:
 if r['geo'][0]!='':continue
 matches=[f for f in schools['features'] if base(f['properties']['name'])==base(r['name']) and ('เขต'+r['district']) in f['properties']['address']]
 if len(matches)==1:
  f=matches[0];lon,lat=t.transform(*f['geometry']['coordinates']);out.append(dict(r,lat=round(lat,7),lng=round(lon,7),evidence=f['properties'],source='https://data.go.th/dataset/939e0c80-70df-42c8-84b3-1fc82f2a7f10/resource/b8528c71-7688-4192-8b39-c3a50132213c/download/bma_school.json',method='ข้อมูล GIS โรงเรียน กทม. (ชุดข้อมูลเดิมปี 2558): ชื่อและเขตตรงกัน'))
(p/'shelter_findings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('Matched',len(out));print('Remaining',[(r['row'],r['name'],r['district']) for r in rows if r['geo'][0]=='' and r['id'] not in {x['id'] for x in out}])
