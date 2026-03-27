#!/usr/bin/env python3
"""Inject GTranslate EN/FR widget into all built HTML files.

Places the widget in a fixed bar just below the navbar, outside the React root,
so React hydration cannot remove it.
"""

import glob
import os

# Complete snippet injected right after </head><body...> opening tag area
# We inject right before </body> but the widget is position:fixed so it
# sits visually in the navbar area
SNIPPET = """
<!-- GTranslate EN/FR Widget (outside React root) -->
<div id="gtranslate-widget" style="position:fixed; bottom:20px; right:20px; z-index:99999; display:flex; gap:5px; background:rgba(255,255,255,0.95); border-radius:8px; padding:6px 10px; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
  <a href="#" onclick="doGTranslate('en|en');return false;" title="English" class="gflag" style="background-position:-0px -0px;"><img src="//gtranslate.net/flags/blank.png" height="24" width="24" alt="English" /></a>
  <a href="#" onclick="doGTranslate('en|fr');return false;" title="French" class="gflag" style="background-position:-200px -100px; margin-left:4px;"><img src="//gtranslate.net/flags/blank.png" height="24" width="24" alt="French" /></a>
</div>
<div id="google_translate_element2" style="display:none!important;"></div>
<style>
  a.gflag { vertical-align: middle; font-size: 24px; padding: 1px 0; background-repeat: no-repeat; background-image: url(//gtranslate.net/flags/24.png); cursor: pointer; display: inline-block; }
  a.gflag img { border: 0; }
  a.gflag:hover { background-image: url(//gtranslate.net/flags/24a.png); }
  #goog-gt-tt { display: none !important; }
  .goog-te-banner-frame { display: none !important; }
  .goog-te-menu-value:hover { text-decoration: none !important; }
  .skiptranslate { display: none !important; }
  body { top: 0 !important; }
</style>
<script>
  function googleTranslateElementInit2() {
    new google.translate.TranslateElement({pageLanguage: 'en', autoDisplay: false}, 'google_translate_element2');
  }
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit2"></script>
<script>
  function GTranslateFireEvent(a,b){try{if(document.createEvent){var c=document.createEvent("HTMLEvents");c.initEvent(b,true,true);a.dispatchEvent(c)}else{var c=document.createEventObject();a.fireEvent("on"+b,c)}}catch(e){}}
  function doGTranslate(a){if(a.value)a=a.value;if(a=="")return;var b=a.split("|")[1];var c;var d=document.getElementsByTagName("select");for(var i=0;i<d.length;i++)if(d[i].className=="goog-te-combo")c=d[i];if(document.getElementById("google_translate_element2")==null||document.getElementById("google_translate_element2").innerHTML.length==0||c.length==0||c.innerHTML.length==0){setTimeout(function(){doGTranslate(a)},500)}else{c.value=b;GTranslateFireEvent(c,"change");GTranslateFireEvent(c,"change")}}
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
            # Inject right before </body>, outside the React-managed DOM tree
            content = content.replace("</body>", SNIPPET + "\n</body>")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
    print(f"Injected GTranslate widget into {count} HTML file(s)")


if __name__ == "__main__":
    inject()
