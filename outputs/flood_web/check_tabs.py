import urllib.request
import re
try:
    req = urllib.request.Request('https://docs.google.com/spreadsheets/d/1RQDU83exQhNpVYjp9JyD5UdocA6JB6GpJeXA-Qe8Pr4/htmlview')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        # Google sheets htmlview uses ul id="sheet-menu"
        idx = html.find('id="sheet-menu"')
        if idx != -1:
            menu = html[idx:idx+2000]
            tabs = re.findall(r'>([^<]+)</a>', menu)
            print('Tabs in HTML:', tabs)
        else:
            print("Sheet menu not found")
except Exception as e:
    print('Failed:', e)
