// scan.js: overlay de progreso de escaneo con estética SaaS corporativa.
(function () {
  var st = document.createElement('style');
  st.textContent = [
    '#scan-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:1200;justify-content:center;align-items:center;backdrop-filter:blur(8px)}',
    '#scan-overlay.active{display:flex}',
    '.scan-card{background:rgba(20,20,23,0.95);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:32px;width:min(540px,92vw);text-align:center;box-shadow:0 25px 50px -12px rgba(0,0,0,0.7);backdrop-filter:blur(20px)}',
    '.scan-bed{position:relative;height:140px;margin:20px 0;border-radius:12px;background:#0c0c0e;border:1px solid #27272a;overflow:hidden}',
    '.scan-bed::before{content:"";position:absolute;inset:8px;background:repeating-linear-gradient(0deg,rgba(255,255,255,.02) 0 2px,transparent 2px 8px);border-radius:6px}',
    '.scan-line{position:absolute;left:4%;right:4%;height:2px;background:linear-gradient(90deg,transparent,#10b981,#6ee7b7,#10b981,transparent);box-shadow:0 0 16px 2px rgba(16,185,129,.4);border-radius:2px;animation:scanmove 2.4s cubic-bezier(.45,0,.55,1) infinite}',
    '@keyframes scanmove{0%{top:6%}50%{top:92%}100%{top:6%}}',
    '.scan-pct{font-size:36px;font-weight:700;color:#f4f4f5;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-variant-numeric:tabular-nums}',
    '.scan-bar{height:6px;background:#27272a;border-radius:999px;overflow:hidden;margin:16px 0 8px}',
    '.scan-bar-fill{height:100%;width:0%;background:linear-gradient(90deg,#10b981,#34d399);border-radius:999px;transition:width .35s ease}',
    '.scan-steps{display:flex;justify-content:space-between;gap:8px;margin-top:24px;border-top:1px solid #27272a;padding-top:18px}',
    '.scan-step{flex:1;font-size:11px;color:#71717a;display:flex;flex-direction:column;align-items:center;gap:6px;line-height:1.2;font-family:sans-serif}',
    '.scan-step .dot{width:22px;height:22px;border-radius:50%;border:1px solid #3f3f46;display:flex;align-items:center;justify-content:center;font-size:10px;font-family:monospace;background:#18181b;color:#a1a1aa}',
    '.scan-step.active{color:#10b981}.scan-step.active .dot{border-color:#10b981;color:#10b981;box-shadow:0 0 10px rgba(16,185,129,.35)}',
    '.scan-step.done{color:#a1a1aa}.scan-step.done .dot{border-color:#10b981;background:#064e3b;color:#34d399}',
    '.scan-error{display:none;margin-top:14px;padding:12px;border-radius:10px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);color:#fca5a5;font-size:12px;text-align:left}',
    '.scan-error.active{display:block}',
    '#scan-overlay.error .scan-line{background:linear-gradient(90deg,transparent,#ef4444,transparent);box-shadow:0 0 16px 2px rgba(239,68,68,.5);animation-play-state:paused}',
    '#scan-overlay.error .scan-pct{color:#fca5a5}',
    '.scan-ok{display:none;font-size:13px;color:#34d399;margin-top:10px;font-weight:600}',
    '.scan-ok.active{display:block}',
    '.scan-btn{margin-top:16px;background:#27272a;color:#e4e4e7;border:1px solid #3f3f46;padding:8px 22px;border-radius:10px;font-size:12px;font-weight:500;cursor:pointer;display:none;transition:all 0.2s}',
    '.scan-btn:hover{background:#3f3f46}',
    '.scan-btn.active{display:inline-block}'
  ].join('\n');
  document.head.appendChild(st);
})();

var scanUI = { mostrado: 0, objetivo: 0, raf: null, inicioFase40: null, interval: null };

function _scanOverlayDOM() {
  var ov = document.getElementById('scan-overlay');
  if (ov) return ov;
  var d = document.createElement('div');
  d.id = 'scan-overlay';
  d.innerHTML =
    '<div class="scan-card">' +
    '<div style="font-size:13px;font-weight:600;color:#e4e4e7;letter-spacing:-0.01em" id="scan-title">Digitalizando platina...</div>' +
    '<div class="scan-bed"><div class="scan-line"></div></div>' +
    '<div class="scan-pct"><span id="scan-pct">0</span>%</div>' +
    '<div class="scan-bar"><div class="scan-bar-fill" id="scan-bar-fill"></div></div>' +
    '<div style="font-size:12px;color:#a1a1aa;margin-top:4px" id="scan-msg">Iniciando hardware...</div>' +
    '<div class="scan-steps">' +
    '<div class="scan-step" id="step-1"><div class="dot">1</div>Conexión</div>' +
    '<div class="scan-step" id="step-2"><div class="dot">2</div>Escaneo</div>' +
    '<div class="scan-step" id="step-3"><div class="dot">3</div>Segmentación</div>' +
    '<div class="scan-step" id="step-4"><div class="dot">4</div>Finalizado</div>' +
    '</div>' +
    '<div class="scan-error" id="scan-error"></div>' +
    '<div class="scan-ok" id="scan-ok">Digitalización completada. Extrayendo imágenes...</div>' +
    '<button class="scan-btn" id="scan-btn" onclick="cerrarOverlayEscaneo()">Cerrar</button>' +
    '</div>';
  document.body.appendChild(d);
  return d;
}

