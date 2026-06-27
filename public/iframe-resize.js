window.addEventListener('message', function (e) {
  if (!e.data || e.data.type !== 'gwf-height') return;
  document.querySelectorAll('iframe').forEach(function (f) {
    try {
      if (f.contentWindow === e.source) {
        f.style.height = e.data.height + 'px';
      }
    } catch (err) {}
  });
});