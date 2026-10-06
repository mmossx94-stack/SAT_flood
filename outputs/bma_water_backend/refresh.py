import argparse, csv, json, re, urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
TH = timezone(timedelta(hours=7))
URL = 'https://weather.bangkok.go.th/water/PageMap/GoogleMap'
# National district codes use a different order from DDS internal district IDs.
OFFICIAL = dict(zip('พระนคร,ดุสิต,หนองจอก,บางรัก,บางเขน,บางกะปิ,ปทุมวัน,ป้อมปราบศัตรูพ่าย,พระโขนง,มีนบุรี,ลาดกระบัง,ยานนาวา,สัมพันธวงศ์,พญาไท,ธนบุรี,บางกอกใหญ่,ห้วยขวาง,คลองสาน,ตลิ่งชัน,บางกอกน้อย,บางขุนเทียน,ภาษีเจริญ,หนองแขม,ราษฎร์บูรณะ,บางพลัด,ดินแดง,บึงกุ่ม,สาทร,บางซื่อ,จตุจักร,บางคอแหลม,ประเวศ,คลองเตย,สวนหลวง,จอมทอง,ดอนเมือง,ราชเทวี,ลาดพร้าว,วัฒนา,บางแค,หลักสี่,สายไหม,คันนายาว,สะพานสูง,วังทองหลาง,คลองสามวา,บางนา,ทวีวัฒนา,ทุ่งครุ,บางบอน'.split(','), (str(1000+i) for i in range(1,51))))
COLORS = {'normal':'#24b295','warning':'#f4b05b','critical':'#e85965','unknown':'#676b6b'}
LEVEL = {'ปกติ':1,'เตือนภัย':2,'วิกฤต':3,'วิกฤติ':3}
STATUS = {1:'normal',2:'warning',3:'critical',0:'unknown'}
def fetch(url, post=False):
    req = urllib.request.Request(url, data=b'payload=TEST_DATA_GOES_HERE' if post else None, headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'})
    with urllib.request.urlopen(req, timeout=45) as response:
        body = response.read().decode('utf-8-sig')
        return body

def write_json(folder, name, data):
    (folder/name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
def write_csv(folder, name, rows):
    if not rows: return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (folder/name).open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
def parse_time(row):
    text=row.get('site_timestampTH')
    if not text: return None
    try:
        date, time = text.split(); day,month,year=map(int,date.split('/'))
        hour,minute=map(int,time.split(':')[:2]); year=year-543 if year>2400 else year
        return datetime(year,month,day,hour,minute,tzinfo=TH)
    except (ValueError,TypeError): return None

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--stale-minutes',type=int,default=15); args=parser.parse_args()
    if args.stale_minutes<=0: raise ValueError('stale-minutes must be positive')
    raw=json.loads(fetch(URL,True))
    if not isinstance(raw,list) or not raw: raise ValueError('Expected non-empty JSON array; previous snapshots preserved')
    now=datetime.now(timezone.utc)
    folder=Path(__file__).parent/('snapshot_'+now.strftime('%Y%m%dT%H%M%S_%fZ')); folder.mkdir()
    write_json(folder,'stations_raw.json',raw); write_csv(folder,'stations_raw.csv',raw)
    normalized=[]
    for row in raw:
        observed=parse_time(row); age=(now-observed).total_seconds()/60 if observed else None
        status=row.get('txtStatus'); rank=LEVEL.get(status,0)
        usable = rank>0 and age is not None and 0<=age<=args.stale_minutes
        reason='usable' if usable else ('sensor_fault_or_unknown_status' if rank==0 else 'missing_time' if age is None else 'future_timestamp' if age<0 else 'stale')
        normalized.append({'station_id':row.get('water_id'),'station_code':row.get('water_code'),'station_name':row.get('water_name'),'source_district_id':row.get('district_id'),'district_name':row.get('district_name'),'district_code':OFFICIAL.get(row.get('district_name')),'latitude':row.get('latitude'),'longitude':row.get('longitude'),'observed_at_source':row.get('site_timestamp'),'observed_at_th_source':row.get('site_timestampTH'),'observed_at_interpreted':observed.isoformat() if observed else None,'age_minutes':round(age,2) if age is not None else None,'source_status':status,'source_color':row.get('colorStatus'),'wl_in':row.get('wl_in'),'wl_out01':row.get('wl_out01'),'wl_out02':row.get('wl_out02'),'warning':row.get('warning'),'critical':row.get('critical'),'usable_for_district_color':usable,'quality_reason':reason,'severity':rank if usable else 0,'fetched_at_utc':now.isoformat()})
    districts=[]
    for name,code in OFFICIAL.items():
        rows=[r for r in normalized if r['district_name']==name]; good=[r for r in rows if r['usable_for_district_color']]
        rank=max((r['severity'] for r in good),default=0); status=STATUS[rank]
        districts.append({'district_code':code,'district_name':name,'source_district_ids':sorted(set(r['source_district_id'] for r in rows if r['source_district_id'] is not None)),'status':status,'color':COLORS[status],'station_count':len(rows),'usable_station_count':len(good),'excluded_station_count':len(rows)-len(good),'normal_count':sum(r['severity']==1 for r in good),'warning_count':sum(r['severity']==2 for r in good),'critical_count':sum(r['severity']==3 for r in good),'partial_data':bool(rows) and len(good)<len(rows),'coverage':'no_station' if not rows else 'no_usable_data' if not good else 'partial' if len(good)<len(rows) else 'complete','trigger_station_codes':[r['station_code'] for r in good if r['severity']==rank],'latest_observed_at':max((r['observed_at_interpreted'] for r in good),default=None),'fetched_at_utc':now.isoformat()})
    write_json(folder,'stations_normalized.json',normalized);write_csv(folder,'stations_normalized.csv',normalized)
    write_json(folder,'district_status.json',districts)
    csv_districts=[{**r,'source_district_ids':json.dumps(r['source_district_ids']),'trigger_station_codes':json.dumps(r['trigger_station_codes'])} for r in districts]
    write_csv(folder,'district_status.csv',csv_districts)
    crosswalk=[{'district_code':r['district_code'],'district_name':r['district_name'],'source_district_ids':r['source_district_ids'],'mapping_basis':'Thai district name; verify against target boundary dataset'} for r in districts]
    write_json(folder,'district_crosswalk.json',crosswalk)
    field_types={k:sorted(set(type(r.get(k)).__name__ for r in raw)) for k in set().union(*(r.keys() for r in raw))}
    write_json(folder,'raw_field_inventory.json',field_types)
    errors=[]
    for filename,url in [('water_summary_source.html','https://weather.bangkok.go.th/water/summary'),('pump_registry_response.json','https://data.bangkok.go.th/api/3/action/datastore_search?resource_id=0a30a58c-213f-4aec-bf16-7dd7f61fb5fd&limit=1000')]:
        try:
            body=fetch(url);(folder/filename).write_text(body,encoding='utf-8')
            if filename.endswith('.json'):
                pump=json.loads(body)
                if pump.get('success') is not True: raise ValueError('Registry success is not true')
                write_json(folder,'pump_registry_records.json',pump['result']['records'])
            else:
                for variable in ('waterSummaryList','districtList'):
                    match=re.search(r'const\s+'+variable+r'\s*=\s*(\[.*?\]);',body,re.S)
                    if match: write_json(folder,variable+'_raw.json',json.loads(match.group(1)))
        except Exception as exc: errors.append({'source':url,'error':str(exc)})
    metadata={'source_url':URL,'method':'POST','form_body':{'payload':'TEST_DATA_GOES_HERE'},'fetched_at_utc':now.isoformat(),'fetched_at_th':now.astimezone(TH).isoformat(),'station_count':len(raw),'unique_station_ids':len(set(r.get('water_id') for r in raw)),'district_count':len(districts),'district_status_counts':dict(Counter(r['status'] for r in districts)),'source_status_counts':dict(Counter(r.get('txtStatus') for r in raw)),'quality_counts':dict(Counter(r['quality_reason'] for r in normalized)),'outside_bangkok_stations':sum(r['district_code'] is None for r in normalized),'stale_minutes_policy':args.stale_minutes,'timestamp_policy':'Use site_timestampTH Buddhist year as UTC+07. Preserve raw site_timestamp. Do not assume Z agrees with TH field.','aggregation_policy':'Highest source alert among usable stations; operational custom policy, not official district alert.','optional_source_errors':errors}
    write_json(folder,'metadata.json',metadata)
    print(json.dumps({'folder':str(folder),**metadata},ensure_ascii=True))
if __name__=='__main__': main()