/* Site-wide Dark/Light switch. Choice is saved in localStorage ('tp-theme'); first paint is set by the inline head script. */
(function(){
  var K='tp-theme',de=document.documentElement;
  function cur(){return de.getAttribute('data-theme')==='dark'?'dark':'light'}
  function apply(t){
    if(t==='dark')de.setAttribute('data-theme','dark');else de.removeAttribute('data-theme');
    /* Night mode on Home is a mix: these sections go dark, the others stay light. */
    document.querySelectorAll('.home-extra [aria-labelledby=hxB1Title],.home-extra [aria-labelledby=hxFormsTitle],.home-extra [aria-labelledby=hxStepsTitle],.home-extra [aria-labelledby=hxAreaTitle],.home-extra [aria-labelledby=hxCheckTitle],.home-extra [aria-label="Website development"],.home-extra [aria-labelledby=hxFinalTitle]').forEach(function(sec){
      if(t==='dark')sec.setAttribute('data-hx-theme','dark');else sec.removeAttribute('data-hx-theme');
    });
    var on=t==='dark';
    document.querySelectorAll('[data-theme-toggle]').forEach(function(b){
      b.setAttribute('aria-pressed',on?'true':'false');
      b.setAttribute('aria-label',on?'Switch to light mode':'Switch to dark mode');
      b.title=on?'Light mode':'Dark mode';
    });
  }
  apply(cur());
  document.querySelectorAll('[data-theme-toggle]').forEach(function(b){
    b.hidden=false;
    b.addEventListener('click',function(){
      var n=cur()==='dark'?'light':'dark';apply(n);
      try{localStorage.setItem(K,n)}catch(e){}
    });
  });
})();

document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-ft-top]');if(b){window.scrollTo({top:0,behavior:'smooth'})}});

(function(){
  function roll(){
    document.querySelectorAll('.footer-link-group a:not(.footer-demo-button), .footer-seo-group a').forEach(function(a){
      if(a.querySelector('.ft-roll')||a.children.length)return;
      var t=a.textContent;if(!t.trim())return;
      a.setAttribute('aria-label',t.trim());
      a.textContent='';
      var w=document.createElement('span');w.className='ft-roll';w.setAttribute('aria-hidden','true');
      Array.from(t).forEach(function(c,i){
        var ch=document.createElement('span');ch.className='ft-ch';ch.style.setProperty('--i',i);
        var a1=document.createElement('span');a1.textContent=c===' '?'\u00a0':c;
        var a2=document.createElement('span');a2.textContent=c===' '?'\u00a0':c;
        ch.appendChild(a1);ch.appendChild(a2);w.appendChild(ch);
      });
      a.appendChild(w);
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',roll);else roll();
})();

/* Phone bottom bar: mark the current page and open or close the Software and More sheets. */
(function(){
  var bar=document.querySelector('.tabbar'),back=document.getElementById('moreBackdrop');
  if(!bar||!back)return;
  var seg=location.pathname.replace(/\.html$/,'').replace(/\/index$/,'').replace(/\/+$/,'').split('/').pop();
  if(!seg||seg==='taxpower-update')seg='home';
  function hit(a){return (a.getAttribute('data-match')||'').split(' ').indexOf(seg)>-1}
  [].slice.call(bar.querySelectorAll('a.tab[data-match]')).forEach(function(a){if(hit(a)){a.classList.add('is-active');a.setAttribute('aria-current','page')}});
  var pairs=[['tabSoft','softSheet'],['tabMore','moreSheet']].map(function(p){
    var b=document.getElementById(p[0]),s=document.getElementById(p[1]);
    return b&&s?{btn:b,sheet:s}:null}).filter(Boolean);
  if(!pairs.length)return;
  pairs.forEach(function(p){
    var rows=[].slice.call(p.sheet.querySelectorAll('.more-row[data-match]'));
    rows.forEach(function(a){if(hit(a)){a.classList.add('is-active');a.setAttribute('aria-current','page');p.btn.classList.add('is-active')}});
  });
  function closeAll(except){pairs.forEach(function(p){if(p!==except){p.sheet.hidden=true;p.btn.setAttribute('aria-expanded','false')}})}
  function set(p,open){
    closeAll(open?p:null);
    p.sheet.hidden=!open;back.hidden=!open;p.btn.setAttribute('aria-expanded',String(open));
    document.body.classList.toggle('more-open',open);
    if(open){var f=p.sheet.querySelector('.more-row:not([hidden])');if(f)f.focus({preventScroll:true})}
  }
  pairs.forEach(function(p){
    p.btn.addEventListener('click',function(){set(p,p.sheet.hidden)});
    p.sheet.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('a'))set(p,false)});
  });
  back.addEventListener('click',function(){pairs.forEach(function(p){set(p,false)})});
  document.addEventListener('keydown',function(e){if(e.key!=='Escape')return;pairs.forEach(function(p){if(!p.sheet.hidden){set(p,false);p.btn.focus()}})});
  window.addEventListener('resize',function(){if(window.innerWidth>760)pairs.forEach(function(p){if(!p.sheet.hidden)set(p,false)})});
})();

/* Google review prompt. Desktop only: shown once, when a visitor who has spent a little time on the site moves the pointer
   out through the top of the window (towards the tab bar or close button). Asks only for an honest review from people who
   already use TaxPower. Remembered for 30 days, so it never nags. */
