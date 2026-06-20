/* LETTAGA site — i18n (flags, EN-UK/US), per-country market (pricing+products+sponsors),
   per-language hero video, Start→country chooser modal, graph bars, nav, reveal, WhatsApp */
(function () {
  var LANG_KEY = 'lettaga_lang';
  var MARKET_KEY = 'lettaga_market';
  var DICT = window.LETTAGA_I18N || {};
  var LANGS = window.LETTAGA_LANGS || [{ code: 'en', label: 'English' }];
  var VIDEOS = window.LETTAGA_VIDEOS || { def: 'cafPEJSs2WE' };
  var CURRENT = 'en';

  var REGIONS = {
    sg: { flag: '🇸🇬', name: 'Singapore', cur: 'S$', ent: '25', tld: 'sg' },
    my: { flag: '🇲🇾', name: 'Malaysia',  cur: 'RM', ent: '40', tld: 'my' }
  };
  function marketForLang(lang) { return (lang === 'ms') ? 'my' : 'sg'; }
  function storedMarket() { try { return localStorage.getItem(MARKET_KEY); } catch (e) { return null; } }

  function langMeta(code) {
    for (var i = 0; i < LANGS.length; i++) if (LANGS[i].code === code) return LANGS[i];
    return LANGS[0];
  }
  function dictFor(lang) { var m = langMeta(lang); return DICT[lang] || DICT[m.base] || DICT.en || {}; }
  function tt(lang, key) { var d = dictFor(lang); return d[key] || (DICT.en && DICT.en[key]) || ''; }
  function flagHTML(flag, label) { return '<span class="fl">' + (flag || '') + '</span><span class="lb">' + label + '</span>'; }

  /* ---------- market: pricing + products + sponsors ---------- */
  function applyMarket(market, persist) {
    if (!REGIONS[market]) market = 'sg';
    var r = REGIONS[market];
    if (persist) { try { localStorage.setItem(MARKET_KEY, market); } catch (e) {} }
    document.querySelectorAll('.ent-price').forEach(function (el) {
      el.innerHTML = r.cur + r.ent + '<small> /yr</small>';
    });
    document.querySelectorAll('.trial-link').forEach(function (a) {
      a.setAttribute('href', 'https://www.lettaga.' + r.tld);
    });
    document.querySelectorAll('.region-label').forEach(function (el) {
      el.textContent = r.flag + ' ' + r.name;
    });
    document.querySelectorAll('[data-market]').forEach(function (el) {
      var m = el.getAttribute('data-market');
      el.style.display = (m === 'all' || m === market) ? '' : 'none';
    });
    document.querySelectorAll('.market-switch button').forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-set-market') === market);
    });
  }
  function initMarket() {
    document.querySelectorAll('.market-switch button').forEach(function (b) {
      b.addEventListener('click', function () { applyMarket(b.getAttribute('data-set-market'), true); });
    });
    var sm = storedMarket();
    if (sm) applyMarket(sm, false);
  }

  /* ---------- hero video (YouTube embed, plays inline on the page) ---------- */
  function setVideo(id) {
    var f = document.getElementById('hero-video');
    if (!f || !id) return;
    var want = 'https://www.youtube.com/embed/' + id + '?rel=0';
    if (f.getAttribute('src') !== want) f.setAttribute('src', want);
    document.querySelectorAll('.vid-langs button').forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-vid') === id);
    });
  }
  function applyVideo(lang) {
    var base = langMeta(lang).base || lang;
    setVideo(VIDEOS[lang] || VIDEOS[base] || VIDEOS.def || 'sCs9w3M_duo');
  }
  function initVideoSwitch() {
    document.querySelectorAll('.vid-langs button').forEach(function (b) {
      b.addEventListener('click', function () { setVideo(b.getAttribute('data-vid')); });
    });
  }
  function initYear() {
    var y = new Date().getFullYear();
    document.querySelectorAll('.year').forEach(function (e) { e.textContent = y; });
  }

  /* ---------- hero GIF carousel (auto-cycling product demos) ---------- */
  function initHeroGif() {
    var wrap = document.getElementById('heroGif');
    if (!wrap) return;
    var imgs = Array.prototype.slice.call(wrap.querySelectorAll('.hg-img'));
    if (imgs.length < 2) return;
    var label = document.getElementById('heroGifLabel');
    var dotsBox = document.getElementById('heroGifDots');
    var i = 0, timer = null, DELAY = 3200;
    var dots = imgs.map(function (im, idx) {
      var b = document.createElement('b');
      b.addEventListener('click', function () { go(idx); restart(); });
      if (dotsBox) dotsBox.appendChild(b);
      return b;
    });
    function go(n) {
      imgs[i].classList.remove('active'); dots[i].classList.remove('active');
      i = (n + imgs.length) % imgs.length;
      imgs[i].classList.add('active'); dots[i].classList.add('active');
      if (label) label.textContent = imgs[i].getAttribute('data-label') || '';
    }
    function next() { go(i + 1); }
    function restart() { if (timer) clearInterval(timer); timer = setInterval(next, DELAY); }
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    dots[0].classList.add('active');
    if (label) label.textContent = imgs[0].getAttribute('data-label') || '';
    if (!reduce) restart();
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { if (timer) clearInterval(timer); }
      else if (!reduce) restart();
    });
  }

  /* ---------- language ---------- */
  function applyLang(lang) {
    var meta = langMeta(lang);
    var d = dictFor(lang);
    CURRENT = lang;
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', meta.dir || 'ltr');
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var v = d[el.getAttribute('data-i18n')] || (DICT.en && DICT.en[el.getAttribute('data-i18n')]);
      if (v) el.textContent = v;
    });
    document.querySelectorAll('[data-i18n-html]').forEach(function (el) {
      var v = d[el.getAttribute('data-i18n-html')] || (DICT.en && DICT.en[el.getAttribute('data-i18n-html')]);
      if (v) el.innerHTML = v;
    });
    document.querySelectorAll('[data-logo]').forEach(function (img) {
      var src = (lang === 'ko') ? img.getAttribute('data-logo-ko') : img.getAttribute('data-logo-en');
      if (src) img.src = src;
    });

    var cur = document.querySelector('.lang-current');
    if (cur) cur.innerHTML = '<span class="fl">' + (meta.flag || '') + '</span>';
    document.querySelectorAll('.lang-menu [data-set-lang]').forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-set-lang') === lang);
    });

    var title = document.querySelector('title');
    var base = meta.base || lang;
    if (title && (title.getAttribute('data-title-' + lang) || title.getAttribute('data-title-' + base))) {
      title.textContent = title.getAttribute('data-title-' + lang) || title.getAttribute('data-title-' + base);
    }

    applyVideo(lang);
    if (!storedMarket()) applyMarket(marketForLang(lang), false);
  }

  function buildLangMenu() {
    var menu = document.querySelector('.lang-menu');
    if (!menu) return;
    menu.innerHTML = '';
    LANGS.forEach(function (l) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('data-set-lang', l.code);
      b.innerHTML = flagHTML(l.flag, l.label);
      if (l.dir === 'rtl') b.setAttribute('dir', 'rtl');
      b.addEventListener('click', function () { applyLang(l.code); menu.classList.remove('open'); });
      menu.appendChild(b);
    });
    var toggle = document.querySelector('.lang-toggle');
    if (toggle) {
      toggle.addEventListener('click', function (e) { e.stopPropagation(); menu.classList.toggle('open'); });
      document.addEventListener('click', function () { menu.classList.remove('open'); });
      menu.addEventListener('click', function (e) { e.stopPropagation(); });
    }
  }

  function detectLang() {
    var n = (navigator.language || 'en').toLowerCase();
    for (var i = 0; i < LANGS.length; i++) if (LANGS[i].code.toLowerCase() === n) return LANGS[i].code;
    if (n.indexOf('zh') === 0) {
      return (n.indexOf('tw') > -1 || n.indexOf('hk') > -1 || n.indexOf('mo') > -1 || n.indexOf('hant') > -1) ? 'zh-Hant' : 'zh-Hans';
    }
    if (n.indexOf('en') === 0) return (n.indexOf('us') > -1) ? 'en-US' : 'en-GB';
    var b = n.split('-')[0];
    for (var j = 0; j < LANGS.length; j++) if (LANGS[j].code.toLowerCase().split('-')[0] === b) return LANGS[j].code;
    return 'en-GB';
  }

  function initLang() {
    var saved = null;
    try { saved = localStorage.getItem(LANG_KEY); } catch (e) {}
    if (!saved || langMeta(saved).code !== saved) saved = detectLang();
    buildLangMenu();
    applyLang(saved);
  }

  /* ---------- Start → country chooser modal ---------- */
  function initTrialModal() {
    var links = document.querySelectorAll('.trial-link');
    if (!links.length) return;
    var modal = document.createElement('div');
    modal.className = 'cc-modal';
    modal.innerHTML =
      '<div class="cc-box"><button class="cc-close" aria-label="Close">&times;</button>' +
      '<h3 class="cc-title"></h3><div class="cc-options">' +
      '<a class="cc-opt" data-region="sg" target="_blank" rel="noopener"><span class="fg">🇸🇬</span><span>Singapore</span></a>' +
      '<a class="cc-opt" data-region="my" target="_blank" rel="noopener"><span class="fg">🇲🇾</span><span>Malaysia</span></a>' +
      '</div></div>';
    document.body.appendChild(modal);
    modal.querySelectorAll('.cc-opt').forEach(function (a) {
      var r = REGIONS[a.getAttribute('data-region')];
      a.setAttribute('href', 'https://www.lettaga.' + r.tld);
      a.addEventListener('click', function () { modal.classList.remove('open'); });
    });
    function close() { modal.classList.remove('open'); }
    modal.querySelector('.cc-close').addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        modal.querySelector('.cc-title').textContent = tt(CURRENT, 'modal.title');
        modal.classList.add('open');
      });
    });
  }

  /* ---------- customer donut gauges + count-up ---------- */
  function easeOut(p) { return 1 - Math.pow(1 - p, 3); }
  function animateCount(el, target, dur) {
    var t0 = null;
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      el.textContent = Math.round(target * easeOut(p)).toLocaleString();
      if (p < 1) requestAnimationFrame(step); else el.textContent = target.toLocaleString();
    }
    requestAnimationFrame(step);
  }
  function runGauges(scope) {
    var C = 2 * Math.PI * 52;
    scope.querySelectorAll('.ring[data-pct]').forEach(function (r) {
      var pct = parseFloat(r.getAttribute('data-pct')) || 0;
      var fg = r.querySelector('.g-fg');
      if (fg) { fg.style.strokeDasharray = C; fg.style.strokeDashoffset = C * (1 - pct / 100); }
    });
    scope.querySelectorAll('[data-count]').forEach(function (el) {
      animateCount(el, parseInt(el.getAttribute('data-count'), 10) || 0, 1300);
    });
  }
  function resetGauges(scope) {
    var C = 2 * Math.PI * 52;
    scope.querySelectorAll('.g-fg').forEach(function (fg) {
      fg.style.transition = 'none'; fg.style.strokeDasharray = C; fg.style.strokeDashoffset = C;
    });
    scope.querySelectorAll('[data-count]').forEach(function (el) { el.textContent = '0'; });
    void scope.offsetWidth;
    scope.querySelectorAll('.g-fg').forEach(function (fg) { fg.style.transition = ''; });
  }
  function initGauges() {
    var sec = document.querySelector('.cust-graph');
    if (!sec) return;
    if (!('IntersectionObserver' in window)) { runGauges(sec); return; }
    var played = false;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting && e.intersectionRatio >= 0.3) { if (!played) { played = true; runGauges(sec); } }
        else if (!e.isIntersecting) { played = false; resetGauges(sec); }
      });
    }, { threshold: [0, 0.3] });
    io.observe(sec);
  }

  /* ---------- nav / reveal ---------- */
  function initNav() {
    var toggle = document.querySelector('.nav-toggle');
    var links = document.querySelector('.nav-links');
    if (toggle && links) {
      toggle.addEventListener('click', function () { links.classList.toggle('open'); });
      links.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () { links.classList.remove('open'); });
      });
    }
  }
  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !('IntersectionObserver' in window) || !els.length) {
      els.forEach(function (e) { e.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (e) { io.observe(e); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initLang(); initMarket(); initVideoSwitch(); initHeroGif(); initTrialModal(); initGauges(); initNav(); initReveal(); initYear();
  });
})();
