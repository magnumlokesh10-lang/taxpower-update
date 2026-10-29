"""Build the site as real, separate pages (one HTML file per tab).
Edit _site-source/*.html, footer.html, nav.html and scripts/seo-routes.json;
then run python scripts/build-pages.py (requires lxml and Pillow), then scripts/build-landing-pages.py.
Each page carries only its own content, styles and scripts.
"""
from pathlib import Path
from copy import deepcopy
import json,re,os
from urllib.parse import urlsplit,unquote
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bundle
import related
from lxml import html,etree
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE='https://taxpower.co/'
# Site root for <base href>. '/' on taxpower.co; set TAXPOWER_BASE_PATH=/repo-name/ to preview a GitHub project page.
BASE_PATH='/'+os.environ.get('TAXPOWER_BASE_PATH','/').strip('/')+'/' if os.environ.get('TAXPOWER_BASE_PATH','/').strip('/') else '/'
BUILD=__import__('time').strftime('%Y%m%d-%H%M')
NAV_PAGE={'home':'index.html','taxpowergst':'taxpowergst.html','taxpowertds':'taxpowertds.html','pricing':'pricing.html','downloads':'downloads.html','aboutus':'aboutus.html','support':'support.html'}
PAGE_ANCHOR={'home':'home','demo-enquiry':'demo-enquiry'}
SCROLL_TO={'gst-return':'dashboard_bg','gst-billing':'gst-billing-intro','technical-support':'technical-support','demo-enquiry':'demo-enquiry'}
config=json.loads((ROOT/'scripts/seo-routes.json').read_text())
variants=json.loads((ROOT/'scripts/image-variants.json').read_text())
source=html.fromstring((ROOT/'_site-source/index.html').read_text())
sections={}
for name in ['taxpowergst','taxpowertds','pricing','downloads','aboutus','support']:
    doc=html.fromstring((ROOT/f'_site-source/{name}.html').read_text())
    node=doc.xpath('//main')[0];node.set('id',name)
    node.set('class',node.get('class','')+' loaded-page-section')
    node.set('data-loaded-page',name+'.html');sections[name]=node
container=source.xpath('//*[@data-page-sections]')[0]
for node in sections.values():container.append(deepcopy(node))
head_assets={}
for name in ['taxpowergst','taxpowertds','pricing','downloads','aboutus','support']:
    doc=html.fromstring((ROOT/f'_site-source/{name}.html').read_text())
    head_assets[name]=[(e.tag,(e.get('href') or e.get('src')).split('?')[0]) for e in doc.xpath('//head/link[@rel="stylesheet"][starts-with(@href,"css/")] | //head/script[starts-with(@src,"js/")]')]
head_assets['home']=[('link','css/stylesheet.css'),('link','css/company-logos.css'),('link','css/home-sections.css'),('link','css/support-cards.css'),('script','js/form-backend.js'),('script','js/script.js'),('script','js/count-up.js'),('script','js/support-page.js')]
DROP=('js/section-routes.js','js/nav-loader.js','js/page-loader.js')
# Shared parts are present before JavaScript, so links are immediately crawlable.
navdoc=html.fromstring((ROOT/'nav.html').read_text())
slot=source.xpath('//*[@data-nav-slot]')[0];parent=slot.getparent();pos=parent.index(slot)
for node in navdoc.xpath('//header | //button[@id="backToTop"]'):
    parent.insert(pos,deepcopy(node));pos+=1
parent.remove(slot)
slot=source.xpath('//*[@data-footer-slot]')[0];slot.getparent().replace(slot,html.fromstring((ROOT/'footer.html').read_text()))
head=source.find('head')
for node in head.xpath('./script[@type="application/ld+json"] | ./meta[@property] | ./meta[starts-with(@name,"twitter:")]'):
    head.remove(node)
for name in ['plus-jakarta-sans-latin-400', 'plus-jakarta-sans-latin-700', 'dm-sans-latin-400']:
    head.append(etree.Element('link',{'rel':'preload','href':'fonts/%s-normal.woff2'%name,'as':'font','type':'font/woff2','crossorigin':'anonymous'}))
