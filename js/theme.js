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

/* Phone bottom bar: mark the current page and open or close the More sheet. */
(function(){
  var bar=document.querySelector('.tabbar'),more=document.getElementById('tabMore'),sheet=document.getElementById('moreSheet'),back=document.getElementById('moreBackdrop');
  if(!bar||!more||!sheet||!back)return;
  var seg=location.pathname.replace(/\.html$/,'').replace(/\/index$/,'').replace(/\/+$/,'').split('/').pop();
  if(!seg||seg==='taxpower-update')seg='home';
  function mark(list,cls,aria){var hit=false;list.forEach(function(a){if((a.getAttribute('data-match')||'').split(' ').indexOf(seg)>-1){a.classList.add(cls);if(aria)a.setAttribute('aria-current','page');hit=true}});return hit}
  mark([].slice.call(bar.querySelectorAll('.tab[data-match]')),'is-active',true);
  if(mark([].slice.call(sheet.querySelectorAll('.more-row[data-match]')),'is-active',true))more.classList.add('is-active');
  function set(open){sheet.hidden=!open;back.hidden=!open;more.setAttribute('aria-expanded',String(open));document.body.classList.toggle('more-open',open);if(open){var f=sheet.querySelector('.more-row:not([hidden])');if(f)f.focus({preventScroll:true})}}
  more.addEventListener('click',function(){set(sheet.hidden)});
  back.addEventListener('click',function(){set(false)});
  sheet.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('a'))set(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!sheet.hidden){set(false);more.focus()}});
  window.addEventListener('resize',function(){if(window.innerWidth>760&&!sheet.hidden)set(false)});
})();
