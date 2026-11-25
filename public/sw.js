/* Simple offline cache: pages are fetched fresh when online, and fall back to the saved copy when offline. */
var V = 'bmb-v2';
var CORE = ['/', '/services.html', '/packages.html', '/portfolio.html', '/solutions.html', '/process.html', '/contact.html',
  '/assets/style.css', '/assets/app.js', '/assets/site-data.js', '/assets/search-index.js', '/favicon.svg', '/assets/nexora-logo.svg', '/assets/bg-tech-team.jpg', '/assets/bg-tech-office.jpg', '/assets/service-web.jpg', '/assets/service-branding.jpg', '/assets/service-video.jpg', '/assets/service-it-support.jpg', '/assets/service-cctv.jpg', '/assets/service-networking.jpg', '/assets/service-marketing.jpg', '/assets/service-software.jpg', '/assets/service-training.jpg', '/assets/service-printing.jpg', '/assets/service-data-recovery.jpg', '/assets/service-consultancy.jpg', '/assets/service-email.jpg', '/assets/service-hosting.jpg'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(V).then(function (c) {
    return Promise.all(CORE.map(function (u) { return c.add(u).catch(function () {}); }));
  }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k !== V; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener('fetch', function (e) {
  var r = e.request, u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin || u.pathname.indexOf('/api/') === 0 || u.pathname === '/admin.html' || u.pathname === '/assets/admin.js') return;
  var isPage = r.mode === 'navigate' || (r.headers.get('accept') || '').indexOf('text/html') > -1;
  if (isPage) {
    e.respondWith(fetch(r).then(function (res) {
      var copy = res.clone(); caches.open(V).then(function (c) { c.put(r, copy); }); return res;
    }).catch(function () { return caches.match(r).then(function (m) { return m || caches.match('/'); }); }));
  } else {
    e.respondWith(caches.match(r).then(function (m) {
      var net = fetch(r).then(function (res) { var copy = res.clone(); caches.open(V).then(function (c) { c.put(r, copy); }); return res; }).catch(function () { return m; });
      return m || net;
    }));
  }
});

