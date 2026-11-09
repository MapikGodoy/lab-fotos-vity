// crop.js v3: Soporte táctil completo para móviles (Pointer Events), líneas guía dinámicas,
// cruz de precisión con coordenadas y regla de tercios.

var crop = {
  base: null,
  cardId: null,
  selX: 0, selY: 0, selW: 0, selH: 0,
  startX: 0, startY: 0,
  imgW: 0, imgH: 0,
  naturalW: 0, naturalH: 0,
  mode: null, // 'select' | 'drag' | 'resize'
  handle: null,
  activePointerId: null
};

function _rect() {
  var c = document.getElementById('crop-container');
  return c ? c.getBoundingClientRect() : { left: 0, top: 0, width: 0, height: 0 };
}

function _clamp(v, lo, hi) {
  return Math.max(lo, Math.min(v, hi));
}

function _actualizarGuias(mx, my, visible) {
  var gh = document.getElementById('crop-guide-h');
  var gv = document.getElementById('crop-guide-v');
  var cc = document.getElementById('crop-crosshair-center');
  var badge = document.getElementById('crop-coord-badge');

  if (!visible || mx < 0 || my < 0 || mx > crop.imgW || my > crop.imgH) {
    if (gh) gh.classList.add('hidden');
    if (gv) gv.classList.add('hidden');
    if (cc) cc.classList.add('hidden');
    if (badge && !crop.mode) badge.classList.add('hidden');
    return;
  }

  if (gh) {
    gh.classList.remove('hidden');
    gh.style.top = my + 'px';
  }
  if (gv) {
    gv.classList.remove('hidden');
    gv.style.left = mx + 'px';
  }
  if (cc) {
    cc.classList.remove('hidden');
    cc.style.left = mx + 'px';
    cc.style.top = my + 'px';
  }

  if (badge) {
    badge.classList.remove('hidden');
    var realW = crop.naturalW && crop.imgW > 0 ? Math.round((crop.selW / crop.imgW) * crop.naturalW) : Math.round(crop.selW);
    var realH = crop.naturalH && crop.imgH > 0 ? Math.round((crop.selH / crop.imgH) * crop.naturalH) : Math.round(crop.selH);
    if (crop.mode && crop.selW > 10 && crop.selH > 10) {
      badge.innerText = realW + ' × ' + realH + ' px';
      badge.style.left = _clamp(crop.selX + crop.selW / 2, 40, crop.imgW - 40) + 'px';
      badge.style.top = Math.max(10, crop.selY - 26) + 'px';
    } else {
      var pxX = crop.naturalW && crop.imgW > 0 ? Math.round((mx / crop.imgW) * crop.naturalW) : Math.round(mx);
      var pxY = crop.naturalH && crop.imgH > 0 ? Math.round((my / crop.imgH) * crop.naturalH) : Math.round(my);
      badge.innerText = 'X: ' + pxX + ' | Y: ' + pxY;
      badge.style.left = _clamp(mx, 45, crop.imgW - 45) + 'px';
      badge.style.top = Math.max(10, my - 26) + 'px';
    }
  }
}

function _renderSel() {
  var s = document.getElementById('crop-selection');
  if (!s) return;
  if (crop.selW > 6 && crop.selH > 6) {
    s.style.display = 'block';
    s.style.left = crop.selX + 'px';
    s.style.top = crop.selY + 'px';
    s.style.width = crop.selW + 'px';
    s.style.height = crop.selH + 'px';
  } else if (!crop.mode) {
    s.style.display = 'none';
  }
}

function _onPointerMove(e) {
  var r = _rect();
  if (r.width <= 0 || r.height <= 0) return;
  var mx = _clamp(e.clientX - r.left, 0, crop.imgW);
  var my = _clamp(e.clientY - r.top, 0, crop.imgH);

  _actualizarGuias(mx, my, true);

  if (!crop.mode) return;

  if (crop.mode === 'select') {
    crop.selX = Math.min(crop.startX, mx);
    crop.selY = Math.min(crop.startY, my);
    crop.selW = Math.abs(mx - crop.startX);
    crop.selH = Math.abs(my - crop.startY);
    _renderSel();
  } else if (crop.mode === 'drag') {
    var dx = mx - crop.startX;
    var dy = my - crop.startY;
    crop.selX = _clamp(crop.selX + dx, 0, crop.imgW - crop.selW);
    crop.selY = _clamp(crop.selY + dy, 0, crop.imgH - crop.selH);
    crop.startX = mx;
    crop.startY = my;
    _renderSel();
  } else if (crop.mode === 'resize') {
    var h = crop.handle || '';
    var x2 = crop.selX + crop.selW;
    var y2 = crop.selY + crop.selH;

    if (h.indexOf('l') !== -1) crop.selX = _clamp(mx, 0, x2 - 25);
    if (h.indexOf('r') !== -1) x2 = _clamp(mx, crop.selX + 25, crop.imgW);
    if (h.indexOf('t') !== -1) crop.selY = _clamp(my, 0, y2 - 25);
    if (h.indexOf('b') !== -1) y2 = _clamp(my, crop.selY + 25, crop.imgH);

    crop.selW = x2 - crop.selX;
    crop.selH = y2 - crop.selY;
    _renderSel();
  }
}

