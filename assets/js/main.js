/* Sandbox Languages — site behaviour (no dependencies) */
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
    window.matchMedia("(min-width: 1021px)").addEventListener("change", function (mq) {
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
    // Deep-link support, e.g. programmes.html#teens
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

  /* ---------- Fee calculator ---------- */
  var calc = document.getElementById("fee-calculator");
  if (calc) {
    var gbp = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP", maximumFractionDigits: 0 });
    var weeksOut = calc.querySelector("[data-weeks]");
    var minus = calc.querySelector("[data-step='-1']");
    var plus = calc.querySelector("[data-step='1']");
    var weeks = 2;
    var MIN_WEEKS = 1;
    var MAX_WEEKS = 6;

    var update = function () {
      var prog = calc.querySelector("input[name='programme']:checked");
      var rate = Number(prog.dataset.rate);
      var lines = [];
      var total = 0;

      var courseCost = rate * weeks;
      lines.push([prog.dataset.label + " × " + weeks + (weeks === 1 ? " week" : " weeks"), courseCost]);
      total += courseCost;

      calc.querySelectorAll("input[data-extra]:checked").forEach(function (extra) {
        var cost = Number(extra.dataset.price) * (extra.dataset.per === "week" ? weeks : 1);
        lines.push([extra.dataset.label, cost]);
        total += cost;
      });

      // Multi-week discount: 5% off tuition for 3+ weeks
      if (weeks >= 3) {
        var discount = Math.round(courseCost * 0.05);
        lines.push(["Stay-longer saving (5%)", -discount]);
        total -= discount;
      }

      var registration = Number(calc.dataset.registration || 0);
      if (registration) {
        lines.push(["Registration fee", registration]);
        total += registration;
      }

      weeksOut.textContent = weeks + (weeks === 1 ? " week" : " weeks");
      minus.disabled = weeks <= MIN_WEEKS;
      plus.disabled = weeks >= MAX_WEEKS;

      var list = calc.querySelector(".calc-lines");
      list.innerHTML = "";
      lines.forEach(function (l) {
        var li = document.createElement("li");
        var a = document.createElement("span");
        var b = document.createElement("span");
        a.textContent = l[0];
        b.textContent = (l[1] < 0 ? "−" : "") + gbp.format(Math.abs(l[1]));
        li.append(a, b);
        list.appendChild(li);
      });
      calc.querySelector("[data-total]").textContent = gbp.format(total);
    };

    minus.addEventListener("click", function () { weeks = Math.max(MIN_WEEKS, weeks - 1); update(); });
    plus.addEventListener("click", function () { weeks = Math.min(MAX_WEEKS, weeks + 1); update(); });
    calc.addEventListener("change", update);
    update();
  }

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
      msg.textContent = "Thanks! We'll be in touch when 2027 bookings open.";
      form.reset();
    });
  });

  /* ---------- Pre-fill programme on contact form from ?programme= ---------- */
  var params = new URLSearchParams(location.search);
  var prefill = params.get("programme");
  var progSelect = document.getElementById("programme");
  if (prefill && progSelect) {
    Array.prototype.forEach.call(progSelect.options, function (opt) {
      if (opt.value === prefill) progSelect.value = prefill;
    });
  }
  var typePrefill = params.get("type");
  if (typePrefill) {
    var radio = document.querySelector("input[name='enquiry-type'][value='" + CSS.escape(typePrefill) + "']");
    if (radio) radio.checked = true;
  }
})();
