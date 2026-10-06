with open('outputs/flood_web/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_bkk = """                try: item['province'] = json.loads(row['raw_station_json'])['geocode']['province_name']['th']
                except (TypeError, ValueError, KeyError):
                    raise ValueError('ข้อมูลจังหวัดใน BKK_water_DB ไม่ครบ')"""

new_bkk = """                try: item['province'] = json.loads(row['raw_station_json']).get('geocode', {}).get('province_name', {}).get('th', 'กรุงเทพมหานคร')
                except (TypeError, ValueError, KeyError):
                    item['province'] = 'กรุงเทพมหานคร'"""

content = content.replace(old_bkk, new_bkk)

with open('outputs/flood_web/server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed BKK geocode error")
