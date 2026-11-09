// qr.js: Integración del generador QR de Desktopia Lab
// Genera e inserta el SVG vectorial oficial verificado desde el backend
var QR = (function () {
  return {
    renderSVG: function (url, size) {
      size = size || 208;
      var cleanUrl = encodeURIComponent(url || window.location.origin);
      return '<img src="/api/qr.svg?url=' + cleanUrl + '&size=' + size + '&t=' + Date.now() + '" width="' + size + '" height="' + size + '" alt="QR ' + url + '" class="block mx-auto rounded-lg select-none" />';
    }
  };
})();
