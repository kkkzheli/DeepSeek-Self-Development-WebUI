// DeepSeek Research — offline service worker
const CACHE = 'deepseek-rsi-v2';
const ASSETS = [
  './index.html',
  './manifest.webmanifest',
  './icon.svg',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll(ASSETS);
    }).then(function() { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(keys.filter(function(k) { return k !== CACHE; })
        .map(function(k) { return caches.delete(k); }));
    }).then(function() { return self.clients.claim(); })
  );
});

// Network-first for navigation (always freshest page), cache-first for assets
self.addEventListener('fetch', function(e) {
  const url = new URL(e.request.url);
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).then(function(res) {
        if (res && res.status === 200) {
          const copy = res.clone();
          caches.open(CACHE).then(function(cache) {
            cache.put('./index.html', copy);
            cache.put('./', copy);
          });
        }
        return res;
      }).catch(function() {
        return caches.match('./index.html').then(function(cached) {
          return cached || caches.match('./');
        });
      })
    );
    return;
  }
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      return cached || fetch(e.request).then(function(res) {
        if (res && res.status === 200 && url.origin === location.origin) {
          const copy = res.clone();
          caches.open(CACHE).then(function(cache) { cache.put(e.request, copy); });
        }
        return res;
      });
    })
  );
});
