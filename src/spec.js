// Measurement overlay, spec tables and theme switch for the flow pages.
(function () {
  function devScale(dev) {
    var w = parseFloat(getComputedStyle(dev).getPropertyValue('--w')) || 360;
    return dev.getBoundingClientRect().width / w;
  }
  function dp(n) { return Math.round(n * 2) / 2; }

  function measure(dev) {
    var s = devScale(dev), d = dev.getBoundingClientRect(), out = [];
    dev.querySelectorAll('[data-el]').forEach(function (el) {
      var r = el.getBoundingClientRect();
      out.push({ el: el, name: el.dataset.el, x: (r.left - d.left) / s, y: (r.top - d.top) / s,
        w: dp(r.width / s), h: dp(r.height / s), c: el.dataset.c || '', t: el.dataset.t || '', i: el.dataset.i || '' });
    });
    return out;
  }

  function fillTables() {
    document.querySelectorAll('.spec-screen').forEach(function (fig) {
      var dev = fig.querySelector('.s-dev'), tb = fig.querySelector('.spec-table tbody');
      if (!dev || !tb) return;
      var rows = measure(dev).filter(function (m) { return m.name !== 'Screen'; });
      tb.innerHTML = rows.map(function (m) {
        return '<tr><td>' + m.name + '</td><td class="n">' + m.w + ' × ' + m.h + '</td><td>' + m.c + '</td><td>' + m.t + '</td><td>' +
          (m.i ? '<code>' + m.i + '</code>' : '') + '</td></tr>';
      }).join('');
    });
  }

  function overlay(on) {
    document.querySelectorAll('.s-dev').forEach(function (dev) {
      dev.querySelectorAll('.s-m').forEach(function (n) { n.remove(); });
      if (!on) return;
      measure(dev).forEach(function (m) {
        if (m.name === 'Screen') return;
        var b = document.createElement('div');
        b.className = 's-m';
        b.title = m.name + ' · ' + m.w + ' × ' + m.h + ' dp';
        b.style.cssText = 'left:' + m.x + 'px;top:' + m.y + 'px;width:' + m.w + 'px;height:' + m.h + 'px';
        b.innerHTML = '<span>' + m.w + '×' + m.h + '</span>';
        dev.appendChild(b);
      });
    });
  }

  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  function setTheme(t) {
    if (t) document.documentElement.dataset.theme = t; else delete document.documentElement.dataset.theme;
    document.querySelectorAll('[data-theme-btn]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.themeBtn === (t || 'auto'))); });
    store('stx-theme', t || '');
  }

  document.addEventListener('DOMContentLoaded', function () {
    setTheme(load('stx-theme') || '');
    document.querySelectorAll('[data-theme-btn]').forEach(function (b) {
      b.addEventListener('click', function () { setTheme(b.dataset.themeBtn === 'auto' ? '' : b.dataset.themeBtn); });
    });
    var mt = document.getElementById('measure-toggle'), on = false;
    if (mt) mt.addEventListener('click', function () {
      on = !on; mt.setAttribute('aria-pressed', String(on)); overlay(on);
    });
    fillTables();
    if (mt && /[?&]measure=1/.test(location.search)) mt.click();
    var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(function () { if (on) overlay(true); }, 150); });
  });
})();
