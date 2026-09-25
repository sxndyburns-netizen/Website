/* Sandbox English Summer School — site behaviour (no dependencies) */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");

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
    if (window.matchMedia) {
      var desktop = window.matchMedia("(min-width: 1241px)");
      var onChange = function (mq) { if (mq.matches) setOpen(false); };
      if (desktop.addEventListener) desktop.addEventListener("change", onChange);
      else if (desktop.addListener) desktop.addListener(onChange);
    }
  }

  /* ---------- Reveal on scroll ----------
     Content is only hidden once the observer is running (html.reveal-ready),
     so if anything fails, everything stays visible. */
  if ("IntersectionObserver" in window) {
    var revealEls = document.querySelectorAll(".reveal");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
    root.classList.add("reveal-ready");
  }

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- Form validation ---------- */
  var messages = {
    valueMissing: "Please fill in this field.",
    typeMismatch: "Please check the format of this field.",
    patternMismatch: "Please check the format of this field.",
    rangeUnderflow: "That value is too low.",
    rangeOverflow: "That value is too high.",
    stepMismatch: "Please enter a whole number.",
    badInput: "Please enter a number."
  };

  var errorElFor = function (input) {
    var ids = (input.getAttribute("aria-describedby") || "").split(/\s+/);
    for (var i = 0; i < ids.length; i++) {
      var el = ids[i] && document.getElementById(ids[i]);
      if (el && el.classList.contains("field-error")) return el;
    }
    return null;
  };

  var isActive = function (input) {
    return !input.disabled && !input.closest("[hidden]");
  };

  var showError = function (input) {
    var errorEl = errorElFor(input);
    if (!errorEl) return true;
    var msg = "";
    if (isActive(input) && !input.validity.valid) {
      if (input.type === "email" && input.validity.typeMismatch) msg = "Please enter a valid email address, e.g. name@example.com.";
      else if (input.type === "checkbox" && input.validity.valueMissing) msg = "Please tick this box to continue.";
      else if (input.dataset.error) msg = input.dataset.error;
      else {
        for (var key in messages) {
          if (input.validity[key]) { msg = messages[key]; break; }
        }
        if (!msg) msg = "Please check this field.";
      }
    }
    var field = input.closest(".field");
    if (field) field.classList.toggle("has-error", !!msg);
    input.setAttribute("aria-invalid", msg ? "true" : "false");
    errorEl.textContent = msg;
    return !msg;
  };

  document.querySelectorAll("form[data-validate]").forEach(function (form) {
    form.setAttribute("novalidate", "");
    var inputs = form.querySelectorAll("input, select, textarea");

    inputs.forEach(function (input) {
      var touched = false;
      input.addEventListener("blur", function () {
        var hasValue = input.type === "checkbox" || input.type === "radio" ? false : input.value !== "";
        if (hasValue || touched) showError(input);
        touched = true;
      });
      input.addEventListener(input.type === "checkbox" ? "change" : "input", function () {
        var field = input.closest(".field");
        if (field && field.classList.contains("has-error")) showError(input);
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
      // No backend is wired up yet: with no real action, show the success state instead.
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

  /* ---------- Consultation form: fields that depend on other answers ---------- */
  var consult = document.getElementById("consultation-form");
  if (consult) {
    var phone = document.getElementById("phone");
    var phoneMark = consult.querySelector("[data-phone-required]");

    var syncEnquirer = function () {
      var checked = consult.querySelector('input[name="enquirer"]:checked');
      var who = checked ? checked.value : "parent";
      consult.querySelectorAll("[data-show-for]").forEach(function (el) {
        var show = el.dataset.showFor.split(" ").indexOf(who) !== -1;
        el.hidden = !show;
        el.querySelectorAll("input, select, textarea").forEach(function (i) { i.disabled = !show; });
      });
    };
    var syncMethod = function () {
      var checked = consult.querySelector('input[name="method"]:checked');
      var needsPhone = !!checked && checked.value !== "video";
      phone.required = needsPhone;
      if (phoneMark) phoneMark.hidden = !needsPhone;
      if (!needsPhone) showError(phone);
    };

    // Pre-fill from links, e.g. consultation.html?type=agent&area=london
    var params = new URLSearchParams(location.search);
    var type = params.get("type");
    if (type) {
      var radio = consult.querySelector('input[name="enquirer"][value="' + (/^(parent|agent|group)$/.test(type) ? type : "other") + '"]');
      if (radio) radio.checked = true;
    }
    var area = document.getElementById("area");
    var areaParam = params.get("area");
    if (area && areaParam) {
      Array.prototype.forEach.call(area.options, function (opt) {
        if (opt.value === areaParam) area.value = areaParam;
      });
    }

    consult.addEventListener("change", function (e) {
      if (e.target.name === "enquirer") syncEnquirer();
      if (e.target.name === "method") syncMethod();
    });
    syncEnquirer();
    syncMethod();
  }

  /* ---------- Newsletter ---------- */
  document.querySelectorAll(".newsletter").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      var input = form.querySelector("input[type='email']");
      var msg = form.parentElement.querySelector(".newsletter-msg");
      if (!input.value || !input.checkValidity()) {
        e.preventDefault();
        msg.textContent = "Please enter a valid email address.";
        input.focus();
        return;
      }
      // With a real action set, let the browser submit to the email provider.
      if (form.getAttribute("action") && form.getAttribute("action") !== "#") return;
      e.preventDefault();
      msg.textContent = "Thanks! We'll be in touch when summer 2028 places open.";
      form.reset();
    });
  });
})();