head.append(etree.Element('meta',{'name':'robots','content':'index, follow, max-image-preview:large'}))
# Preserve existing heading typography independently of semantic heading levels.
for h in source.xpath('//h1'):
    h.set('class',(h.get('class','')+' original-h1').strip());h.set('data-page-heading','true')
# The Magnum card is a peer company heading, not an H3 immediately after H1.
for h in source.xpath('//*[contains(@class,"se-magnum-panel")]/h3'):
    h.tag='h2';h.set('class','magnum-company-heading')
# Normalize navigation to published clean routes, preserving in-page feature anchors.
alias={'index.html':'home','taxpowergst.html':'taxpowergst','taxpowertds.html':'taxpowertds','pricing.html':'pricing','downloads.html':'downloads','aboutus.html':'aboutus','support.html':'support'}
anchors={'home':'home','taxpowergst':'taxpowergst','dashboard_bg':'gst-return','gst-return':'gst-return','gst-billing-intro':'gst-billing','gst-einvoice':'gst-billing','taxpowertds':'taxpowertds','pricing':'pricing','pricing-banner':'pricing','downloads':'downloads','downloads-banner':'downloads','aboutus':'aboutus','support':'support','technical-support':'technical-support','demo-enquiry':'demo-enquiry'}
for a in source.xpath('//a[@href]'):
    u=urlsplit(a.get('href'))
    if u.scheme or u.netloc:continue
    if u.fragment in anchors and (not u.path or u.path in alias):a.set('href',anchors[u.fragment])
    elif u.path in alias and not u.fragment:a.set('href',alias[u.path])
# Serve smaller images at the same intrinsic dimensions; keep decorative alt empty.
for img in source.xpath('//img[@src]'):
    old=img.get('src');path=unquote(old.split('?')[0]);actual=variants.get(path,path)
    if actual!=path:img.set('src',actual)
    file=ROOT/actual
    if file.exists() and file.suffix.lower()!='.svg':
        with Image.open(file) as im:w,h=im.size
        if not img.get('width'):img.set('width',str(w))
        if not img.get('height'):img.set('height',str(h))
    if not img.get('alt') and '/swt_icon/' not in path and '/frms_bg/' not in path:
        if any(folder in path for folder in ['/gst_ss/','/tds_ss/','/billing_ss/']):
            img.set('alt',Path(path).stem.replace('_',' ').replace('taxpowergst','TaxPower GST').replace('taxpowertds','TaxPower TDS'))
    if not img.get('decoding'):img.set('decoding','async')
    if not img.get('fetchpriority') and not img.get('loading'):img.set('loading','lazy')
# Lightweight illustration variants referenced by CSS are updated separately.
for el in source.xpath('//script[@src] | //link[@href]'):
    key='src' if el.tag=='script' else 'href';value=el.get(key)
    if value.startswith(('js/','css/')):el.set(key,value.split('?')[0]+('?v=20261023-office-map' if value.startswith('css/aboutus.css') else '?v=20261023-vidarbha' if value.startswith('css/stylesheet.css') else '?v=20261017-seo'))
