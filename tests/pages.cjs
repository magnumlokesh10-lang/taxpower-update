// Static checks for the built pages. Run: node tests/pages.cjs (no packages needed).
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const read=p=>fs.readFileSync(p,'utf8');
const routes=JSON.parse(read('scripts/seo-routes.json'));
const navFor={home:'index.html',taxpowergst:'taxpowergst.html',taxpowertds:'taxpowertds.html',pricing:'pricing.html',downloads:'downloads.html',aboutus:'aboutus.html',support:'support.html'};
let checked=0;
for(const [route,meta] of Object.entries(routes)){
  const html=read(route+'.html');
  assert.equal(html,read(route+'/index.html'),route+': slash and .html versions must match');
  assert.ok(html.includes('<title>'+meta.title.replace(/&/g,'&amp;')+'</title>'),route+': title');
  assert.equal((html.match(/<h1[\s>]/g)||[]).length,1,route+': exactly one h1');
  assert.ok(html.includes('rel="canonical" href="https://taxpower.co/'+(meta.canonical||route)+'"'),route+': canonical');
  assert.ok(html.includes(meta.description.replace(/&/g,'&amp;')),route+': description');
  assert.ok(!/section-routes|page-loader|nav-loader|data-page-sections|loaded-page-section/.test(html),route+': no one-page leftovers');
  assert.equal((html.match(/<(main|section)[^>]*data-route-section/g)||[]).length>=1,true,route+': has page content');
  assert.equal((html.match(/id="(home|taxpowergst|taxpowertds|pricing|downloads|aboutus|support)"[^>]*data-route-section/g)||[]).length,1,route+': carries only its own page, not the whole site');
  const cur=html.match(/<a[^>]*class="[^"]*nav-item[^"]*h-current[^"]*"[^>]*>/g)||[];
  assert.equal(cur.length,1,route+': one active nav item');
  assert.ok(cur[0].includes('data-nav-page="'+navFor[meta.section]+'"'),route+': active nav matches page');
  for(const m of html.matchAll(/(?:src|href)="((?:css|js|asset)\/[^"?#]+)/g)){
    assert.ok(fs.existsSync(decodeURIComponent(m[1])),route+': missing file '+m[1]);
  }
  checked++;
}
console.log('PASS: '+checked+' separate pages - metadata, single h1, own content only, active tab, all local files exist.');
