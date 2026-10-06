const {chromium}=require('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url'),path=require('node:path'),assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 try{
  const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route(/^https?:/,r=>r.abort());
  await page.goto(pathToFileURL(path.resolve('outputs/flood_web/index.html')).href);
  assert.match(await page.locator('#quality').textContent(),/24 ชั่วโมง/);
  assert.match(await page.locator('#quality').textContent(),/ไม่ทราบเวลาข้อมูล/);
  assert.match(await page.locator('#areaTable').textContent(),/ความสด ณ นำเข้า/);
  await page.click('#tab-bkk');
  assert.match(await page.locator('#shelterTable').textContent(),/ความสด ณ นำเข้า/);
  assert.match(await page.locator('#shelterTable').textContent(),/ข้อมูลเก่าเกิน 24 ชั่วโมง/);
  await page.selectOption('#district','คลองสามวา');
  assert.equal(await page.locator('#areaTable tbody tr').count(),1);
  assert.deepEqual(errors,[]);
  const counts=await page.evaluate(()=>Object.fromEntries(['stations','bkkStations','shelters','disasters','vulnerable'].map(k=>[k,DATA[k].reduce((a,r)=>{const q=quality(r);a[q]=(a[q]||0)+1;return a},{})])));
  console.log('PASS: web renders, national/BKK filters, report/shelter quality, no JS errors.',counts);
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
