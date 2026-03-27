(function () {
  var ukFlag =
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 60 40" style="border-radius:2px;">' +
    '<rect width="60" height="40" fill="#012169"/>' +
    '<path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="8"/>' +
    '<path d="M0,0 L60,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,60 0,60 40,30 20,0 40)"/>' +
    '<path d="M60,0 L0,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,0 40,60 40,30 20,60 0)"/>' +
    '<path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="12"/>' +
    '<path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/>' +
    '</svg>';

  var qcFlag =
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 24 16" style="border-radius:2px;">' +
    '<rect width="24" height="16" fill="#003DA5"/>' +
    '<rect x="10" y="0" width="4" height="16" fill="#fff"/>' +
    '<rect x="0" y="6" width="24" height="4" fill="#fff"/>' +
    '<text x="5" y="5.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text>' +
    '<text x="15" y="5.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text>' +
    '<text x="5" y="13.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text>' +
    '<text x="15" y="13.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text>' +
    '</svg>';

  // Detect BASE_URL from a meta tag
  var baseUrl = '';
  var metaBase = document.querySelector('meta[name="base-url"]');
  if (metaBase) {
    baseUrl = metaBase.getAttribute('content').replace(/\/$/, '');
  }

  function isOnFrench() {
    var path = window.location.pathname;
    var frPrefix = baseUrl + '/fr';
    return path === frPrefix || path.startsWith(frPrefix + '/');
  }

  function getPageSlug() {
    var path = window.location.pathname;
    if (isOnFrench()) {
      var frPrefix = baseUrl + '/fr';
      return path.slice(frPrefix.length) || '/';
    }
    return path.slice(baseUrl.length) || '/';
  }

  function switchTo(lang) {
    var slug = getPageSlug();
    var newPath;
    if (lang === 'fr') {
      newPath = baseUrl + '/fr' + slug;
    } else {
      newPath = baseUrl + slug;
    }
    localStorage.setItem('myst-lang', lang);
    window.location.href = newPath;
  }

  // Build the widget element (without inserting it)
  function buildWidget() {
    var currentLang = isOnFrench() ? 'fr' : 'en';

    var widget = document.createElement('div');
    widget.id = 'lang-switcher-widget';

    var enLink = document.createElement('a');
    enLink.innerHTML = ukFlag;
    enLink.title = 'English';
    enLink.setAttribute('role', 'button');
    enLink.setAttribute('aria-label', 'Switch to English');
    if (currentLang === 'en') enLink.className = 'active';
    enLink.onclick = function (e) {
      e.preventDefault();
      if (currentLang !== 'en') switchTo('en');
    };

    var frLink = document.createElement('a');
    frLink.innerHTML = qcFlag;
    frLink.title = 'Français';
    frLink.setAttribute('role', 'button');
    frLink.setAttribute('aria-label', 'Passer au français');
    if (currentLang === 'fr') frLink.className = 'active';
    frLink.onclick = function (e) {
      e.preventDefault();
      if (currentLang !== 'fr') switchTo('fr');
    };

    widget.appendChild(enLink);
    widget.appendChild(frLink);
    return widget;
  }

  function ensureWidget() {
    if (!document.body) return;
    if (document.getElementById('lang-switcher-widget')) return;
    document.body.appendChild(buildWidget());
  }

  // MutationObserver: fires synchronously before next paint when React
  // removes our widget, so we can re-append it with zero visible flicker.
  var observer = new MutationObserver(function () {
    if (!document.getElementById('lang-switcher-widget')) {
      ensureWidget();
    }
  });

  function startObserver() {
    observer.observe(document.body, { childList: true, subtree: true });
  }

  // Backup interval in case MutationObserver misses an edge case
  setInterval(ensureWidget, 500);

  // Auto-redirect based on saved preference (only on first page load)
  function autoRedirect() {
    var pref = localStorage.getItem('myst-lang');
    if (!pref) return;
    var onFr = isOnFrench();
    if (pref === 'fr' && !onFr) {
      switchTo('fr');
    } else if (pref === 'en' && onFr) {
      switchTo('en');
    }
  }

  // Initialize
  if (document.body) {
    ensureWidget();
    startObserver();
    autoRedirect();
  } else {
    document.addEventListener('DOMContentLoaded', function () {
      ensureWidget();
      startObserver();
      autoRedirect();
    });
  }
})();
