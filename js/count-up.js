/* Counts the highlight numbers up when they scroll into view. Final values are already in the HTML. */
(function () {
  'use strict';
  var nums = document.querySelectorAll('.tp-num[data-to]');
  if (!nums.length) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;
  function text(el, v) {
    var s = el.dataset.sep ? Math.round(v).toLocaleString('en-IN') : String(Math.round(v));
    el.textContent = s + (el.dataset.suffix || '');
  }
  function run(el) {
    var to = Number(el.dataset.to), from = to > 1000 ? 0 : 0, dur = to >= 1000 ? 1600 : 1100, t0 = null;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      text(el, from + (to - from) * e);
      if (p < 1) requestAnimationFrame(step); else text(el, to);
    }
    text(el, 0);
    requestAnimationFrame(step);
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { io.unobserve(en.target); run(en.target); } });
  }, { threshold: 0.4 });
  nums.forEach(function (n) { io.observe(n); });
})();
