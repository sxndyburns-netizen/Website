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

  /* ---------- Sending forms to Formspree ----------
     Forms post to their action URL (the Formspree endpoint set in src/build.py).
     With JavaScript we send JSON in the background and stay on the page; without it,
     the browser posts the form normally and Formspree shows its own thank-you page. */
  var hasEndpoint = function (form) {
    var action = form.getAttribute("action");
    return !!action && action !== "#";
  };

  // Human-readable value for a field: the option or label text, not the internal value.
  var readable = function (input) {
    if (input.type === "radio" || input.type === "checkbox") {
      if (input.dataset.value) return input.dataset.value;
      var label = input.closest("label");
      return label ? label.textContent.replace(/\s+/g, " ").trim() : input.value;
    }
    if (input.tagName === "SELECT") {
      var opt = input.options[input.selectedIndex];
      return opt && opt.value !== "" ? opt.text : "";
    }
    return input.value.trim();
  };

  var collect = function (form) {
    var data = {};
    Array.prototype.forEach.call(form.elements, function (input) {
      if (!input.name || input.disabled || input.type === "submit" || input.type === "button") return;
      if ((input.type === "radio" || input.type === "checkbox") && !input.checked) return;
      var value = input.type === "hidden" || input.name === "_gotcha" ? input.value : readable(input);
      if (value === "" && input.name !== "_gotcha") return;
      data[input.name] = data[input.name] ? data[input.name] + ", " + value : value;
    });
    if (data.email) data._replyto = data.email;
    return data;
  };

  var send = function (form, data) {
    return fetch(form.getAttribute("action"), {
      method: "POST",
      headers: { "Accept": "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(data),
      credentials: "omit"
    }).then(function (res) {
      if (!res.ok) throw new Error("Formspree returned " + res.status);
      return res;
    });
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
      e.preventDefault();
      var success = document.getElementById(form.dataset.success);
      var status = document.getElementById(form.dataset.status);
      var button = form.querySelector("[type='submit']");
      var showSuccess = function () {
        if (!success) return;
        form.hidden = true;
        success.hidden = false;
        success.focus();
      };
      // No endpoint set (e.g. a local copy): show the success state without sending.
      if (!hasEndpoint(form) || !window.fetch) {
        if (hasEndpoint(form)) { form.submit(); return; }
        showSuccess();
        return;
      }
      var data = collect(form);
      if (data.enquirer) data._subject = "Consultation request: " + data.enquirer + (data.name ? " – " + data.name : "");
      if (status) status.hidden = true;
      button.disabled = true;
      form.setAttribute("aria-busy", "true");
      send(form, data).then(showSuccess).catch(function () {
        form.removeAttribute("aria-busy");
        if (status) {
          status.innerHTML = 'Sorry, your request couldn\'t be sent. Please check your connection and try again. If it still doesn\'t work, email us at <a href="mailto:hello@sandboxenglish.co.uk">hello@sandboxenglish.co.uk</a>.';
          status.hidden = false;
          status.focus();
        }
      }).then(function () {
        button.disabled = false;
        form.removeAttribute("aria-busy");
      });
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
    form.setAttribute("novalidate", ""); // validated below; without JS the browser checks the email itself
    form.addEventListener("submit", function (e) {
      var input = form.querySelector("input[type='email']");
      var msg = form.parentElement.querySelector(".newsletter-msg");
      if (!input.value || !input.checkValidity()) {
        e.preventDefault();
        msg.textContent = "Please enter a valid email address.";
        input.focus();
        return;
      }
      e.preventDefault();
      var thanks = function () {
        msg.textContent = "Thanks! We'll be in touch when summer 2028 places open.";
        form.reset();
      };
      if (!hasEndpoint(form) || !window.fetch) {
        if (hasEndpoint(form)) { form.submit(); return; }
        thanks();
        return;
      }
      var button = form.querySelector("[type='submit']");
      button.disabled = true;
      msg.textContent = "Signing you up…";
      send(form, collect(form)).then(thanks).catch(function () {
        msg.textContent = "Sorry, that didn't work. Please try again in a moment.";
      }).then(function () { button.disabled = false; });
    });
  });
})();
