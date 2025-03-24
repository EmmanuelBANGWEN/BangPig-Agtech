self.addEventListener("install", (event) => {
    console.log("Service Worker installé");
    event.waitUntil(
        caches.open("v1").then((cache) => {
            return cache.addAll([
                "home/",
                "/static/assets/img/icon-192.png",
                "/static/assets/img/icon-512.png",
                // Ajoute d'autres fichiers statiques nécessaires
            ]);
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            return cachedResponse || fetch(event.request);
        })
    );
});












// self.addEventListener('install', function(event) {
//     event.waitUntil(
//       caches.open('pwa-cache').then(function(cache) {
//         return cache.addAll([
//           '/', // URL de la page d'accueil
//           '/static/css/base.css', // votre fichier CSS
//           '/static/js/base.js', // votre fichier JS
//           '/static/assets/img/gg.png', // votre icône
//         ]);
//       })
//     );
//   });
  
//   self.addEventListener('fetch', function(event) {
//     event.respondWith(
//       caches.match(event.request).then(function(response) {
//         return response || fetch(event.request);
//       })
//     );
//   });
  

