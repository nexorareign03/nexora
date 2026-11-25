(function () {
  'use strict';
  var S = window.SITE || {}, C = S.CONTACT || {}, CUR = S.CUR || 'GHS';
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  function digits(v) { return String(v || '').replace(/\D/g, ''); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  var HAS_WA = !!digits(C.whatsapp);
  function waUrl(m) { return HAS_WA ? 'https://wa.me/' + digits(C.whatsapp) + '?text=' + encodeURIComponent(m || '') : 'contact.html'; }

  /* ---------- theme ---------- */
  var th = $('#th');
  if (th) th.addEventListener('click', function () {
    var r = document.documentElement, dark = r.dataset.theme ? r.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    r.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('bmb-theme', r.dataset.theme); } catch (e) {}
  });

  /* ---------- mobile menu ---------- */
  var bg = $('#bg'), dr = $('#dr');
  if (bg && dr) bg.addEventListener('click', function () {
    var open = dr.hidden; dr.hidden = !open; bg.setAttribute('aria-expanded', open);
  });

  /* ---------- contact details + WhatsApp links ---------- */
  $$('[data-wa]').forEach(function (a) {
    a.href = waUrl(a.getAttribute('data-wa') || 'Hello Nexora Technologies, I would like to know more about your services.');
    if (HAS_WA) { a.target = '_blank'; a.rel = 'noopener'; }
  });
  $$('[data-ct]').forEach(function (n) {
    var k = n.getAttribute('data-ct'), v = C[k], row = n.closest('.ctr') || n;
    if (!v) { row.hidden = true; return; }
    if (k === 'whatsapp') v = '+' + digits(v);
    n.textContent = v;
    if (n.tagName === 'A') n.href = k === 'email' ? 'mailto:' + C.email : k === 'phone' ? 'tel:' + String(C.phone).replace(/\s/g, '') : waUrl('');
  });
  $$('[data-ctgroup]').forEach(function (g) {
    var any = $$('.ctr', g).some(function (r) { return !r.hidden; });
    var none = $('.ct-none', g); if (none) none.hidden = any;
  });
  $$('[data-needwa]').forEach(function (n) { if (!HAS_WA) n.hidden = true; });

  /* ---------- search ---------- */
  function bindSearch(form) {
    var inp = $('.qin', form), box = $('.qr', form), idx = window.SEARCH || [];
    function run() {
      var q = inp.value.trim().toLowerCase(); box.innerHTML = '';
      if (q.length < 2) { box.hidden = true; return; }
      var hits = idx.filter(function (i) { return (i.t + ' ' + i.k).toLowerCase().indexOf(q) > -1; }).slice(0, 6);
      if (!hits.length) { box.appendChild(el('p', '', 'No match. Try “website”, “CCTV” or “Wi-Fi”.')); }
      hits.forEach(function (h) { var a = el('a'); a.href = h.u; a.appendChild(document.createTextNode(h.t)); a.appendChild(el('small', '', h.c)); box.appendChild(a); });
      box.hidden = false;
    }
    inp.addEventListener('input', run);
    form.addEventListener('submit', function (e) { e.preventDefault(); run(); var a = $('a', box); if (a && e.submitter !== null) a.focus(); });
    $('.qb', form).addEventListener('click', function () { run(); });
    document.addEventListener('click', function (e) { if (!form.contains(e.target)) box.hidden = true; });
  }
  $$('.qf').forEach(bindSearch);

  /* ---------- scroll reveal ---------- */
  var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function (es) {
    es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
  }, { threshold: .1 }) : null;
  $$('.rv').forEach(function (n) { io ? io.observe(n) : n.classList.add('in'); });

  /* ---------- portfolio, testimonials, clients ---------- */
  function projectCard(p) {
    var c = el('article', 'pc ctr'), im = el('div', 'im');
    if (p.image) im.style.backgroundImage = 'url("' + String(p.image).replace(/"/g, '') + '")';
    if (p.category) c.appendChild(el('span', 'badge', p.category));
    c.appendChild(im);
    var tx = el('div', 'tx'); tx.appendChild(el('h3', '', p.title || 'Project'));
    if (p.summary) tx.appendChild(el('p', '', p.summary));
    if (p.result) tx.appendChild(el('p', '', p.result)).style.marginTop = '8px';
    c.appendChild(tx); return c;
  }
  var P = S.PROJECTS || [], T = S.TESTIMONIALS || [], CL = S.CLIENTS || [];
  var pg = $('#proj-grid'); if (pg) { if (P.length) { P.forEach(function (p) { pg.appendChild(projectCard(p)); }); var pe = $('#proj-empty'); if (pe) pe.hidden = true; } else { pg.hidden = true; } }
  var ph = $('#proj-home'); if (ph && P.length) { ph.hidden = false; var g = $('.cards', ph); P.slice(0, 4).forEach(function (p) { g.appendChild(projectCard(p)); }); }
  var tm = $('#tm'); if (tm && T.length) { tm.hidden = false; var tg = $('.tms', tm); T.forEach(function (t) { var d = el('div', 'tm'); d.appendChild(el('q', '', t.quote)); d.appendChild(el('b', '', t.name)); if (t.role) d.appendChild(el('span', '', t.role)); tg.appendChild(d); }); }
  var cl = $('#cl'); if (cl && CL.length) { cl.hidden = false; var cg = $('.cl', cl); CL.forEach(function (c) { if (typeof c === 'string') cg.appendChild(el('span', '', c)); else if (c.logo) { var i = el('img'); i.src = c.logo; i.alt = c.name || ''; i.loading = 'lazy'; cg.appendChild(i); } else cg.appendChild(el('span', '', c.name)); }); }

  /* ---------- forms ---------- */
  var LISTS = {
    service: ['Website design & development', 'Graphic design & branding', 'Multimedia & video editing', 'Computer & IT support', 'CCTV & security systems', 'Networking services', 'Digital marketing', 'Software & application development', 'Additional services', 'Not sure yet'],
    budget: [CUR + ' 1,000 – 5,000', CUR + ' 5,000 – 15,000', CUR + ' 15,000 – 50,000', CUR + ' 50,000+', 'Not sure yet, I need a quote'],
    slot: ['Morning', 'Afternoon', 'Evening'],
    mode: ['WhatsApp call', 'Phone call', 'Video call', 'In person'],
    survey: ['CCTV installation', 'Wi-Fi / network setup', 'Access control', 'Other'],
    property: ['Home', 'Office', 'School', 'Shop / retail', 'Other'],
    issue: ['Computer or laptop', 'Wi-Fi / internet', 'CCTV / cameras', 'Printer', 'Email / accounts', 'Software', 'Other'],
    urgency: ['Not urgent', 'Soon', 'Urgent']
  };
  $$('select[data-list]').forEach(function (s) {
    var ph = s.getAttribute('data-ph');
    if (ph) { var o = el('option', '', ph); o.value = ''; s.appendChild(o); }
    LISTS[s.getAttribute('data-list')].forEach(function (v) { var o = el('option', '', v); o.value = v; s.appendChild(o); });
  });
  var tomorrow = new Date(Date.now() + 864e5), iso = tomorrow.getFullYear() + '-' + ('0' + (tomorrow.getMonth() + 1)).slice(-2) + '-' + ('0' + tomorrow.getDate()).slice(-2);
  $$('input[type=date]').forEach(function (i) { i.min = iso; });

  var qp = new URLSearchParams(location.search), pre = qp.get('service'), qs = $('select[name=service][data-list=service]', $('form[data-type=quote]') || document);
  if (pre && qs) qs.value = pre;

  var LABEL = { name: 'Name', email: 'Email', phone: 'Phone', service: 'Service', budget: 'Budget', date: 'Preferred date', slot: 'Time', mode: 'How', location: 'Location', property: 'Property', quantity: 'Size', urgency: 'Urgency', message: 'Details' };
  var INTRO = { quote: 'I would like a quote.', consultation: 'I would like to book a consultation.', survey: 'I would like to request a site survey.', support: 'I need IT support.' };
  function waMsg(d) {
    var lines = ['Hello Nexora Technologies, ' + INTRO[d.type]];
    ['name', 'email', 'phone', 'service', 'budget', 'date', 'slot', 'mode', 'location', 'property', 'quantity', 'urgency', 'message'].forEach(function (k) { if (d[k]) lines.push(LABEL[k] + ': ' + d[k]); });
    return lines.join('\n');
  }
  function formData(f) { var d = {}; new FormData(f).forEach(function (v, k) { d[k] = v; }); d.type = f.getAttribute('data-type'); return d; }

  $$('form.fm').forEach(function (f) {
    var ok = $('.ok', f), btn = $('button[type=submit]', f), wo = $('.waonly', f);
    if (wo) wo.addEventListener('click', function () { window.open(waUrl(waMsg(formData(f))), '_blank', 'noopener'); });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = formData(f); ok.className = 'ok';
      if (!d.email && !d.phone) { ok.className = 'ok bad'; ok.textContent = 'Please add an email address or a phone number so we can reply.'; return; }
      var bw = $('.bw', f), both = HAS_WA && bw && bw.checked, w = both ? window.open('', '_blank') : null;
      function done(msg, good) { ok.className = 'ok ' + (good ? 'good' : 'bad'); ok.textContent = msg; if (w) w.location.href = waUrl(waMsg(d)); }
      btn.disabled = true; ok.textContent = 'Sending...';
      fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (x) {
          if (x.ok) { f.reset(); done('Thanks, we have received your request.' + (both ? ' Tap send in WhatsApp to finish.' : ''), true); }
          else done((x.j.error || 'We could not send your message.') + (HAS_WA ? ' You can still send it on WhatsApp.' : ''), false);
        })
        .catch(function () { done('Network error. ' + (HAS_WA ? 'You can still send it on WhatsApp.' : 'Please try again.'), false); })
        .then(function () { btn.disabled = false; });
    });
  });

  /* ---------- contact tabs ---------- */
  var tabs = $$('.ft');
  if (tabs.length) {
    var names = tabs.map(function (t) { return t.getAttribute('data-t'); });
    function showTab(n) {
      if (names.indexOf(n) < 0) n = 'quote';
      tabs.forEach(function (t) { var on = t.getAttribute('data-t') === n; t.classList.toggle('on', on); t.setAttribute('aria-selected', on); });
      $$('.fp').forEach(function (p) { p.hidden = p.getAttribute('data-p') !== n; });
    }
    tabs.forEach(function (t) { t.addEventListener('click', function () { var n = t.getAttribute('data-t'); showTab(n); history.replaceState(null, '', '#' + n); }); });
    window.addEventListener('hashchange', function () { showTab(location.hash.slice(1)); });
    showTab(location.hash.slice(1));
  }

  /* ---------- offline support ---------- */
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', function () { navigator.serviceWorker.register('/sw.js').catch(function () {}); });
  }
})();