function _onPointerUp(e) {
  var container = document.getElementById('crop-container');
  if (crop.activePointerId !== null && container) {
    try { container.releasePointerCapture(crop.activePointerId); } catch(err) {}
  }
  crop.activePointerId = null;
  crop.mode = null;
  crop.handle = null;

  // Si el recorte dibujado es demasiado diminuto (un simple tap), lo quitamos
  if (crop.selW < 20 || crop.selH < 20) {
    crop.selW = 0; crop.selH = 0;
    _renderSel();
  }
}

function abrirModalRecorte(base, cardId) {
  crop.base = base;
  crop.cardId = cardId;
  crop.selX = crop.selY = crop.selW = crop.selH = 0;
  crop.mode = null;
  crop.handle = null;
  crop.activePointerId = null;

  var modal = document.getElementById('crop-modal');
  var img = document.getElementById('crop-image');
  var sel = document.getElementById('crop-selection');
  var container = document.getElementById('crop-container');

  if (sel) sel.style.display = 'none';
  if (modal) modal.classList.add('active');

  function initDimensions() {
    if (!img) return;
    crop.imgW = img.clientWidth || img.offsetWidth;
    crop.imgH = img.clientHeight || img.offsetHeight;
    crop.naturalW = img.naturalWidth || crop.imgW;
    crop.naturalH = img.naturalHeight || crop.imgH;
    
    // Sugerencia inicial: encuadre central con 85% de margen
    if (crop.imgW > 60 && crop.imgH > 60) {
      crop.selW = Math.round(crop.imgW * 0.85);
      crop.selH = Math.round(crop.imgH * 0.85);
      crop.selX = Math.round((crop.imgW - crop.selW) / 2);
      crop.selY = Math.round((crop.imgH - crop.selH) / 2);
      _renderSel();
    }
  }

  img.onload = initDimensions;
  img.src = '/api/ver-foto/' + base + '_original.png?t=' + Date.now();
  if (img.complete && img.naturalWidth) {
    initDimensions();
  }

  // Desvincular eventos anteriores para evitar acumulaciones
  container.onpointerdown = null;
  container.onpointermove = null;
  container.onpointerup = null;
  container.onpointercancel = null;
  container.onpointerleave = null;

  container.onpointerdown = function(e) {
    e.preventDefault();
    e.stopPropagation();
    var r = _rect();
    var mx = _clamp(e.clientX - r.left, 0, crop.imgW);
    var my = _clamp(e.clientY - r.top, 0, crop.imgH);
    crop.activePointerId = e.pointerId;

    try { container.setPointerCapture(e.pointerId); } catch(err) {}

    var targetHandle = e.target.getAttribute('data-handle');
    if (targetHandle) {
      crop.mode = 'resize';
      crop.handle = targetHandle;
      crop.startX = mx;
      crop.startY = my;
    } else if (e.target.id === 'crop-selection' || e.target.closest('#crop-selection')) {
      crop.mode = 'drag';
      crop.startX = mx;
      crop.startY = my;
    } else {
      crop.mode = 'select';
      crop.startX = mx;
      crop.startY = my;
      crop.selX = mx;
      crop.selY = my;
      crop.selW = 0;
      crop.selH = 0;
      _renderSel();
    }
    _actualizarGuias(mx, my, true);
  };

  container.onpointermove = _onPointerMove;
  container.onpointerup = _onPointerUp;
  container.onpointercancel = _onPointerUp;
  container.onpointerleave = function(e) {
    if (!crop.mode) _actualizarGuias(0, 0, false);
  };
}

function cerrarModalRecorte() {
  var modal = document.getElementById('crop-modal');
  if (modal) modal.classList.remove('active');
  crop.base = null;
  crop.cardId = null;
  crop.mode = null;
  _actualizarGuias(0, 0, false);
}

