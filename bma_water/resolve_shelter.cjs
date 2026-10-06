const fs=require('fs');
const rows=JSON.parse(fs.readFileSync(__dirname+'/shelter_live.json','utf8'));
async function main(){
 const out=[]; const todo=rows.filter(r=>r.geo[0]==='' && r.url);
 for(let i=0;i<todo.length;i+=6){await Promise.all(todo.slice(i,i+6).map(async r=>{
  try{const res=await fetch(r.url,{signal:AbortSignal.timeout(20000)});const html=await res.text();out.push({...r,finalUrl:res.url,http:res.status});fs.writeFileSync(__dirname+'/map_'+r.row+'.html',html);}catch(e){out.push({...r,error:e.message});}
 })); console.log('resolved',out.length,'/',todo.length);}
 fs.writeFileSync(__dirname+'/shelter_resolved.json',JSON.stringify(out,null,2));
}
main();
