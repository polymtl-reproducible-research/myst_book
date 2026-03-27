#!/usr/bin/env python3
"""Inject GTranslate EN/FR widget into all built HTML files."""

import glob
import os

SNIPPET = """
<!-- GTranslate EN/FR Widget - injected after React hydration -->
<style>
  #gtranslate-widget {
    display: flex;
    gap: 8px;
    padding: 8px 12px;
    margin: 0 12px 8px 12px;
  }
  a.gflag { vertical-align: middle; font-size: 24px; padding: 1px 0; background-repeat: no-repeat; background-image: url(//gtranslate.net/flags/24.png); cursor: pointer; }
  a.gflag img { border: 0; }
  a.gflag:hover { background-image: url(//gtranslate.net/flags/24a.png); }
  #goog-gt-tt { display: none !important; }
  .goog-te-banner-frame { display: none !important; }
  .goog-te-menu-value:hover { text-decoration: none !important; }
  .skiptranslate { display: none !important; }
  body { top: 0 !important; }
  #google_translate_element2 { display: none !important; }
</style>
<script>
(function() {
  // Wait for React hydration to finish, then inject the widget
  function injectGTranslate() {
    if (document.getElementById('gtranslate-widget')) return;

    // Create the widget container
    var widget = document.createElement('div');
    widget.id = 'gtranslate-widget';
    var flagStyle = "cursor:pointer;display:inline-block;line-height:0;";
    var ukFlag = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 60 40" style="border-radius:2px;"><rect width="60" height="40" fill="#012169"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="8"/><path d="M0,0 L60,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,60 0,60 40,30 20,0 40)"/><path d="M60,0 L0,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,0 40,60 40,30 20,60 0)"/><path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="12"/><path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/></svg>';
    var qcFlag = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 24 16" style="border-radius:2px;"><rect width="24" height="16" fill="#003DA5"/><rect x="10" y="0" width="4" height="16" fill="#fff"/><rect x="0" y="6" width="24" height="4" fill="#fff"/><text x="5" y="5.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text><text x="15" y="5.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text><text x="5" y="13.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text><text x="15" y="13.5" font-size="5" fill="#fff" font-family="serif">&#9884;</text></svg>';
    widget.innerHTML = '<a href="#" onclick="doGTranslate(\\'en|en\\');return false;" title="English" style="' + flagStyle + '">' + ukFlag + '</a>' +
      '<a href="#" onclick="doGTranslate(\\'en|fr\\');return false;" title="Français" style="' + flagStyle + '">' + qcFlag + '</a>';
    // Insert at the top of the left sidebar TOC
    var sidebar = document.querySelector('.myst-toc');
    if (sidebar) {
      sidebar.insertBefore(widget, sidebar.firstChild);
    } else {
      // Fallback: append to body as fixed element
      widget.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:10000;display:flex;gap:5px;background:rgba(255,255,255,0.9);border-radius:6px;padding:4px 8px;box-shadow:0 1px 4px rgba(0,0,0,0.15);';
      document.body.appendChild(widget);
    }

    // Create hidden translate element (only once)
    if (!document.getElementById('google_translate_element2')) {
      var te = document.createElement('div');
      te.id = 'google_translate_element2';
      document.body.appendChild(te);

      // Load Google Translate
      window.googleTranslateElementInit2 = function() {
        new google.translate.TranslateElement({pageLanguage: 'en', autoDisplay: false}, 'google_translate_element2');
      };
      var s = document.createElement('script');
      s.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit2';
      document.body.appendChild(s);
    }
  }

  // GTranslate helper functions
  window.GTranslateFireEvent = function(a,b){try{if(document.createEvent){var c=document.createEvent("HTMLEvents");c.initEvent(b,true,true);a.dispatchEvent(c)}else{var c=document.createEventObject();a.fireEvent("on"+b,c)}}catch(e){}};
  window.doGTranslate = function(a){if(a.value)a=a.value;if(a=="")return;var b=a.split("|")[1];var c;var d=document.getElementsByTagName("select");for(var i=0;i<d.length;i++)if(d[i].className=="goog-te-combo")c=d[i];if(document.getElementById("google_translate_element2")==null||document.getElementById("google_translate_element2").innerHTML.length==0||c.length==0||c.innerHTML.length==0){setTimeout(function(){doGTranslate(a)},500)}else{c.value=b;GTranslateFireEvent(c,"change");GTranslateFireEvent(c,"change")}};

  // Use MutationObserver to re-inject if React removes the widget
  var observer = new MutationObserver(function() {
    if (!document.getElementById('gtranslate-widget')) {
      injectGTranslate();
    }
  });

  // Start observing once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(injectGTranslate, 500);
      observer.observe(document.body, { childList: true, subtree: true });
    });
  } else {
    setTimeout(injectGTranslate, 500);
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
</script>
<!-- End GTranslate Widget -->
"""

BUILD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "_build", "html")


def inject():
    html_files = glob.glob(os.path.join(BUILD_DIR, "**", "*.html"), recursive=True)
    count = 0
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "gtranslate-widget" in content:
            continue
        if "</body>" in content:
            content = content.replace("</body>", SNIPPET + "\n</body>")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
    print(f"Injected GTranslate widget into {count} HTML file(s)")


if __name__ == "__main__":
    inject()
