import urllib.request
import re
try:
    req = urllib.request.Request('https://docs.google.com/spreadsheets/d/1RQDU83exQhNpVYjp9JyD5UdocA6JB6GpJeXA-Qe8Pr4/htmlview')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        print("BKK_water_DB in html?", 'BKK_water_DB' in html)
        print("Config in html?", 'Config' in html)
        print("Status in html?", 'Status' in html)
        # Find all sheet names in the javascript payload config
        match = re.search(r'var _view = (\{.*?\});', html)
        if match:
            print("Found _view")
        else:
            match2 = re.search(r'var bootstrapData = (\{.*?\});', html)
            print("Found bootstrapData?", match2 is not None)
except Exception as e:
    print('Failed:', e)
