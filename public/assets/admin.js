(function () {
  'use strict';
  function $(s) { return document.querySelector(s); }
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  var TYPES = { quote: 'Quote', consultation: 'Consultation', survey: 'Site survey', support: 'Support' };
  var LABELS = { service: 'Service', budget: 'Budget', date: 'Date', slot: 'Time', mode: 'How', location: 'Location', property: 'Property', quantity: 'Size', urgency: 'Urgency' };
  var items = [], token = '';
  try { token = sessionStorage.getItem('bmb-admin') || ''; } catch (e) {}

  function api(opts) {
    return fetch('/api/admin/messages', Object.assign({ headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' } }, opts || {}));
  }
  function load() {
    return api().then(function (r) {
      if (r.status === 401) throw new Error('Wrong token.');
      if (!r.ok) throw new Error('Could not load enquiries (' + r.status + ').');
      return r.json();
    }).then(function (d) { items = d; $('#lg').hidden = true; $('#app').hidden = false; $('#out').hidden = false; render(); });
  }
  function render() {
    var q = $('#s').value.trim().toLowerCase(), ty = $('#ty').value, st = $('#st').value, box = $('#list');
    box.innerHTML = '';
    var rows = items.filter(function (m) {
      var status = m.status || 'new', type = m.type || 'quote';
      if (ty && type !== ty) return false;
      if (st && status !== st) return false;
      if (!q) return true;
      return [m.name, m.email, m.phone, m.message, m.service, m.location].join(' ').toLowerCase().indexOf(q) > -1;
    });
    var nNew = items.filter(function (m) { return (m.status || 'new') === 'new'; }).length;
    $('#cnt').textContent = rows.length + ' shown · ' + items.length + ' total · ' + nNew + ' new';
    if (!rows.length) box.appendChild(el('div', 'empty', 'No enquiries match.'));
    rows.forEach(function (m) {
      var status = m.status || 'new', c = el('div', 'msg' + (status === 'done' ? ' done' : ''));
      var h = el('div', 'mh'), l = el('div');
      l.appendChild(el('span', 'tg' + (status === 'new' ? ' n' : ''), status));
      l.appendChild(el('span', 'tg', TYPES[m.type || 'quote'] || 'Quote'));
      l.appendChild(el('b', '', m.name));
      h.appendChild(l); h.appendChild(el('time', '', new Date(m.createdAt).toLocaleString()));
      c.appendChild(h);
      var kv = el('div', 'kv');
      Object.keys(LABELS).forEach(function (k) {
        var v = k === 'service' || k === 'budget' ? m[k] : (m.details || {})[k];
        if (v && v !== 'Not specified') { var s = el('span'); s.appendChild(el('b', '', LABELS[k] + ': ')); s.appendChild(document.createTextNode(v)); kv.appendChild(s); }
      });
      c.appendChild(kv);
      if (m.message) c.appendChild(el('pre', '', m.message));
      var a = el('div', 'ma');
      if (m.email) { var e1 = el('a', 'lk', 'Email'); e1.href = 'mailto:' + m.email; a.appendChild(e1); }
      if (m.phone) {
        var t = el('a', 'lk', 'Call'); t.href = 'tel:' + m.phone.replace(/\s/g, ''); a.appendChild(t);
        var w = el('a', 'lk', 'WhatsApp'); w.href = 'https://wa.me/' + m.phone.replace(/\D/g, ''); w.target = '_blank'; w.rel = 'noopener'; a.appendChild(w);
      }
      var b = el('button', 'lk', status === 'done' ? 'Mark as new' : 'Mark as done');
      b.addEventListener('click', function () {
        var next = status === 'done' ? 'new' : 'done'; b.disabled = true;
        api({ method: 'PATCH', body: JSON.stringify({ key: m.key, status: next }) }).then(function (r) {
          if (!r.ok) throw new Error(); m.status = next; render();
        }).catch(function () { b.disabled = false; alert('Could not update. Try again.'); });
      });
      a.appendChild(b); c.appendChild(a); box.appendChild(c);
    });
  }
  $('#lg').addEventListener('submit', function (e) {
    e.preventDefault(); token = $('#tk').value.trim(); $('#lgm').textContent = 'Checking...';
    load().then(function () { try { sessionStorage.setItem('bmb-admin', token); } catch (x) {} })
      .catch(function (x) { $('#lgm').className = 'ok bad'; $('#lgm').textContent = x.message; });
  });
  $('#out').addEventListener('click', function () { try { sessionStorage.removeItem('bmb-admin'); } catch (e) {} location.reload(); });
  ['#s', '#ty', '#st'].forEach(function (s) { $(s).addEventListener('input', render); });
  $('#rf').addEventListener('click', function () { load().catch(function () {}); });
  if (token) load().catch(function () { try { sessionStorage.removeItem('bmb-admin'); } catch (e) {} });
})();
