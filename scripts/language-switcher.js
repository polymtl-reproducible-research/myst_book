(function () {
  'use strict';

  // === Widget dimensions (must match CSS in inject-language-switcher.py) ===
  var W = 80;
  var H = 32;
  var PAD_BOTTOM = 20;
  var PAD_RIGHT = 20;
  var PAD_BOTTOM_MOBILE = 10;
  var PAD_RIGHT_MOBILE = 10;
  var MOBILE_BREAKPOINT = 640;

  // === BASE_URL detection ===
  var baseUrl = '';
  var metaBase = document.querySelector('meta[name="base-url"]');
  if (metaBase) {
    baseUrl = metaBase.getAttribute('content').replace(/\/$/, '');
  }

  // === Language detection and navigation ===
  function isOnFrench() {
    var path = window.location.pathname;
    var frPrefix = baseUrl + '/fr';
    return path === frPrefix || path.startsWith(frPrefix + '/');
  }

  function getPageSlug() {
    var path = window.location.pathname;
    if (isOnFrench()) {
      return path.slice((baseUrl + '/fr').length) || '/';
    }
    return path.slice(baseUrl.length) || '/';
  }

  function switchTo(lang) {
    var slug = getPageSlug();
    var newPath = lang === 'fr'
      ? baseUrl + '/fr' + slug
      : baseUrl + slug;
    localStorage.setItem('myst-lang', lang);
    window.location.href = newPath;
  }

  // === Click handling via document listener (React-proof) ===
  function getWidgetBounds() {
    var isMobile = window.innerWidth <= MOBILE_BREAKPOINT;
    var padR = isMobile ? PAD_RIGHT_MOBILE : PAD_RIGHT;
    var padB = isMobile ? PAD_BOTTOM_MOBILE : PAD_BOTTOM;
    return {
      right: window.innerWidth - padR,
      bottom: window.innerHeight - padB,
      left: window.innerWidth - padR - W,
      top: window.innerHeight - padB - H
    };
  }

  document.addEventListener('click', function (e) {
    var b = getWidgetBounds();
    if (e.clientX >= b.left && e.clientX <= b.right &&
        e.clientY >= b.top && e.clientY <= b.bottom) {
      e.preventDefault();
      e.stopPropagation();
      var mid = b.left + W / 2;
      if (e.clientX < mid) {
        switchTo('en');
      } else {
        switchTo('fr');
      }
    }
  }, true);

  // === Auto-redirect based on saved preference ===
  var pref = localStorage.getItem('myst-lang');
  if (pref) {
    var onFr = isOnFrench();
    if (pref === 'fr' && !onFr) {
      switchTo('fr');
    } else if (pref === 'en' && onFr) {
      switchTo('en');
    }
  }
})();
