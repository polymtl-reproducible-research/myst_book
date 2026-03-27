(function () {
  'use strict';

  // === Flag SVGs as data URIs ===
  var ukSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 60 40">' +
    '<rect width="60" height="40" fill="%23012169"/>' +
    '<path d="M0,0 L60,40 M60,0 L0,40" stroke="%23fff" stroke-width="8"/>' +
    '<path d="M0,0 L60,40" stroke="%23C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,60 0,60 40,30 20,0 40)"/>' +
    '<path d="M60,0 L0,40" stroke="%23C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,0 40,60 40,30 20,60 0)"/>' +
    '<path d="M30,0 V40 M0,20 H60" stroke="%23fff" stroke-width="12"/>' +
    '<path d="M30,0 V40 M0,20 H60" stroke="%23C8102E" stroke-width="6"/>' +
    '</svg>';
  var ukUri = 'data:image/svg+xml,' + ukSvg;

  var qcSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 24 16">' +
    '<rect width="24" height="16" fill="%23003DA5"/>' +
    '<rect x="10" y="0" width="4" height="16" fill="%23fff"/>' +
    '<rect x="0" y="6" width="24" height="4" fill="%23fff"/>' +
    '<text x="5" y="5.5" font-size="5" fill="%23fff" font-family="serif">⚜</text>' +
    '<text x="15" y="5.5" font-size="5" fill="%23fff" font-family="serif">⚜</text>' +
    '<text x="5" y="13.5" font-size="5" fill="%23fff" font-family="serif">⚜</text>' +
    '<text x="15" y="13.5" font-size="5" fill="%23fff" font-family="serif">⚜</text>' +
    '</svg>';
  var qcUri = 'data:image/svg+xml,' + qcSvg;

  // === Widget dimensions (must match CSS below) ===
  var W = 80;    // total width
  var H = 32;    // total height
  var PAD_BOTTOM = 20;
  var PAD_RIGHT = 20;
  var PAD_BOTTOM_MOBILE = 10;
  var PAD_RIGHT_MOBILE = 10;
  var MOBILE_BREAKPOINT = 640;

  // === CSS for the widget (body::after pseudo-element) ===
  var css = [
    'body::after {',
    '  content: "";',
    '  position: fixed;',
    '  bottom: ' + PAD_BOTTOM + 'px;',
    '  right: ' + PAD_RIGHT + 'px;',
    '  z-index: 2147483647;',
    '  display: block;',
    '  width: ' + W + 'px;',
    '  height: ' + H + 'px;',
    '  background-color: rgba(255, 255, 255, 0.95);',
    '  background-image: url("' + ukUri + '"), url("' + qcUri + '");',
    '  background-repeat: no-repeat, no-repeat;',
    '  background-position: 8px center, 48px center;',
    '  background-size: 24px 16px, 24px 16px;',
    '  border-radius: 8px;',
    '  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);',
    '  cursor: pointer;',
    '  pointer-events: auto;',
    '}',
    '.dark body::after, html.dark body::after {',
    '  background-color: rgba(30, 30, 30, 0.95);',
    '  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);',
    '}',
    '@media (max-width: ' + MOBILE_BREAKPOINT + 'px) {',
    '  body::after {',
    '    bottom: ' + PAD_BOTTOM_MOBILE + 'px;',
    '    right: ' + PAD_RIGHT_MOBILE + 'px;',
    '  }',
    '}',
  ].join('\n');

  // === Attach CSS via adoptedStyleSheets (React-proof) ===
  var sheet = null;

  function applyStyles() {
    if (typeof CSSStyleSheet === 'function' && 'adoptedStyleSheets' in document) {
      // Modern browsers: attach stylesheet to Document object (not a DOM node)
      if (!sheet) {
        sheet = new CSSStyleSheet();
        sheet.replaceSync(css);
      }
      var existing = Array.prototype.slice.call(document.adoptedStyleSheets);
      if (existing.indexOf(sheet) === -1) {
        document.adoptedStyleSheets = existing.concat([sheet]);
      }
    } else {
      // Fallback: create <style> element
      if (!document.getElementById('lang-switcher-style')) {
        var style = document.createElement('style');
        style.id = 'lang-switcher-style';
        style.textContent = css;
        document.head.appendChild(style);
      }
    }
  }

  // Belt-and-suspenders: re-apply styles every frame in case anything clears them
  function styleLoop() {
    applyStyles();
    requestAnimationFrame(styleLoop);
  }

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
      top: window.innerHeight - padB - H,
    };
  }

  document.addEventListener('click', function (e) {
    var b = getWidgetBounds();
    if (e.clientX >= b.left && e.clientX <= b.right &&
        e.clientY >= b.top && e.clientY <= b.bottom) {
      e.preventDefault();
      e.stopPropagation();
      // Left half = EN flag, right half = FR flag
      var mid = b.left + W / 2;
      if (e.clientX < mid) {
        switchTo('en');
      } else {
        switchTo('fr');
      }
    }
  }, true); // capture phase — fires before React

  // === Auto-redirect based on saved preference ===
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

  // === Initialize ===
  applyStyles();
  requestAnimationFrame(styleLoop);
  autoRedirect();
})();