(function(){
  var URL='https://g.page/r/CfXFywcVUofsEAI/review',K='tp-review-ask',DAYS=30,MIN_MS=15000,start=Date.now(),shown=false,last=null;
  function get(){try{return localStorage.getItem(K)}catch(e){return null}}
  function put(){try{localStorage.setItem(K,String(Date.now()))}catch(e){}}
  var prev=get();
  if(prev&&Date.now()-Number(prev)<DAYS*864e5)return;
  if(!window.matchMedia||!window.matchMedia('(hover:hover) and (pointer:fine)').matches)return;
  function close(){var m=document.getElementById('tpReviewAsk');if(m)m.remove();document.removeEventListener('keydown',onKey);if(last&&last.focus)try{last.focus()}catch(e){}}
  function onKey(e){if(e.key==='Escape')close()}
  function open(){
    if(shown)return;shown=true;put();last=document.activeElement;
    var m=document.createElement('div');m.id='tpReviewAsk';m.className='tp-review-ask';
    m.innerHTML='<div class="tp-review-backdrop" data-rv-close></div><div class="tp-review-card" role="dialog" aria-modal="true" aria-labelledby="tpReviewTitle">'
      +'<button type="button" class="tp-review-x" data-rv-close aria-label="Close">&times;</button>'
      +'<div class="tp-review-stars" aria-hidden="true">★★★★★</div>'
      +'<h2 id="tpReviewTitle">Already use TaxPower?</h2>'
      +'<p>Your honest review on Google helps other CAs and businesses choose the right software. It takes about a minute.</p>'
      +'<div class="tp-review-actions"><a class="tp-review-go" href="'+URL+'" target="_blank" rel="noopener noreferrer" data-rv-close>Write a Google review</a>'
      +'<button type="button" class="tp-review-later" data-rv-close>Maybe later</button></div></div>';
    m.addEventListener('click',function(e){if(e.target.closest('[data-rv-close]'))close()});
    document.body.appendChild(m);document.addEventListener('keydown',onKey);
    var go=m.querySelector('.tp-review-go');if(go)go.focus();
  }
  document.addEventListener('mouseout',function(e){
    if(shown||e.relatedTarget||e.clientY>0)return;
    if(Date.now()-start<MIN_MS)return;
    if(document.body.classList.contains('more-open'))return;
    var a=document.activeElement;if(a&&/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName))return;
    open();
  });
})();

/* Compact page loader: a thin progress bar plus a small "Loading" pill.
   Nothing shows on fast loads. It appears only if a page (or the next page after a link click) is slow, and goes away when loading ends. */
(function(){
  var doc=document,root=doc.documentElement,bar,pill,tBar,tPill,tMax,tick,w=0,live=false;
  function build(){
    if(bar)return;
    bar=doc.createElement('div');bar.className='tp-ld-bar';bar.setAttribute('aria-hidden','true');
    pill=doc.createElement('div');pill.className='tp-ld-pill';pill.setAttribute('role','status');pill.setAttribute('aria-live','polite');
    pill.innerHTML='<span class="tp-ld-ic" aria-hidden="true"><svg viewBox="0 0 26 26"><circle cx="13" cy="13" r="11.5" class="t"/><circle cx="13" cy="13" r="11.5" class="a"/></svg><img src="asset/swt_icon/taxpower_icon.png" width="16" height="16" alt=""></span><span class="tp-ld-tx">Loading</span>';
    (doc.body||root).appendChild(bar);(doc.body||root).appendChild(pill);
  }
  function setW(v){w=v;bar.style.transform='scaleX('+v+')'}
  function start(barDelay,pillDelay){
    if(live)return;live=true;clearTimeout(tBar);clearTimeout(tPill);clearTimeout(tMax);
    tBar=setTimeout(function(){build();bar.classList.remove('done');bar.style.opacity='1';setW(.08);
      clearInterval(tick);tick=setInterval(function(){setW(w+(.86-w)*.07)},180)},barDelay);
    tPill=setTimeout(function(){build();pill.classList.add('on')},pillDelay);
    tMax=setTimeout(finish,20000);
  }
  function finish(){
    if(!live)return;live=false;clearTimeout(tBar);clearTimeout(tPill);clearTimeout(tMax);clearInterval(tick);
    if(!bar)return;
    setW(1);bar.classList.add('done');pill.classList.remove('on');
    setTimeout(function(){if(!live&&bar){bar.style.opacity='0'}},260);
    setTimeout(function(){if(!live&&bar){bar.style.transition='none';setW(0);void bar.offsetWidth;bar.style.transition=''}},700);
  }
  /* first load of this page */
  if(doc.readyState!=='complete'){start(200,700);window.addEventListener('load',finish,{once:true})}
  /* next page after a click on an internal link */
  doc.addEventListener('click',function(e){
    if(e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
    var a=e.target.closest&&e.target.closest('a[href]');
    if(!a||a.target&&a.target!=='_self'||a.hasAttribute('download'))return;
    var u;try{u=new URL(a.href,location.href)}catch(x){return}
    if(u.origin!==location.origin)return;
    if(u.pathname===location.pathname&&u.search===location.search)return;
    if(/\.(exe|msi|pdf|zip|ics|xml|png|jpe?g|webp|svg|gif|txt)$/i.test(u.pathname))return;
    start(0,900);
  },true);
  /* coming back with the Back button must never leave the loader on screen */
  window.addEventListener('pageshow',function(e){if(e.persisted)finish()});
})();
