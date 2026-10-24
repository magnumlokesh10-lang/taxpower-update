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
  var K='tp-nav-line',line;
  function place(animate){
    var wrap=document.getElementById('navLinksContainer');
    if(!wrap||window.innerWidth<=1180)return;
    var cur=wrap.querySelector('.nav-item.h-current');
    if(!cur)return;
    if(!line){line=document.createElement('span');line.className='nav-slide-line';line.setAttribute('aria-hidden','true');wrap.appendChild(line)}
    var w=wrap.getBoundingClientRect(),c=cur.getBoundingClientRect();
    var width=Math.max(24,Math.min(72,c.width*.6)),x=c.left-w.left+(c.width-width)/2;
    var prev=null;try{prev=JSON.parse(sessionStorage.getItem(K)||'null')}catch(e){}
    if(animate&&prev){line.style.transition='none';line.style.width=prev.w+'px';line.style.transform='translateX('+prev.x+'px)';line.classList.add('on');void line.offsetWidth;line.style.transition=''}
    line.style.width=width+'px';line.style.transform='translateX('+x+'px)';line.classList.add('on');
    try{sessionStorage.setItem(K,JSON.stringify({x:x,w:width}))}catch(e){}
  }
  function init(){requestAnimationFrame(function(){place(true);setTimeout(function(){place(false)},700)})}
  document.addEventListener('taxpower:sections-loaded',init);
  window.addEventListener('load',function(){setTimeout(function(){place(false)},300)});
  window.addEventListener('resize',function(){place(false)});
  if(document.readyState!=='loading')init();
})();
