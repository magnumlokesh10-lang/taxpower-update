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