function _coordenadasPct() {
  if (crop.imgW <= 0 || crop.imgH <= 0 || crop.selW <= 0 || crop.selH <= 0) return null;
  return {
    x1: (crop.selX / crop.imgW) * 100,
    y1: (crop.selY / crop.imgH) * 100,
    x2: ((crop.selX + crop.selW) / crop.imgW) * 100,
    y2: ((crop.selY + crop.selH) / crop.imgH) * 100
  };
}

async function aplicarRecorte() {
  if (!crop.base || crop.bloqueado) return;
  if (crop.selW < 20 || crop.selH < 20) {
    mostrarToast('Seleccioná un área para recortar', 'error');
    return;
  }
  var c = _coordenadasPct();
  if (!c) return;

  var base = crop.base;
  var cardId = crop.cardId;
  crop.bloqueado = true;
  var btnRecorte = document.getElementById('btn-aplicar-recorte');
  if (btnRecorte) {
    btnRecorte.disabled = true;
    btnRecorte.classList.add('opacity-50', 'pointer-events-none');
  }

  try {
    mostrarToast('Recortando imagen...', 'info');
    var url = '/api/recortar/' + base + '?x1=' + c.x1.toFixed(2) + '&y1=' + c.y1.toFixed(2) + '&x2=' + c.x2.toFixed(2) + '&y2=' + c.y2.toFixed(2);
    var res = await fetch(url, { method: 'POST' });
    var data = await res.json();
    if (res.ok) {
      mostrarToast('Recortado correctamente', 'success');
      cerrarModalRecorte();
      if (typeof refrescarImagenesTarjeta === 'function') {
        refrescarImagenesTarjeta(base, cardId);
      }
      var bd = document.getElementById('btn-deshacer-' + cardId);
      if (bd) bd.style.display = 'inline-block';
    } else {
      mostrarToast(data.detail || 'Error al recortar', 'error');
    }
  } catch (e) {
    mostrarToast('Error de conexión con el servidor', 'error');
  } finally {
    crop.bloqueado = false;
    if (btnRecorte) {
      btnRecorte.disabled = false;
      btnRecorte.classList.remove('opacity-50', 'pointer-events-none');
    }
  }
}

async function extraerFotoNueva() {
  if (!crop.base || crop.bloqueado) return;
  if (crop.selW < 20 || crop.selH < 20) {
    mostrarToast('Seleccioná un área para la nueva foto', 'error');
    return;
  }
  var c = _coordenadasPct();
  if (!c) return;

  var base = crop.base;
  crop.bloqueado = true;
  var btnExtraer = document.getElementById('btn-extraer');
  if (btnExtraer) {
    btnExtraer.disabled = true;
    btnExtraer.classList.add('opacity-50', 'pointer-events-none');
  }

  try {
    mostrarToast('Extrayendo nueva foto...', 'info');
    var url = '/api/extraer-foto/' + base + '?x1=' + c.x1.toFixed(2) + '&y1=' + c.y1.toFixed(2) + '&x2=' + c.x2.toFixed(2) + '&y2=' + c.y2.toFixed(2);
    var res = await fetch(url, { method: 'POST' });
    var data = await res.json();
    if (res.ok) {
      var nb = data.nueva_base;
      mostrarToast('Foto extraída: ' + (data.dimensiones || ''), 'success');
      cerrarModalRecorte();
      agregarTarjetaAlaWeb(nb);
      var cardId = 'foto-card-' + nb;
      var st = document.getElementById('status-' + cardId);
      if (st) st.innerText = 'Restaurando con IA (GPU + CPU)...';
      try {
        var iaRes = await fetch('/api/procesar-ia/' + nb, { method: 'POST' });
        var iaData = await iaRes.json();
        actualizarTarjetaConIA(nb, iaData.caras, iaData.ia, iaData.completa, iaData.rostros_detectados, iaData.auto_rotada);
      } catch (e) {
        actualizarTarjetaConIA(nb, null, null, null, 0, false);
      }
    } else {
      mostrarToast(data.detail || 'Error al extraer', 'error');
    }
  } catch (e) {
    mostrarToast('Error de conexión', 'error');
  } finally {
    crop.bloqueado = false;
    if (btnExtraer) {
      btnExtraer.disabled = false;
      btnExtraer.classList.remove('opacity-50', 'pointer-events-none');
    }
  }
}
