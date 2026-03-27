#!/usr/bin/env python3
"""Inject Google Translate with custom flag buttons into all built HTML files."""

import glob
import os

SNIPPET = r"""
<!-- Google Translate with Custom Flags -->
<div id="google_translate_element" style="display:none;"></div>
<script>
  function googleTranslateElementInit() {
    new google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: 'en,fr',
      autoDisplay: false
    }, 'google_translate_element');
  }
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
<style>
  #gtranslate-flags {
    display: flex !important;
    flex-direction: row !important;
    gap: 8px;
    padding: 8px 12px;
    margin: 0 12px 8px 12px;
    align-items: center;
  }
  #gtranslate-flags a {
    cursor: pointer;
    display: inline-block;
    line-height: 0;
    opacity: 0.5;
    transition: opacity 0.2s;
    border: 2px solid transparent;
    border-radius: 3px;
    padding: 1px;
  }
  #gtranslate-flags a:hover { opacity: 1; }
  #gtranslate-flags a.active { opacity: 1; border-color: #3b82f6; }
  /* Keep Google Translate bar visible */
  body { top: 0 !important; }
</style>
<script>
(function() {
  var ukFlag = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 60 40" style="border-radius:2px;"><rect width="60" height="40" fill="#012169"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="8"/><path d="M0,0 L60,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,60 0,60 40,30 20,0 40)"/><path d="M60,0 L0,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,0 40,60 40,30 20,60 0)"/><path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="12"/><path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/></svg>';
  var qcFlag = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 24 16" style="border-radius:2px;"><rect width="24" height="16" fill="#003DA5"/><rect x="10" y="0" width="4" height="16" fill="#fff"/><rect x="0" y="6" width="24" height="4" fill="#fff"/><text x="5" y="5.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text><text x="15" y="5.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text><text x="5" y="13.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text><text x="15" y="13.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text></svg>';

  function doTranslate(lang) {
    var combo = document.querySelector('.goog-te-combo');
    if (!combo) {
      setTimeout(function() { doTranslate(lang); }, 500);
      return;
    }
    combo.value = lang;
    combo.dispatchEvent(new Event('change'));
    updateFlags(lang);
    if (lang === 'fr') {
      setTimeout(applyCorrections, 1500);
      setTimeout(applyCorrections, 3000);
    }
  }

  // Dictionary of translation corrections: wrong -> correct
  var corrections = {
    'Chapitres': 'Chapitres',
    'Cahiers': 'Carnets',
    // Add more corrections here, e.g.:
    // 'wrong translation': 'correct translation',
  };

  function applyCorrections() {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      var node = walker.currentNode;
      var text = node.textContent;
      for (var wrong in corrections) {
        if (text.indexOf(wrong) !== -1) {
          node.textContent = text.replace(new RegExp(wrong, 'g'), corrections[wrong]);
        }
      }
    }
  }

  function updateFlags(lang) {
    var flags = document.getElementById('gtranslate-flags');
    if (!flags) return;
    flags.querySelectorAll('a').forEach(function(a) {
      a.classList.toggle('active', a.dataset.lang === lang);
    });
  }

  function injectFlags() {
    if (document.getElementById('gtranslate-flags')) return;

    var container = document.createElement('div');
    container.id = 'gtranslate-flags';

    var enLink = document.createElement('a');
    enLink.innerHTML = ukFlag;
    enLink.title = 'English';
    enLink.dataset.lang = 'en';
    enLink.className = 'active';
    enLink.onclick = function(e) { e.preventDefault(); doTranslate('en'); };

    var frLink = document.createElement('a');
    frLink.innerHTML = qcFlag;
    frLink.title = 'Français';
    frLink.dataset.lang = 'fr';
    frLink.onclick = function(e) { e.preventDefault(); doTranslate('fr'); };

    container.appendChild(enLink);
    container.appendChild(frLink);

    var sidebar = document.querySelector('.myst-toc');
    if (sidebar) {
      sidebar.insertBefore(container, sidebar.firstChild);
    } else {
      container.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:10000;display:flex;gap:5px;background:rgba(255,255,255,0.95);border-radius:8px;padding:6px 10px;box-shadow:0 2px 8px rgba(0,0,0,0.2);';
      document.body.appendChild(container);
    }
  }

  var observer = new MutationObserver(function() {
    if (!document.getElementById('gtranslate-flags')) {
      injectFlags();
    }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(injectFlags, 500);
      observer.observe(document.body, { childList: true, subtree: true });
    });
  } else {
    setTimeout(injectFlags, 500);
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
</script>
<!-- End Google Translate with Custom Flags -->
"""

BUILD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "_build", "html")


def inject():
    html_files = glob.glob(os.path.join(BUILD_DIR, "**", "*.html"), recursive=True)
    count = 0
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "gtranslate-flags" in content:
            continue
        if "</body>" in content:
            content = content.replace("</body>", SNIPPET + "\n</body>")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
    print(f"Injected Google Translate widget into {count} HTML file(s)")


if __name__ == "__main__":
    inject()
