/* Small starter for every page. Header, page content and footer are already in the HTML. */
(() => {
  const start = () => {
    const year = document.querySelector('[data-current-year]');
    if (year) year.textContent = new Date().getFullYear();
    // Scripts that wait for the page content are told it is ready.
    document.dispatchEvent(new CustomEvent('taxpower:sections-loaded'));
    document.dispatchEvent(new CustomEvent('taxpower:footer-loaded'));
    // Pages such as GST Billing or Technical Support open at a part of a bigger page.
    const anchor = (window.TaxPowerPage && window.TaxPowerPage.scrollTo) || '';
    const target = anchor && document.getElementById(anchor);
    if (target && !location.hash) {
      const header = document.querySelector('.header');
      const top = target.getBoundingClientRect().top + window.scrollY - (header ? header.offsetHeight : 64) - 16;
      window.scrollTo({ top: Math.max(0, top), behavior: 'auto' });
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();

(function(){var h,t=false;function u(){t=false;h=h||document.querySelector('.header');if(h)h.classList.toggle('is-scrolled',window.scrollY>12)}
function s(){if(!t){t=true;requestAnimationFrame(u)}}
window.addEventListener('scroll',s,{passive:true});document.addEventListener('taxpower:sections-loaded',u);u()})();


(function(){
  var K='tp-home-theme',root=document.querySelector('.home-extra');
  if(!root)return;
  var btn=root.querySelector('[data-hx-theme-toggle]');
  function apply(t){
    if(t==='dark')root.setAttribute('data-hx-theme','dark');else root.removeAttribute('data-hx-theme');
    if(btn){btn.setAttribute('aria-pressed',t==='dark'?'true':'false');var l=btn.querySelector('.hx-theme-t');if(l)l.textContent=t==='dark'?'Light':'Dark'}
  }
  var saved=null;try{saved=localStorage.getItem(K)}catch(e){}
  apply(saved==='dark'?'dark':'light');
  if(btn){btn.hidden=false;btn.addEventListener('click',function(){
    var next=root.getAttribute('data-hx-theme')==='dark'?'light':'dark';apply(next);
    try{localStorage.setItem(K,next)}catch(e){}
  })}
})();
