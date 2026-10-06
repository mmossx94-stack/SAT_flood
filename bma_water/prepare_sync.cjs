// Run extract_bma.ps1 -Refresh first. Produces the exact Apps Script schema.
const fs=require('fs'),path=require('path'),vm=require('vm');
const dir=__dirname;
const context=vm.createContext({Utilities:{formatDate:d=>new Date(d.getTime()+7*3600000).toISOString().slice(0,19)}});
vm.runInContext(fs.readFileSync(path.join(dir,'Disater_BKK_DB.gs'),'utf8'),context);
context.html=fs.readFileSync(path.join(dir,'source_summary.html'),'utf8');
context.received=fs.statSync(path.join(dir,'source_summary.html')).mtime.toISOString();
const data=vm.runInContext(`({headers:BKK_HEADERS,rows:bkkBuildRows_(bkkExtractArray_(html,'waterSummaryList'),bkkExtractArray_(html,'districtList'),new Date(received))})`,context);
fs.writeFileSync(path.join(dir,'sync_values.json'),JSON.stringify([data.headers,...data.rows]));
console.log(JSON.stringify({rows:data.rows.length,columns:data.headers.length,received:context.received}));
