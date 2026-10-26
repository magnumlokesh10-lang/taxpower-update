"""Join and minify the CSS or JS a page needs into one file (css/p-<name>.css, js/p-<name>.js).
The files in css/ and js/ stay the editable sources; the p-* files are build output.
Uses esbuild if present (ESBUILD env var, or the usual tool folders); otherwise joins files without minifying."""
import hashlib,os,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def _esbuild():
    for c in [os.environ.get('ESBUILD'),shutil.which('esbuild'),'/opt/npm-tools/node_modules/.bin/esbuild',str(ROOT/'node_modules/.bin/esbuild')]:
        if c and Path(c).exists():return c
def _min(text,loader):
    e=_esbuild()
    if not e:return text
    return subprocess.run([e,'--loader='+loader,'--minify','--log-level=error'],input=text,capture_output=True,text=True,check=True).stdout
def make(name,files,kind):
    """files: source paths like 'css/stylesheet.css' in cascade/run order. Returns 'css/p-name.css?v=hash'."""
    files=list(files)
    if kind=='js' and name!='landing' and 'js/theme.js' not in files:files.append('js/theme.js')
    parts=[]
    for f in files:
        t=(ROOT/f).read_text()
        parts.append(_min(t,kind) if kind=='css' else _min(t,'js').rstrip().rstrip(';')+';')
    if kind=='css':
        import darkgen
        dk=[darkgen.generate((ROOT/f).read_text()) for f in files if not f.endswith('home-sections.css')]
        parts.append(_min('\n'.join(dk)+'\n'+(ROOT/'css/dark-extra.css').read_text(),'css'))
    out=('\n' if kind=='css' else '\n').join(parts)+'\n'
    rel=f'{kind}/p-{name}.{kind}'
    (ROOT/rel).write_text(out)
    return rel+'?v='+hashlib.md5(out.encode()).hexdigest()[:8]
