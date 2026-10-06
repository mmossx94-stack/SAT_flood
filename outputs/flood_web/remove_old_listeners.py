import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. document.querySelectorAll('.tab').forEach(...)
old_tab = "document.querySelectorAll('.tab').forEach(x=>x.addEventListener('click',()=>{state.tab=x.dataset.tab;$('search').value='';$('statusFilter').value='';render()}));"
new_tab = "document.querySelectorAll('.tab').forEach(x=>x.addEventListener('click',()=>{state.tab=x.dataset.tab;render()}));"
js = js.replace(old_tab, new_tab)

# 2. $('tableSort').addEventListener(...) to $('statusFilter').addEventListener(...)
old_listeners = "$('tableSort').addEventListener('change',e=>{state.tableSort=e.target.value;render()});$('region').addEventListener('change',e=>{state.region=e.target.value;state.province='';opts('province',DATA.vulnerable.filter(r=>!state.region||r.region===state.region).map(r=>r.province).sort((a,b)=>a.localeCompare(b,'th')),'ทุกจังหวัด');render()});$('province').addEventListener('change',e=>{state.province=e.target.value;render()});$('district').addEventListener('change',e=>{state.district=e.target.value;render()});$('search').addEventListener('input',renderStations);$('statusFilter').addEventListener('change',renderStations);"
new_listeners = "$('region').addEventListener('change',e=>{state.region=e.target.value;state.province='';opts('province',DATA.vulnerable.filter(r=>!state.region||r.region===state.region).map(r=>r.province).sort((a,b)=>a.localeCompare(b,'th')),'ทุกจังหวัด');render()});$('province').addEventListener('change',e=>{state.province=e.target.value;render()});$('district').addEventListener('change',e=>{state.district=e.target.value;render()});"
js = js.replace(old_listeners, new_listeners)

# 3. $('reset').addEventListener
old_reset = "$('reset').addEventListener('click',()=>{tableFilters.clear();document.querySelectorAll('[data-table-filters]').forEach(el=>el.remove());state.region='';state.province='';state.district='';$('region').value='';$('district').value='';$('search').value='';$('statusFilter').value='';opts('province',provinceNames(),'ทุกจังหวัด');render()});"
new_reset = "$('reset').addEventListener('click',()=>{tableFilters.clear();document.querySelectorAll('[data-table-filters]').forEach(el=>el.remove());state.region='';state.province='';state.district='';$('region').value='';$('district').value='';opts('province',provinceNames(),'ทุกจังหวัด');render()});"
js = js.replace(old_reset, new_reset)

# 4. $('tableSort').classList.toggle('hidden',bkk);
js = js.replace("$('tableSort').classList.toggle('hidden',bkk);", "")

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