function _scanTick() {
  var diff = scanUI.objetivo - scanUI.mostrado;
  if (Math.abs(diff) < 0.1) scanUI.mostrado = scanUI.objetivo;
  else scanUI.mostrado += diff * 0.08;
  var p = document.getElementById('scan-pct');
  var fill = document.getElementById('scan-bar-fill');
  if (p) p.innerText = Math.round(scanUI.mostrado);
  if (fill) fill.style.width = Math.round(scanUI.mostrado) + '%';
  scanUI.raf = requestAnimationFrame(_scanTick);
}

function _marcarPasos(p) {
  var t = [10, 40, 75, 100];
  for (var i = 0; i < 4; i++) {
    var el = document.getElementById('step-' + (i + 1));
    if (!el) continue;
    el.classList.remove('active', 'done');
    var dot = el.querySelector('.dot');
    if (p >= t[i]) {
      if (i === 3 || p >= t[i + 1]) { el.classList.add('done'); if (dot) dot.innerText = '✓'; }
      else { el.classList.add('active'); if (dot) dot.innerText = String(i + 1); }
    } else if (dot) { dot.innerText = String(i + 1); }
  }
}

function _scanFallo(mensaje) {
  var ov = document.getElementById('scan-overlay');
  if (ov) ov.classList.add('error');
  var err = document.getElementById('scan-error');
  if (err) { err.innerText = mensaje; err.classList.add('active'); }
  var msg = document.getElementById('scan-msg');
  if (msg) msg.innerText = 'El proceso se detuvo debido a un error.';
  var btn = document.getElementById('scan-btn');
  if (btn) btn.classList.add('active');
  if (scanUI.raf) { cancelAnimationFrame(scanUI.raf); scanUI.raf = null; }
  mostrarToast(mensaje, 'error');
}

function cerrarOverlayEscaneo() {
  var ov = document.getElementById('scan-overlay');
  if (ov) ov.classList.remove('active');
  if (scanUI.interval) { clearInterval(scanUI.interval); scanUI.interval = null; }
  if (scanUI.raf) { cancelAnimationFrame(scanUI.raf); scanUI.raf = null; }
}

async function procesarEscaneo(esTest) {
  var dpi = document.getElementById('selector-dpi').value;
  var ov = _scanOverlayDOM();
  ov.classList.remove('error');
  ov.classList.add('active');
  document.getElementById('scan-error').classList.remove('active');
  document.getElementById('scan-btn').classList.remove('active');
  document.getElementById('scan-ok').classList.remove('active');
  document.getElementById('scan-title').innerText = esTest ? 'Digitalización en modo simulación' : 'Digitalización con Xerox Phaser';
  document.getElementById('scan-msg').innerText = 'Iniciando escáner...';
  scanUI.mostrado = 0; scanUI.objetivo = 0; scanUI.inicioFase40 = null;
  if (scanUI.raf) cancelAnimationFrame(scanUI.raf);
  scanUI.raf = requestAnimationFrame(_scanTick);
  _marcarPasos(0);

  try {
    var url = esTest ? '/api/escanear-test?dpi=' + dpi : '/api/escanear?dpi=' + dpi;
    await fetch(url, { method: 'POST' });
  } catch (e) {
    _scanFallo('No hay conexión con el servidor.');
    return;
  }

  if (scanUI.interval) clearInterval(scanUI.interval);
  scanUI.interval = setInterval(async function () {
    try {
      var res = await fetch('/api/estado-escaner');
      var estado = await res.json();
      var pReal = estado.progreso || 0;
      var p = pReal;

      if (pReal >= 40 && pReal < 75) {
        if (!scanUI.inicioFase40) scanUI.inicioFase40 = Date.now();
        var seg = (Date.now() - scanUI.inicioFase40) / 1000;
        var simulado = 40 + Math.min(32, seg * (esTest ? 8 : 0.5));
        p = Math.max(pReal, Math.min(simulado, 72));
      } else {
        scanUI.inicioFase40 = null;
      }

      scanUI.objetivo = p;
      var msg = document.getElementById('scan-msg');
      if (msg) msg.innerText = estado.mensaje || '';
      _marcarPasos(pReal);

      if (estado.error) {
        clearInterval(scanUI.interval); scanUI.interval = null;
        _scanFallo(estado.mensaje || 'El escáner reportó un error.');
      } else if (estado.completado) {
        clearInterval(scanUI.interval); scanUI.interval = null;
        scanUI.objetivo = 100;
        _marcarPasos(100);
        document.getElementById('scan-ok').classList.add('active');
        setTimeout(function () {
          cerrarOverlayEscaneo();
          procesarLoteDeTarjetasIA(estado.fotos_listas || []);
        }, 1200);
      }
    } catch (e) { /* reintenta en el siguiente tick */ }
  }, 700);
}