source.xpath('//h1[@class="visually-hidden original-h1"]')
organization={'@type':['Organization','LocalBusiness'],'@id':BASE+'#siddharth','name':'Siddharth Enterprises','description':'Authorized TaxPower dealer in Nagpur, Maharashtra selling TaxPower GST, Billing and TDS software across India.','areaServed':{'@type':'Country','name':'India'},'url':BASE+'aboutus','logo':BASE+'asset/swt_icon/siddharth-enterprises-logo.webp','email':'support@taxpower.co','telephone':['+919145073173','+917755912821'],'address':{'@type':'PostalAddress','streetAddress':'Plot No.14, Godawari Apartment, Amar Nagar Road, T-Point Hingna, Hingna MIDC','addressLocality':'Nagpur','addressRegion':'Maharashtra','postalCode':'440016','addressCountry':'IN'}}
for route,meta in config.items():
    doc=deepcopy(source);head=doc.find('head');canonical=BASE+meta.get('canonical',route)
    doc.xpath('//title')[0].text=meta['title']
    doc.xpath('//meta[@name="description"]')[0].set('content',meta['description'])
    doc.xpath('//link[@rel="canonical"]')[0].set('href',canonical)
    for prop,value in {'og:title':meta['title'],'og:description':meta['description'],'og:url':canonical,'og:type':'website','og:locale':'en_IN','og:site_name':'TaxPower','og:image':BASE+'asset/swt_icon/taxpower_icon.png'}.items():head.append(etree.Element('meta',{'property':prop,'content':value}))
    for name,value in {'twitter:card':'summary','twitter:title':meta['title'],'twitter:description':meta['description']}.items():head.append(etree.Element('meta',{'name':name,'content':value}))
    keep=meta['section']
    # Only this page's content stays: the other tabs are their own pages.
    cont=doc.xpath('//*[@data-page-sections]')[0]
    if keep=='home':cont.getparent().remove(cont)
    else:
        for node in doc.xpath('//main[@id="home"] | //section[contains(@class,"trusted-companies-section")] | //div[contains(@class,"home-extra")]'):node.getparent().remove(node)
        for node in list(cont):
            if node.get('id')!=keep:cont.remove(node)
        for node in cont:node.attrib.pop('data-loaded-page',None);node.set('class',node.get('class','').replace('loaded-page-section','').strip())
        cont.attrib.pop('data-prerendered',None);cont.attrib.pop('data-page-sections',None)
    # Per-page styles and scripts.
    for el in doc.xpath('//head/script[@src] | //head/link[@rel="stylesheet"][starts-with(@href,"css/")] | //head/link[@rel="preload"][@href="nav.html"]'):el.getparent().remove(el)
    # One minified CSS file and one JS file per page.
    assets=[(t,u) for t,u in head_assets[keep] if u not in DROP and u!='js/page-init.js']
    css_files=[u for t,u in assets if t=='link']
    if 'css/taxpowergst.css' in css_files:  # this sheet has always had to come last
        css_files.remove('css/taxpowergst.css');css_files.append('css/taxpowergst.css')
    js_files=[u for t,u in assets if t=='script']+['js/page-init.js']
    _b=etree.Element('script');_b.text="try{if(localStorage.getItem('tp-theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}catch(e){}";head.append(_b)
    head.append(etree.Element('link',{'rel':'stylesheet','href':bundle.make(keep,css_files,'css')}))
    head.append(etree.Element('script',{'src':bundle.make(keep,js_files,'js'),'defer':''}))
    stub=etree.Element('script');stub.text='window.TaxPowerPage='+json.dumps({'anchor':'#'+PAGE_ANCHOR.get(route,keep) if route in('demo-enquiry','home') else '','nav':NAV_PAGE[keep],'scrollTo':SCROLL_TO.get(route,'')})+';'
    head.insert(0,stub)
    head.append(html.fromstring('<script type="speculationrules">'+json.dumps({'prerender':[{'where':{'href_matches':BASE_PATH+'*'},'eagerness':'moderate'}],'prefetch':[{'where':{'href_matches':BASE_PATH+'*'},'eagerness':'moderate'}]})+'</script>'))
    # Same-page '#links' must keep working under <base>; links to other tabs become real page links.
    for a in doc.xpath('//a[@href]'):
        h=a.get('href')
        if h.startswith('#') and len(h)>1:
            if doc.xpath('//*[@id=$i]',i=h[1:]):a.set('href',route+h)
        elif h in anchors.values() or h.split('#')[0] in alias.values():pass
    # Mark the current tab in the header before any script runs.
    nav_item=doc.xpath('//a[contains(@class,"nav-item")][@data-nav-page=$p]',p=NAV_PAGE[keep])
    if nav_item:
        nav_item[0].set('class',nav_item[0].get('class','')+' h-current');nav_item[0].set('aria-current','page')
        if keep in('taxpowergst','taxpowertds'):
            for other in doc.xpath('//a[contains(@class,"nav-item")][@data-nav-page="taxpowergst.html" or @data-nav-page="taxpowertds.html"]'):
                if other is not nav_item[0]:other.set('class',other.get('class','')+' is-product-collapsed')
    primary=doc.get_element_by_id(meta['section'])
    for node in doc.xpath('//main'):node.tag='section';node.set('data-route-section','true')
    primary.tag='main';primary.set('data-route-section','true')
    heading=primary.xpath('.//*[@data-page-heading]')[0]
    if meta.get('heading'):heading=doc.get_element_by_id(meta['heading']);heading.set('class',(heading.get('class','')+' original-h2').strip())
    for h in doc.xpath('//h1'):h.tag='h2'
    heading.tag='h1'
    if not heading.get('id'):heading.set('id','page-heading-'+meta['section'])
    primary.set('aria-labelledby',heading.get('id'))
    graph=[organization,{'@type':'Organization','@id':BASE+'#magnum','name':'Magnum Infosystem Pvt. Ltd.','url':'https://www.magnuminfosystem.com/Default'},{'@type':'WebSite','@id':BASE+'#website','url':BASE+'home','name':'TaxPower','inLanguage':'en-IN','publisher':{'@id':BASE+'#siddharth'}},{'@type':'ContactPage' if meta['section']=='support' else 'AboutPage' if route=='aboutus' else 'WebPage','@id':canonical+'#webpage','url':canonical,'name':meta['title'],'description':meta['description'],'isPartOf':{'@id':BASE+'#website'},'publisher':{'@id':BASE+'#siddharth'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'home'}]+([] if route=='home' else [{'@type':'ListItem','position':2,'name':config[meta.get('canonical',route)]['title'].split('|')[0].strip(),'item':canonical}])}]
    if meta['section'] in ['taxpowergst','taxpowertds']:
        graph.append({'@type':'SoftwareApplication','name':'TaxPower Billing' if route=='gst-billing' else 'TaxPower TDS' if route=='taxpowertds' else 'TaxPower GST','applicationCategory':'BusinessApplication','applicationSubCategory':'GST and TDS compliance software','description':meta['description'],'operatingSystem':'Windows','url':canonical,'publisher':{'@id':BASE+'#magnum'}})
    if route=='pricing':
        graph.append({'@type':'ItemList','name':'TaxPower Complete Suite Plans','itemListElement':[{'@type':'ListItem','position':i+1,'item':{'@type':'Product','name':'TaxPower '+edition+' Complete Suite','brand':{'@type':'Brand','name':'TaxPower'},'offers':{'@type':'Offer','price':price,'priceCurrency':'INR','url':canonical,'seller':{'@id':BASE+'#siddharth'}}}} for i,(edition,price) in enumerate([('Professional',15000),('Business',20000)])]})
    schema=etree.Element('script',{'type':'application/ld+json','id':'site-structured-data','data-route':route});schema.text=json.dumps({'@context':'https://schema.org','@graph':graph});head.append(schema)
    # Both .html resolution and directory resolution serve the same static page.
    for filename,nested in [(route+'.html',False),(route+'/index.html',True)]+([('index.html',False)] if route=='home' else []):
        output=deepcopy(doc);base=etree.Element('base',{'href':BASE_PATH});output.find('head').insert(0,base)
        path=ROOT/filename;path.parent.mkdir(exist_ok=True);rendered='<!DOCTYPE html>\n'+html.tostring(output,encoding='unicode',method='html');rendered=rendered.replace('<footer class="site-footer',related.block(route)+'<footer class="site-footer',1)
        path.write_text('\n'.join(line.rstrip() for line in rendered.splitlines())+'\n')
landing=json.loads((ROOT/'scripts/landing-pages.json').read_text())
landing_slugs=[landing['hub']['slug']]+[c['slug'] for c in landing['cities']]+[f['slug'] for f in landing['features']]+[x['slug'] for x in json.loads((ROOT/'scripts/resource-pages.json').read_text())['pages']]+[x['slug'] for x in json.loads((ROOT/'scripts/resource-pages.json').read_text())['posts']]+['gst-tds-due-dates','taxpower-gst-features','taxpower-tds-features','sitemap']
canonical_routes=[r for r,m in config.items() if not m.get('canonical')]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+BASE+r+'</loc></url>\n' for r in canonical_routes+landing_slugs)+'</urlset>\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'sitemap.xml\n')
print('Built',len(config),'routes with static content, metadata, headings and schema.')
