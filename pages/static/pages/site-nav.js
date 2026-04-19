/**
 * Public nav: hide on scroll down, show on scroll up.
 * Works with Lenis (uses lenis.scroll + lenis "scroll" event) and native scroll fallback.
 */
(function () {
  var wrap = document.getElementById("siteHeaderWrap");
  if (!wrap || !wrap.hasAttribute("data-nav-scroll")) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) return;

  var lastY = 0;
  var threshold = 8;
  var topReveal = 48;

  function getScrollY() {
    if (window.__lenis && typeof window.__lenis.scroll === "number") {
      return window.__lenis.scroll;
    }
    return window.scrollY || document.documentElement.scrollTop || 0;
  }

  function onScrollFrame() {
    var y = getScrollY();

    if (y < topReveal) {
      wrap.classList.remove("site-header-wrap--hidden");
      lastY = y;
      return;
    }

    var delta = y - lastY;
    if (delta > threshold) {
      wrap.classList.add("site-header-wrap--hidden");
    } else if (delta < -threshold) {
      wrap.classList.remove("site-header-wrap--hidden");
    }

    lastY = y;
  }

  function bind() {
    lastY = getScrollY();

    var ticking = false;
    function onNativeScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        onScrollFrame();
      });
    }

    function attachLenis() {
      if (!window.__lenis || typeof window.__lenis.on !== "function") return false;
      window.__lenis.on("scroll", onScrollFrame);
      return true;
    }

    if (attachLenis()) return;

    window.addEventListener("scroll", onNativeScroll, { passive: true });

    window.addEventListener(
      "lenis:ready",
      function onReady() {
        window.removeEventListener("scroll", onNativeScroll);
        window.removeEventListener("lenis:ready", onReady);
        attachLenis();
      },
      { once: true }
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();
