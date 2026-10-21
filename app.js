// AI StackWatch 24 — progressive enhancement only. All content is in the static HTML;
// this script animates counters and duplicates the ticker strip for a seamless loop.
(function () {
  // Duplicate ticker content once for a seamless marquee loop
  var t = document.querySelector(".ticker");
  if (t) { t.innerHTML += t.innerHTML; }

  // Count-up animation for hero stats (final values already in the HTML for no-JS readers)
  var nums = document.querySelectorAll(".stat .num[data-count]");
  if ("IntersectionObserver" in window && nums.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, target = parseFloat(el.getAttribute("data-count")), t0 = null;
        io.unobserve(el);
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min((ts - t0) / 1100, 1);
          el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString("en-US");
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    nums.forEach(function (n) { io.observe(n); });
  }

  // Layer map: hovering/tapping a layer dims the others
  var layers = document.querySelectorAll(".layer");
  layers.forEach(function (l) {
    function on() { layers.forEach(function (o) { o.style.opacity = (o === l) ? "1" : "0.45"; }); }
    function off() { layers.forEach(function (o) { o.style.opacity = "1"; }); }
    l.addEventListener("mouseenter", on);
    l.addEventListener("mouseleave", off);
    l.addEventListener("click", on);
  });
})();
