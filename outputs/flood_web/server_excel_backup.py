from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime, timezone
import json
import openpyxl
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parents[1] / 'ปภ' / 'รายงานสถานการณ์สาธารณภัยรายจังหวัด.xlsx'
def read_data(path=SOURCE):
    with path.open('rb') as stream:
        w = openpyxl.load_workbook(stream, read_only=True, data_only=True)
        raw = {}
        try:
            for name in ['Disaster_DB','Vulnerable_group','thai_water_DB','BKK_water_DB','shelter_DB']:
                rows = w[name].iter_rows(values_only=True)
                headers = next(rows)
                raw[name] = [dict(zip(headers,r)) for r in rows if any(x is not None for x in r)]
        finally:
            w.close()
    def pick(r,keys): return {k:r.get(k) for k in keys.split()}
    def stations(rows,bkk=False):
        result=[]
        for r in rows:
            item=pick(r,'station_id station_name district_or_area latitude longitude observed_at_th water_in_m_msl warning_in_source critical_in_source flood_status_source age_minutes_at_fetch fetched_at_th source_url')
            item['province']=json.loads(r['raw_station_json'])['geocode']['province_name']['th'] if bkk else r['district_or_area']
            result.append(item)
        return result
    return dict(source=path.name,loadedAt=datetime.now(timezone.utc).isoformat(),sourceModifiedAt=datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat(),
        disasters=[pick(r,'Record_ID Report_Date Ingested_At Region Province Disaster_Type Affected_Districts_Count Affected_Households Casualties_Deaths Water_Level_Trend Current_Status Source_URL') for r in raw['Disaster_DB']],
        vulnerable=[dict(province=r['จังหวัด'],region=r['เขตสุขภาพ'],children=r['จำนวนเด็ก 0-4 ปีทั้งหมด (คน)'],pregnant=r['จำนวนหญิงตั้งครรภ์ทั้งหมด (คน)'],elderly=r['จำนวนผู้สูงอายุ 60 ปีขึ้นไปทั้งหมด (คน)']) for r in raw['Vulnerable_group'] if r.get('จังหวัด')],
        stations=stations(raw['thai_water_DB']),bkkStations=stations(raw['BKK_water_DB'],True),
        shelters=[pick(r,'shelter_id district shelter_name capacity occupied available status_source latitude longitude updated_at_source fetched_at_th source_url map_url') for r in raw['shelter_DB']])
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def end_headers(self):
        self.send_header('Cache-Control','no-store, max-age=0')
        super().end_headers()
    def do_GET(self):
        route=self.path.split('?')[0]
        if route=='/api/data':
            try:
                body=json.dumps(read_data(),ensure_ascii=False,default=lambda v:v.isoformat(),allow_nan=False).encode('utf-8')
                self.send_response(200)
            except Exception as exc:
                print('Excel read failed:',repr(exc),flush=True)
                body=json.dumps({'error':'อ่าน Excel ไม่สำเร็จ กรุณาบันทึกและปิดไฟล์แล้วลองใหม่'},ensure_ascii=False).encode('utf-8')
                self.send_response(503)
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Content-Length',str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif route in ('/','/index.html', '/thai_provinces.json'):
            if route == '/': self.path = '/index.html'
            super().do_GET()
        else: self.send_error(404)
if __name__=='__main__':
    print('http://127.0.0.1:8765/ Excel: '+str(SOURCE),flush=True)
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
