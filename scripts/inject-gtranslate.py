#!/usr/bin/env python3
"""Inject GTranslate EN/FR widget into the navbar of all built HTML files."""

import glob
import os

# Widget HTML to insert into the navbar, right after the GitHub button
WIDGET_HTML = '''<div id="gtranslate-widget" class="hidden sm:flex items-center gap-1 ml-2"><a href="#" onclick="doGTranslate('en|en');return false;" title="English" class="gflag" style="background-position:-0px -0px;"><img src="//gtranslate.net/flags/blank.png" height="24" width="24" alt="English" /></a><a href="#" onclick="doGTranslate('en|fr');return false;" title="French" class="gflag" style="background-position:-200px -100px;"><img src="//gtranslate.net/flags/blank.png" height="24" width="24" alt="French" /></a></div>'''

# Styles and scripts injected before </head>
HEAD_SNIPPET = """
<!-- GTranslate Styles -->
<style>
  a.gflag { vertical-align: middle; font-size: 24px; padding: 1px 0; background-repeat: no-repeat; background-image: url(//gtranslate.net/flags/24.png); cursor: pointer; display: inline-block; }
  a.gflag img { border: 0; }
  a.gflag:hover { background-image: url(//gtranslate.net/flags/24a.png); }
  #goog-gt-tt { display: none !important; }
  .goog-te-banner-frame { display: none !important; }
  .goog-te-menu-value:hover { text-decoration: none !important; }
  .skiptranslate { display: none !important; }
  body { top: 0 !important; }
  #google_translate_element2 { display: none !important; }
</style>
"""

# Scripts injected before </body>
BODY_SNIPPET = """
<!-- GTranslate Scripts -->
<div id="google_translate_element2"></div>
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

        # Find the GitHub button's parent div and insert widget after it
        # The pattern: <div class="hidden sm:block"><a href="...">GitHub</a></div>
        github_marker = '>GitHub</a></div></div></nav></div>'
        if github_marker in content:
            content = content.replace(
                github_marker,
                '>GitHub</a></div>' + WIDGET_HTML + '</div></nav></div>'
            )
            # Inject styles into <head>
            content = content.replace('</head>', HEAD_SNIPPET + '</head>')
            # Inject scripts before </body>
            content = content.replace('</body>', BODY_SNIPPET + '</body>')

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
    print(f"Injected GTranslate widget into {count} HTML file(s)")


if __name__ == "__main__":
    inject()
