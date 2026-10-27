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
      a.textContent='';
      var w=document.createElement('span');w.className='ft-roll';
      var s1=document.createElement('span');s1.textContent=t;
      var s2=document.createElement('span');s2.textContent=t;s2.setAttribute('aria-hidden','true');
      w.appendChild(s1);w.appendChild(s2);a.appendChild(w);
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',roll);else roll();
})();
