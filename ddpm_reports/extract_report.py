import csv,json,re,pathlib,datetime
p=pathlib.Path(__file__).parent
raw=json.loads((p/'tables_raw.json').read_text(encoding='utf-8'))
old=json.loads((p/'Disaster_DB_before_2026-10-01.json').read_text(encoding='utf-8'))['values']
source='https://backofficeminisite.disaster.go.th/apiv1/apps/minisite_directing/194/content/8728/download?filename=5d20575fa6cbe9d1e5a046aeef36e7a3.pdf'
out=[]
def number(x):
    return int(x.replace(',','')) if x and re.fullmatch(r'[\d,]+',x) else (x or '')
for page in raw[:6]:
    for table in page['tables']:
        for r in table:
            if not r[0] or not re.match(r'^\d+\.',r[0]): continue
            n=int(re.match(r'^(\d+)\.',r[0])[1]); prev=old[n]
            assert n==len(out)+1  # Source order and province labels visually verified on pages 1-6.
            trend=next(v for v in r if v and v.startswith('ระดับน้ำ')).replace('ระดับน้ำ','')
            missing=r[21] if page['page']==6 else r[20]
            remark=f"ปภ. รายงาน 545/2569 วันที่ 30 ก.ย. 2569 เวลา 06.00 น. ตารางหน้า {page['page']}; บาดเจ็บ: {r[17] or 'ช่องว่าง'}; สูญหาย: {missing or 'ช่องว่าง'}; คงเครื่องหมาย - และช่องว่างตามต้นฉบับ"
            row=[prev[0],prev[1],prev[2],prev[3],prev[4],number(r[1]),prev[6] if n!=32 else '-',number(r[4]),number(r[7]),number(r[11]),number(r[14]),trend,'กำลังประสบภัย',remark,datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S'),source]
            out.append(row)
assert len(out)==32 and len({r[0] for r in out})==32
(p/'Disaster_DB_2026-09-30_0600.json').write_text(json.dumps([old[0]]+out,ensure_ascii=False,indent=2),encoding='utf-8')
with (p/'Disaster_DB_2026-09-30_0600.csv').open('w',newline='',encoding='utf-8-sig') as f: csv.writer(f).writerows([old[0]]+out)
for entry in raw:
    for i,table in enumerate(entry['tables']):
        with (p/f"table_page_{entry['page']:02}_{i+1}.csv").open('w',newline='',encoding='utf-8-sig') as f: csv.writer(f).writerows(table)
print(json.dumps({'records':len(out),'districts':sum(r[5] for r in out if isinstance(r[5],int)),'subdistricts':sum(r[7] for r in out if isinstance(r[7],int)),'villages':sum(r[8] for r in out if isinstance(r[8],int)),'households':sum(r[9] for r in out if isinstance(r[9],int)),'deaths_numeric':sum(r[10] for r in out if isinstance(r[10],int))},ensure_ascii=False))
