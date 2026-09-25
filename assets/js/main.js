/* Sandbox English Summer School — site behaviour (no dependencies) */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  /* ---------- Sticky header shadow ---------- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      nav.classList.toggle("is-open", open);
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    window.matchMedia("(min-width: 1181px)").addEventListener("change", function (mq) {
      if (mq.matches) setOpen(false);
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- Tabs ---------- */
  document.querySelectorAll(".tabs").forEach(function (tabs) {
    var tabList = tabs.querySelectorAll('[role="tab"]');
    var select = function (tab, focus) {
      tabList.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) tab.focus();
      if (history.replaceState && tab.dataset.hash) {
        history.replaceState(null, "", "#" + tab.dataset.hash);
      }
    };
    tabList.forEach(function (tab, i) {
      tab.addEventListener("click", function () { select(tab); });
      tab.addEventListener("keydown", function (e) {
        var next = null;
        if (e.key === "ArrowRight") next = tabList[(i + 1) % tabList.length];
        if (e.key === "ArrowLeft") next = tabList[(i - 1 + tabList.length) % tabList.length];
        if (e.key === "Home") next = tabList[0];
        if (e.key === "End") next = tabList[tabList.length - 1];
        if (next) { e.preventDefault(); select(next, true); }
      });
    });
    // Deep-link support: a tab with data-hash="x" opens from page.html#x
    var hash = location.hash.replace("#", "");
    if (hash) {
      tabList.forEach(function (t) {
        if (t.dataset.hash === hash) {
          select(t);
          tabs.scrollIntoView();
        }
      });
    }
  });

  /* ---------- Form validation ---------- */
  var messages = {
    valueMissing: "Please fill in this field.",
    typeMismatch: "Please check the format of this field.",
    patternMismatch: "Please check the format of this field.",
    rangeUnderflow: "That value is too low.",
    rangeOverflow: "That value is too high."
  };

  var fieldOf = function (input) { return input.closest(".field") || input.closest(".checkbox"); };

  var showError = function (input) {
    var field = fieldOf(input);
    if (!field) return true;
    var errorEl = field.querySelector(".field-error");
    var msg = "";
    if (!input.validity.valid) {
      if (input.type === "email" && input.validity.typeMismatch) msg = "Please enter a valid email address, e.g. name@example.com.";
      else if (input.type === "checkbox" && input.validity.valueMissing) msg = "Please tick this box to continue.";
      else {
        for (var key in messages) {
          if (input.validity[key]) { msg = input.dataset.error || messages[key]; break; }
        }
      }
    }
    field.classList.toggle("has-error", !!msg);
    input.setAttribute("aria-invalid", msg ? "true" : "false");
    if (errorEl) errorEl.textContent = msg;
    return !msg;
  };

  document.querySelectorAll("form[data-validate]").forEach(function (form) {
    form.setAttribute("novalidate", "");
    var inputs = form.querySelectorAll("input, select, textarea");

    inputs.forEach(function (input) {
      input.addEventListener("blur", function () {
        if (input.value || input.dataset.touched) showError(input);
        input.dataset.touched = "1";
      });
      input.addEventListener("input", function () {
        if (fieldOf(input) && fieldOf(input).classList.contains("has-error")) showError(input);
      });
    });

    form.addEventListener("submit", function (e) {
      var firstInvalid = null;
      inputs.forEach(function (input) {
        if (!showError(input) && !firstInvalid) firstInvalid = input;
      });
      if (firstInvalid) {
        e.preventDefault();
        firstInvalid.focus();
        return;
      }
      // No backend is wired up yet: if the form has no real action,
      // show the success state instead of navigating away.
      if (!form.getAttribute("action") || form.getAttribute("action") === "#") {
        e.preventDefault();
        var success = document.getElementById(form.dataset.success);
        if (success) {
          form.hidden = true;
          success.hidden = false;
          success.focus();
        }
      }
    });
  });

  /* ---------- Newsletter ---------- */
  document.querySelectorAll(".newsletter").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = form.querySelector("input[type='email']");
      var msg = form.parentElement.querySelector(".newsletter-msg");
      if (!input.value || !input.checkValidity()) {
        msg.textContent = "Please enter a valid email address.";
        input.focus();
        return;
      }
      msg.textContent = "Thanks! We'll be in touch when summer 2028 places open.";
      form.reset();
    });
  });

  /* ---------- Pre-fill the consultation form from links, e.g. ?type=agent&area=london ---------- */
  var params = new URLSearchParams(location.search);
  var type = params.get("type");
  if (type) {
    var radio = document.querySelector('input[name="enquirer"][value="' + (/^(parent|agent|group)$/.test(type) ? type : "other") + '"]');
    if (radio) radio.checked = true;
  }
  var area = document.getElementById("area");
  var areaParam = params.get("area");
  if (area && areaParam) {
    Array.prototype.forEach.call(area.options, function (opt) {
      if (opt.value === areaParam) area.value = areaParam;
    });
  }
})();
