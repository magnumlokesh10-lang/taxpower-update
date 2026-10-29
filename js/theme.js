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
