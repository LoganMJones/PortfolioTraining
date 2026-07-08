(function () {
  "use strict";

  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.querySelector(".nav")
    || document.querySelector(".site-nav")
    || document.querySelector(".mobile-nav");

  if (menuBtn && nav) {
    function setMenuOpen(open) {
      nav.classList.toggle("is-open", open);
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      document.body.style.overflow = open ? "hidden" : "";
    }

    menuBtn.addEventListener("click", function () {
      setMenuOpen(!nav.classList.contains("is-open"));
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setMenuOpen(false);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        setMenuOpen(false);
        menuBtn.focus();
      }
    });
  }

  var sections = document.querySelectorAll("section[id]");
  var navLinks = nav ? nav.querySelectorAll("a[href^='#']") : [];

  if (sections.length && navLinks.length) {
    var navObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var id = entry.target.id;
            navLinks.forEach(function (link) {
              if (link.getAttribute("href") === "#" + id) {
                link.setAttribute("aria-current", "true");
              } else {
                link.removeAttribute("aria-current");
              }
            });
          }
        });
      },
      { rootMargin: "-45% 0px -45% 0px", threshold: 0 }
    );
    sections.forEach(function (s) { navObserver.observe(s); });
  }

  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach(function (el) { revealObserver.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  var deckSlides = document.querySelectorAll(".deck-slide[id]");
  var deckDots = document.querySelectorAll(".deck-dots a[href^='#']");

  if (deckSlides.length && deckDots.length) {
    var deckObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var id = entry.target.id;
            deckDots.forEach(function (dot) {
              if (dot.getAttribute("href") === "#" + id) {
                dot.setAttribute("aria-current", "true");
              } else {
                dot.removeAttribute("aria-current");
              }
            });
          }
        });
      },
      { root: document.querySelector(".deck"), threshold: 0.55 }
    );
    deckSlides.forEach(function (slide) { deckObserver.observe(slide); });
  }
})();
