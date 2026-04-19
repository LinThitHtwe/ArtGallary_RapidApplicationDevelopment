/**
 * Site-wide smooth scrolling (Lenis).
 * - Default: drives Lenis via requestAnimationFrame.
 * - Pages with GSAP + ScrollTrigger (home): call __lenisConnectGsap(gsap, ScrollTrigger)
 *   once so Lenis uses GSAP's ticker instead (avoids double raf).
 */
(function () {
  if (typeof window === "undefined" || !window.Lenis) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (window.__lenis) return;

  var lenis = new Lenis({
    duration: 1.45,
    easing: function (t) {
      return 1 - Math.pow(1 - t, 4);
    },
    smoothWheel: true,
    smoothTouch: false,
    wheelMultiplier: 0.92,
    touchMultiplier: 1.85,
    infinite: false,
  });

  window.__lenis = lenis;
  document.documentElement.classList.add("lenis", "lenis-smooth");

  var rafId = null;

  function defaultRaf(time) {
    lenis.raf(time);
    rafId = requestAnimationFrame(defaultRaf);
  }

  function startDefaultRaf() {
    if (rafId != null) return;
    rafId = requestAnimationFrame(defaultRaf);
  }

  function stopDefaultRaf() {
    if (rafId != null) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
  }

  window.__lenisConnectGsap = function (gsap, ScrollTrigger) {
    if (!gsap || !ScrollTrigger || window.__lenisGsapConnected) return;
    window.__lenisGsapConnected = true;
    stopDefaultRaf();
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(function (time) {
      lenis.raf(time * 1000);
    });
    gsap.ticker.lagSmoothing(0);
  };

  startDefaultRaf();

  window.addEventListener(
    "click",
    function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      var href = a.getAttribute("href");
      if (!href || href === "#") return;
      var el = document.querySelector(href);
      if (!el) return;
      e.preventDefault();
      if (typeof lenis.scrollTo !== "function") {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
        return;
      }
      try {
        lenis.scrollTo(el, {
          offset: -96,
          duration: 1.35,
          easing: function (t) {
            return 1 - Math.pow(1 - t, 3);
          },
        });
      } catch (err) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    },
    true
  );

  window.dispatchEvent(new CustomEvent("lenis:ready", { detail: { lenis: lenis } }));
})();
