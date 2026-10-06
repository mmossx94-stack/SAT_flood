const {chromium}=require('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict');
(async()=>{
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8765',{waitUntil:'networkidle'});
async function cards(){return page.locator('#cards .number').allTextContents()}
let c=await cards();console.log('National',c);assert.match(c[0],/31/);assert.match(c[1],/1,177,404/);
assert.match(await page.locator('#mapCount').textContent(),/804/);
await page.selectOption('#reportDate','2026-09-30');c=await cards();assert.match(c[0],/32/);assert.match(c[1],/1,041,307/);
await page.selectOption('#reportDate','2026-10-01');await page.selectOption('#province','กรุงเทพมหานคร');c=await cards();assert.match(c[0],/1/);assert.match(c[1],/329,000/);
await page.click('#reset');await page.screenshot({path:'outputs/flood_web/national.png',fullPage:false});
await page.click('#tab-bkk');c=await cards();console.log('BKK',c);assert.match(c[0],/329,000/);assert.match(c[1],/272/);assert.match(c[2],/4,449/);assert.match(c[3],/11,611/);assert.equal(await page.locator('#areaTable tbody tr').count(),50);
await page.screenshot({path:'outputs/flood_web/bkk.png',fullPage:false});
await page.selectOption('#district','คลองสามวา');console.log('District',await cards());assert.equal(await page.locator('#areaTable tbody tr').count(),1);assert.ok((await page.locator('#shelterTable').textContent()).includes('ผู้พักเกินความจุ'));
await page.fill('#search','ไม่มีสถานีชื่อนี้');assert.ok((await page.locator('#stationTable').textContent()).includes('ไม่มีข้อมูล'));
await page.click('#reset');await page.click('#methodBtn');assert.ok(await page.locator('#methods').isVisible());await page.click('#closeMethods');
const downloadPromise=page.waitForEvent('download');await page.click('#export');const download=await downloadPromise;console.log('Download',download.suggestedFilename());
await page.setViewportSize({width:390,height:844});await page.screenshot({path:'outputs/flood_web/mobile.png',fullPage:false});
await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:'outputs/flood_web/mobile-top.png',fullPage:false});
console.log('Mobile dimensions',await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth})));assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
assert.deepEqual(errors,[]);console.log('PASS: dates, provinces, BKK totals, district filter, empty state, modal, export, mobile overflow, JS errors');
const offline=await browser.newPage();await offline.route(/^https?:/,route=>route.abort());await offline.goto('file:///C:/Users/admin/OneDrive/'+encodeURIComponent('กลุ่มพยากรณ์สุขภาพ')+'/'+encodeURIComponent('2569_น้ำท่วม')+'/SAT/outputs/flood_web/index.html');assert.match(await offline.locator('#cards').textContent(),/1,177,404/);await offline.click('#tab-bkk');assert.match(await offline.locator('#cards').textContent(),/329,000/);console.log('PASS: direct local HTML and core controls without internet');
await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
