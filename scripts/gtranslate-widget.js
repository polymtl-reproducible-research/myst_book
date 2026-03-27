(function () {
  // Guard: don't double-initialize
  if (document.getElementById('gtranslate-fixed-widget')) return;

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

  // 1. Create hidden Google Translate element on <body>
  var gtel = document.createElement('div');
  gtel.id = 'google_translate_element';
  gtel.style.display = 'none';
  document.body.appendChild(gtel);

  // 2. Create fixed widget on <html> (outside React and Google Translate scope)
  var widget = document.createElement('div');
  widget.id = 'gtranslate-fixed-widget';

  var enLink = document.createElement('a');
  enLink.innerHTML = ukFlag;
  enLink.title = 'English';
  enLink.dataset.lang = 'en';
  enLink.className = 'active';
  enLink.onclick = function (e) {
    e.preventDefault();
    doTranslate('en');
  };

  var frLink = document.createElement('a');
  frLink.innerHTML = qcFlag;
  frLink.title = 'Français';
  frLink.dataset.lang = 'fr';
  frLink.onclick = function (e) {
    e.preventDefault();
    doTranslate('fr');
  };

  widget.appendChild(enLink);
  widget.appendChild(frLink);
  document.documentElement.appendChild(widget);

  // 3. Load Google Translate API
  window.googleTranslateElementInit = function () {
    new google.translate.TranslateElement(
      {
        pageLanguage: 'en',
        includedLanguages: 'en,fr',
        autoDisplay: false,
      },
      'google_translate_element'
    );
  };

  var script = document.createElement('script');
  script.src =
    'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
  document.head.appendChild(script);

  // 4. Translation functions
  function doTranslate(lang) {
    var combo = document.querySelector('.goog-te-combo');
    if (!combo) {
      // Bounded retry: wait for Google Translate API to load
      var attempts = 0;
      var interval = setInterval(function () {
        combo = document.querySelector('.goog-te-combo');
        attempts++;
        if (combo) {
          clearInterval(interval);
          applyTranslation(combo, lang);
        } else if (attempts >= 6) {
          clearInterval(interval);
        }
      }, 500);
      return;
    }
    applyTranslation(combo, lang);
  }

  function applyTranslation(combo, lang) {
    combo.value = lang;
    combo.dispatchEvent(new Event('change'));
    updateFlags(lang);
    if (lang === 'fr') {
      setTimeout(applyCorrections, 1500);
      setTimeout(applyCorrections, 3000);
    }
  }

  function updateFlags(lang) {
    var flags = document.getElementById('gtranslate-fixed-widget');
    if (!flags) return;
    var links = flags.querySelectorAll('a');
    for (var i = 0; i < links.length; i++) {
      if (links[i].dataset.lang === lang) {
        links[i].classList.add('active');
      } else {
        links[i].classList.remove('active');
      }
    }
  }

  // 5. Translation corrections dictionary
  var corrections = {
    Cahiers: 'Carnets',
  };

  function applyCorrections() {
    var walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT
    );
    while (walker.nextNode()) {
      var node = walker.currentNode;
      var text = node.textContent;
      for (var wrong in corrections) {
        if (text.indexOf(wrong) !== -1) {
          node.textContent = text.replace(
            new RegExp(wrong, 'g'),
            corrections[wrong]
          );
        }
      }
    }
  }

  // 6. Check cookie for existing translation state
  function getTranslateCookie() {
    var match = document.cookie.match(/googtrans=\/en\/(\w+)/);
    return match ? match[1] : 'en';
  }

  var currentLang = getTranslateCookie();
  if (currentLang !== 'en') {
    updateFlags(currentLang);
  }
})();
