const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const ctx=vm.createContext({console,Utilities:{formatDate:d=>new Date(d.getTime()+7*3600000).toISOString().slice(0,19)}});
vm.runInContext(fs.readFileSync('bma_water/Disater_BKK_DB.gs','utf8'),ctx);
vm.runInContext(fs.readFileSync('bma_water/Shelter.gs','utf8'),ctx);
const html=fs.readFileSync('outputs/flood_web/template.html','utf8');
vm.runInContext(html.slice(html.indexOf('const STALE_MINUTES='),html.indexOf('const badge='))+'\nthis.quality=quality;',ctx);
const fetched=new Date('2026-10-02T12:00:00Z');
for(const [mins,label] of [[0,'ภายใน 24 ชั่วโมง'],[60,'ภายใน 24 ชั่วโมง'],[1440,'ภายใน 24 ชั่วโมง'],[1440+1/60,'ข้อมูลเก่าเกิน 24 ชั่วโมง'],[-1,'เวลาอนาคต']]){
 const observed=new Date(fetched.getTime()-mins*60000).toISOString();
 const row=ctx.bkkBuildRows_([{water_id:1,water_name:'test',wl_in:0,site_timestamp:observed}],[{district_id:1,name:'test'}],fetched)[0];
 assert.equal(row[18],label==='ข้อมูลเก่าเกิน 24 ชั่วโมง'?'ข้อมูลเก่า':label);
 assert(Math.abs(ctx.shelterAgeMinutes_(observed,fetched)-mins)<1e-8);
 assert.equal(ctx.quality({observed_at_th:observed,fetched_at_th:fetched.toISOString()}),label);
 assert.equal(ctx.quality({updated_at_source:observed,fetched_at_th:fetched.toISOString()}),label);
}
assert.equal(ctx.shelterAgeMinutes_('',fetched),'');
assert.equal(ctx.shelterAgeMinutes_('bad',fetched),'');
assert.equal(ctx.quality({}), 'ไม่ทราบเวลาข้อมูล');
assert.equal(ctx.quality({Report_Date:'2026-10-01T00:00:00',Ingested_At:fetched.toISOString()}),'ไม่ทราบเวลาข้อมูล');
assert.equal(ctx.quality({Report_Date:'2026-10-02T18:00:00+07:00',Ingested_At:fetched.toISOString()}),'ภายใน 24 ชั่วโมง');
assert.equal(ctx.quality({observed_at_th:'bad',age_minutes_at_fetch:0,fetched_at_th:fetched.toISOString()}),'ไม่ทราบเวลาข้อมูล');
console.log('PASS: BMA, shelter and web: 0, 60, 1440 minutes; 24h + 1 second; future; missing/invalid time; DDPM unconfirmed midnight; explicit report time.');
