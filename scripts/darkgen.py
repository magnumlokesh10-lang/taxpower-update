"""Build the dark-mode override CSS for a page bundle.
For every rule in the bundle's source stylesheets that uses colour, emit a copy scoped to html[data-theme=dark]
with the colours remapped by lightness (light surfaces -> dark, dark text -> light, brand colours kept).
Runs at build time, so the browser only downloads plain CSS."""
import colorsys,re
DARK='html[data-theme=dark]'
# Banners/heroes are designed bright (photos, illustrations); they stay as in light mode.
BRIGHT=['.slider-viewport','.pricing-banner','.downloads-banner','.gst-feature-card','.gst-feature-row','.gst-dashboard-hero','.gst-motion-frame','.gst-browser-frame','.company-logo-card']
NOT_IN=':where(:not(:is('+','.join(b+','+b+' *' for b in BRIGHT)+')))'
HEX=re.compile(r'#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b')
FUNC=re.compile(r'(rgba?|hsla?)\(([^()]*)\)',re.I)
NAMED={'white':(255,255,255,1),'black':(0,0,0,1)}
NAMEDRE=re.compile(r'(?<![\w#-])(white|black)(?![\w-])',re.I)
URL=re.compile(r'url\((?:[^()"\']|"[^"]*"|\'[^\']*\')*\)',re.I)
BG={'background','background-color','background-image'}
TXT={'color','fill','stroke','caret-color','-webkit-text-fill-color','text-decoration-color'}
def _hex(h):
    h=h[1:]
    if len(h)in(3,4):h=''.join(c*2 for c in h)
    r,g,b=(int(h[i:i+2],16) for i in(0,2,4));a=int(h[6:8],16)/255 if len(h)==8 else 1
    return r,g,b,a
def _func(kind,body):
    p=[x for x in re.split(r'[,\s/]+',body.strip()) if x]
    def num(x,scale):
        return float(x[:-1])/100*scale if x.endswith('%') else float(x)
    try:
        if kind.lower().startswith('rgb'):
            r,g,b=(num(p[i],255) for i in range(3));a=num(p[3],1) if len(p)>3 else 1
            return r,g,b,a
        h=float(p[0].replace('deg',''));s=num(p[1],1);l=num(p[2],1);a=num(p[3],1) if len(p)>3 else 1
        if s>1:s/=100
        if l>1:l/=100
        r,g,b=colorsys.hls_to_rgb(h/360%1,l,s);return r*255,g*255,b*255,a
    except Exception:return None
def _fmt(r,g,b,a):
    r,g,b=(max(0,min(255,round(v))) for v in(r,g,b))
    if a>=0.999:return '#%02x%02x%02x'%(r,g,b)
    return 'rgba(%d,%d,%d,%s)'%(r,g,b,('%.3f'%a).rstrip('0').rstrip('.'))
def _map(c,mode):
    r,g,b,a=c;h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255)
    if mode=='text':
        if l<0.45:l=0.95-0.5*l;s*=0.85;a=min(1,a+0.3) if a<1 else a
        elif l<0.74:l=0.76
        else:return c,False
    elif mode=='border':
        if l>=0.75:l=0.37-(l-0.75)*0.6;s*=0.7
        elif l<0.3 and a<0.5:return (255,255,255,a),True
        else:return c,False
    else:  # surface (backgrounds, shadows)
        if l>=0.78:l=0.07+(1-l)*0.9;s*=0.75
        else:return c,False
    if mode!='text' and s<0.12:h=0.6;s=0.30  # neutral greys take the site's navy tint
    r,g,b=colorsys.hls_to_rgb(h,l,s);return (r*255,g*255,b*255,a),True
def _mode(prop):
    p=prop.lower()
    if p.startswith('--'):
        return 'text' if re.search(r'text|ink|fg|font|mute|title|head|label|copy|dim|sub',p) else 'border' if re.search(r'border|line|stroke',p) else 'surface'
    if p in TXT:return 'text'
    if p in BG or p.startswith('background'):return 'surface'
    if 'shadow' in p:return 'surface'
    if (p.startswith('border') or p.startswith('outline') or p=='column-rule') and not re.search(r'radius|width|style|spacing|collapse|image|offset',p):return 'border'
    return None
