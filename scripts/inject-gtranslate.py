#!/usr/bin/env python3
"""Inject LibreTranslate EN/FR widget into all built HTML files."""

import glob
import os

SNIPPET = r"""
<!-- LibreTranslate EN/FR Widget -->
<style>
  #translate-widget {
    display: flex;
    gap: 8px;
    padding: 8px 12px;
    margin: 0 12px 8px 12px;
    align-items: center;
  }
  #translate-widget a {
    cursor: pointer;
    display: inline-block;
    line-height: 0;
    opacity: 0.5;
    transition: opacity 0.2s;
    border: 2px solid transparent;
    border-radius: 3px;
    padding: 1px;
  }
  #translate-widget a:hover { opacity: 1; }
  #translate-widget a.active { opacity: 1; border-color: #3b82f6; }
  #translate-spinner {
    display: none;
    width: 14px;
    height: 14px;
    border: 2px solid #ccc;
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
<script>
(function() {
  var LIBRE_API = 'https://translate.fedilab.app';
  var currentLang = 'fr';
  var originalTexts = new Map();

  var ukFlag = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 60 40" style="border-radius:2px;"><rect width="60" height="40" fill="#012169"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="8"/><path d="M0,0 L60,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,60 0,60 40,30 20,0 40)"/><path d="M60,0 L0,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,0 40,60 40,30 20,60 0)"/><path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="12"/><path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/></svg>';
  var qcFlag = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 24 16" style="border-radius:2px;"><rect width="24" height="16" fill="#003DA5"/><rect x="10" y="0" width="4" height="16" fill="#fff"/><rect x="0" y="6" width="24" height="4" fill="#fff"/><text x="5" y="5.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text><text x="15" y="5.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text><text x="5" y="13.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text><text x="15" y="13.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text></svg>';

  function getTextNodes(root) {
    var nodes = [];
    var walker = document.createTreeWalker(
      root, NodeFilter.SHOW_TEXT,
      { acceptNode: function(n) {
        if (!n.textContent.trim()) return NodeFilter.FILTER_REJECT;
        var tag = n.parentElement.tagName;
        if (['SCRIPT','STYLE','CODE','PRE','KBD','SVG','MATH'].indexOf(tag) >= 0) return NodeFilter.FILTER_REJECT;
        if (n.parentElement.closest('svg, math, .katex, code, pre, script, style, #translate-widget')) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }}
    );
    while (walker.nextNode()) nodes.push(walker.currentNode);
    return nodes;
  }

  function translatePage(targetLang) {
    if (targetLang === currentLang) return;

    var article = document.body;
    var spinner = document.getElementById('translate-spinner');

    if (targetLang === 'en') {
      // Restore originals
      originalTexts.forEach(function(orig, node) {
        if (node.parentNode) node.textContent = orig;
      });
      currentLang = 'en';
      updateActiveFlag();
      return;
    }

    var textNodes = getTextNodes(article);
    // Save originals
    textNodes.forEach(function(n) {
      if (!originalTexts.has(n)) originalTexts.set(n, n.textContent);
    });

    // Batch texts (LibreTranslate accepts array)
    var texts = textNodes.map(function(n) { return originalTexts.get(n) || n.textContent; });
    if (!texts.length) return;

    if (spinner) spinner.style.display = 'inline-block';

    // Split into chunks of 50 to avoid request size limits
    var chunkSize = 50;
    var promises = [];
    for (var i = 0; i < texts.length; i += chunkSize) {
      (function(chunk, startIdx) {
        var p = fetch(LIBRE_API + '/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            q: chunk,
            source: 'en',
            target: targetLang,
            format: 'text'
          })
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
          var translated = data.translatedText;
          if (Array.isArray(translated)) {
            translated.forEach(function(t, j) {
              var node = textNodes[startIdx + j];
              if (node && node.parentNode) node.textContent = t;
            });
          }
        });
        promises.push(p);
      })(texts.slice(i, i + chunkSize), i);
    }

    Promise.all(promises).then(function() {
      currentLang = targetLang;
      updateActiveFlag();
      if (spinner) spinner.style.display = 'none';
    }).catch(function(err) {
      console.error('Translation failed:', err);
      if (spinner) spinner.style.display = 'none';
      alert('Translation failed. The LibreTranslate server may be unavailable.');
    });
  }

  function updateActiveFlag() {
    var widget = document.getElementById('translate-widget');
    if (!widget) return;
    widget.querySelectorAll('a').forEach(function(a) {
      a.classList.toggle('active', a.dataset.lang === currentLang);
    });
  }

  function injectWidget() {
    if (document.getElementById('translate-widget')) return;

    var widget = document.createElement('div');
    widget.id = 'translate-widget';
    var enLink = document.createElement('a');
    enLink.innerHTML = ukFlag;
    enLink.title = 'English';
    enLink.dataset.lang = 'en';
    enLink.className = '';
    enLink.onclick = function(e) { e.preventDefault(); translatePage('en'); };

    var frLink = document.createElement('a');
    frLink.innerHTML = qcFlag;
    frLink.title = 'Français';
    frLink.dataset.lang = 'fr';
    frLink.onclick = function(e) { e.preventDefault(); translatePage('fr'); };

    var spinner = document.createElement('div');
    spinner.id = 'translate-spinner';

    widget.appendChild(enLink);
    widget.appendChild(frLink);
    widget.appendChild(spinner);

    var sidebar = document.querySelector('.myst-toc');
    if (sidebar) {
      sidebar.insertBefore(widget, sidebar.firstChild);
    } else {
      widget.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:10000;display:flex;gap:5px;background:rgba(255,255,255,0.95);border-radius:8px;padding:6px 10px;box-shadow:0 2px 8px rgba(0,0,0,0.2);';
      document.body.appendChild(widget);
    }
  }

  function injectAndTranslate() {
    injectWidget();
    // Auto-translate to French on load
    if (currentLang === 'fr') {
      currentLang = 'en'; // Reset so translatePage('fr') actually runs
      translatePage('fr');
    }
  }

  // MutationObserver to re-inject after React navigation
  var observer = new MutationObserver(function() {
    if (!document.getElementById('translate-widget')) {
      injectAndTranslate();
    }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(injectAndTranslate, 500);
      observer.observe(document.body, { childList: true, subtree: true });
    });
  } else {
    setTimeout(injectAndTranslate, 500);
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
</script>
<!-- End LibreTranslate Widget -->
"""

BUILD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "_build", "html")


def inject():
    html_files = glob.glob(os.path.join(BUILD_DIR, "**", "*.html"), recursive=True)
    count = 0
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "translate-widget" in content:
            continue
        if "</body>" in content:
            content = content.replace("</body>", SNIPPET + "\n</body>")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
    print(f"Injected LibreTranslate widget into {count} HTML file(s)")


if __name__ == "__main__":
    inject()
