import urllib.request
import re
try:
    req = urllib.request.Request('https://docs.google.com/spreadsheets/d/1RQDU83exQhNpVYjp9JyD5UdocA6JB6GpJeXA-Qe8Pr4/htmlview')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        idx = html.find('Config')
        print(html[idx-50:idx+50])
except Exception as e:
    print('Failed:', e)