def remap(prop,value):
    """Return (new_value, changed, kept_colored_bg)."""
    mode=_mode(prop)
    if not mode:return value,False
    urls=[];value2=URL.sub(lambda m:(urls.append(m.group(0)),'\0%d\0'%(len(urls)-1))[1],value)
    changed=False
    def rep_hex(m):
        nonlocal changed
        c=_hex(m.group(0));n,ch=_map(c,mode)
        if ch:changed=True;return _fmt(*n)
        return m.group(0)
    def rep_fn(m):
        nonlocal changed
        c=_func(m.group(1),m.group(2))
        if not c:return m.group(0)
        n,ch=_map(c,mode)
        if ch:changed=True;return _fmt(*n)
        return m.group(0)
    def rep_name(m):
        nonlocal changed
        n,ch=_map(NAMED[m.group(1).lower()],mode)
        if ch:changed=True;return _fmt(*n)
        return m.group(0)
    v=HEX.sub(rep_hex,value2);v=FUNC.sub(rep_fn,v);v=NAMEDRE.sub(rep_name,v)
    v=re.sub('\0(\\d+)\0',lambda m:urls[int(m.group(1))],v)
    return v,changed
def _has_colored_bg(decls):
    for prop,val in decls:
        if prop.lower() in BG and 'url(' not in val.lower()[:4]:
            if 'gradient' in val.lower() or HEX.search(val) or FUNC.search(val):
                cols=[_hex(x) for x in HEX.findall(val)]+[c for c in (_func(m.group(1),m.group(2)) for m in FUNC.finditer(val)) if c]
                for r,g,b,a in cols:
                    h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255)
                    if a>0.5 and 0.25<l<0.78 and s>0.25:return True
    return False
def _split_decls(body):
    out=[];cur='';depth=0;q=None
    for ch in body:
        if q:
            cur+=ch
            if ch==q:q=None
            continue
        if ch in'"\'':q=ch;cur+=ch;continue
        if ch=='(':depth+=1
        elif ch==')':depth-=1
        if ch==';'and depth==0:out.append(cur);cur=''
        else:cur+=ch
    if cur.strip():out.append(cur)
    res=[]
    for d in out:
        if ':' not in d:continue
        k,v=d.split(':',1);res.append((k.strip(),v.strip()))
    return res
def _split_sel(sel):
    out=[];cur='';depth=0
    for ch in sel:
        if ch in'([':depth+=1
        elif ch in')]':depth-=1
        if ch==','and depth==0:out.append(cur);cur=''
        else:cur+=ch
    out.append(cur);return [s.strip() for s in out if s.strip()]
def _scope(sel):
    s=sel
    m=re.search(r'(::?(?:before|after|first-line|first-letter|placeholder|selection|marker|-webkit-[\w-]+))$',s)
    s=(s[:m.start()]+NOT_IN+m.group(1)) if m else s+NOT_IN
    if s.startswith(':root'):return DARK+s[5:]
    if s.startswith('html'):return DARK+s[4:]
    return DARK+' '+s
def _blocks(css):
    """yield (prelude, body) top-level blocks."""
    i=0;n=len(css);depth=0;start=0;pre='';q=None
    out=[];bs=0
    while i<n:
        ch=css[i]
        if q:
            if ch==q:q=None
        elif ch in'"\'':q=ch
        elif ch=='{':
            if depth==0:pre=css[start:i].strip();bs=i+1
            depth+=1
        elif ch=='}':
            depth-=1
            if depth==0:out.append((pre,css[bs:i]));start=i+1
        elif ch==';'and depth==0:start=i+1
        i+=1
    return out
def _gen(css):
    out=[]
    for pre,body in _blocks(css):
        if pre.startswith('@'):
            name=re.match(r'@[\w-]+',pre).group(0).lower()
            if name in('@media','@supports','@layer','@container'):
                inner=_gen(body)
                if inner:out.append(pre+'{'+inner+'}')
            continue
        decls=_split_decls(body);keep=_has_colored_bg(decls)
        new=[]
        for k,v in decls:
            imp=''
            if v.lower().endswith('!important'):v=v[:-10].strip();imp='!important'
            if keep and _mode(k)=='text':continue
            nv,ch=remap(k,v)
            # Unchanged colour declarations are repeated too, so a later, more specific light rule (e.g. .btn.active) keeps beating an earlier mapped one.
            if _mode(k):new.append(f'{k}:{nv}{imp}')
        if not new:continue
        sels=[_scope(s) for s in _split_sel(pre) if '.home-extra' not in s and 'data-hx-theme' not in s]
        if sels:out.append(','.join(sels)+'{'+';'.join(new)+'}')
    return '\n'.join(out)
def generate(css_text):
    css=re.sub(r'/\*.*?\*/','',css_text,flags=re.S)
    return _gen(css)
