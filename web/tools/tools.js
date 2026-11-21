/* SmarType: interactive client-side logic for free web micro-tools. Runs 100% in tab memory. */
(() => {
  const EMPTY_MSG = "Paste or type comma-separated or line-separated notes above.";
  const stripListMarker = (line) =>
    String(line || "").trim().replace(/^(?:[-*•☐☑](?:\s+|$)|\d+[.)](?:\s+|$)|\[\s*[xX]?\s*\](?:\s+|$))/, "").trim();
  const capFirst = (s) => (/^[a-z]/.test(s) && !/^https?:\/\//i.test(s) ? s[0].toUpperCase() + s.slice(1) : s);

  const splitRoughItems = (raw, mode) => {
    const src = String(raw || "").trim();
    if (!src) return [];
    const sep = !/[\r\n;•,]/.test(src) && mode !== "table" ? /\s+-\s+/ : /\r?\n|;|•|,(?!\d{3}\b)/;
    return src.split(sep).map(stripListMarker).filter(Boolean);
  };

  const formatRoughNotes = (raw, mode = "bullets") => {
    const items = splitRoughItems(raw, mode);
    if (!items.length) return { text: EMPTY_MSG, empty: true };
    if (mode === "table") {
      const rows = items.map((item) => {
        const m = item.match(/^([^|:]+?)(?:\s*:\s+|\s+-\s+)(.+)$/);
        const col1 = capFirst((m ? m[1] : item).trim()).replace(/\|/g, "/");
        const col2 = (m ? m[2].trim() : "—").replace(/\|/g, "/");
        return `${col1} | ${col2}`;
      });
      return { text: ["Item | Details", "--- | ---", ...rows].join("\n"), empty: false };
    }
    const lines = items.map((item, i) => {
      const clean = capFirst(item);
      if (mode === "numbered") return `${i + 1}. ${clean}`;
      return mode === "checklist" ? `☐ ${clean}` : `• ${clean}`;
    });
    return { text: lines.join("\n"), empty: false };
  };

  const fallbackCopy = (text, done) => {
    const prev = document.activeElement, ta = Object.assign(document.createElement("textarea"), { value: text, readOnly: true });
    ta.style.cssText = "position:fixed;opacity:0;pointer-events:none";
    let ok = false;
    try {
      document.body.appendChild(ta);
      ta.select();
      ok = Boolean(document.execCommand("copy"));
    } catch {
      ok = false;
    } finally {
      ta.remove();
      prev?.focus?.();
    }
    done(ok);
  };

  const copyText = (text, done) => {
    if (!text) return;
    if (typeof navigator !== "undefined" && navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(text).then(() => done(true), () => fallbackCopy(text, done));
    } else {
      fallbackCopy(text, done);
    }
  };

  const syncRow = (row, items, cls, activeIdx, getLabel, onPick) => {
    if (!row) return;
    if (row.children.length !== items.length) {
      const hadFocus = row.contains(document.activeElement);
      row.replaceChildren(...items.map(() => Object.assign(document.createElement("button"), { type: "button" })));
      if (hadFocus && row.children.length) row.children[Math.max(0, Math.min(activeIdx, row.children.length - 1))].focus();
    }
    items.forEach((it, i) => {
      const b = row.children[i], on = i === activeIdx;
      b.className = cls + (on ? " on" : "");
      b.textContent = getLabel(it);
      b.setAttribute("aria-pressed", String(on));
      if (!b._pick) b.addEventListener("click", () => b._pick?.());
      b._pick = () => onPick(i);
    });
  };

  const init = () => {
    const root = document.querySelector("[data-tool]"), dataEl = document.getElementById("tool-data");
    if (!root || !dataEl) return;
    const cfg = JSON.parse(dataEl.textContent || "{}");
    const copyBtn = root.querySelector("[data-copy]"), copyLabel = root.querySelector("[data-copy-label]");
    const outEl = root.querySelector("[data-output]"), subEl = root.querySelector("[data-sub]"), badgeEl = root.querySelector("[data-badge]");
    let currentCopy = outEl ? outEl.textContent : "", copyTimer = null;
    const setCopy = (next) => {
      if (next !== currentCopy) {
        currentCopy = next;
        clearTimeout(copyTimer);
        if (copyLabel) copyLabel.textContent = "Copy";
      }
    };

    copyBtn?.addEventListener("click", () => {
      if (copyBtn.disabled) return;
      copyText(currentCopy, (ok) => {
        if (!ok || !copyLabel) return;
        copyLabel.textContent = "Copied";
        clearTimeout(copyTimer);
        copyTimer = setTimeout(() => { copyLabel.textContent = "Copy"; }, 1600);
      });
    });

    if (root.dataset.tool === "presets") {
      const groups = cfg.groups || [{ label: "", dir: "ltr", lang: "en", outLang: "en", presets: cfg.presets || [] }];
      let gIdx = 0, pIdx = 0, tIdx = 0;
      const groupRow = root.querySelector("[data-group-row]"), presetRow = root.querySelector("[data-preset-row]");
      const toneRow = root.querySelector("[data-tone-row]"), srcEl = root.querySelector("[data-source]");
      const render = () => {
        const g = groups[gIdx] || groups[0], presets = g.presets || [];
        if (pIdx >= presets.length) pIdx = 0;
        const p = presets[pIdx] || { raw: "", tones: [] }, tones = p.tones || [];
        if (tIdx >= tones.length) tIdx = 0;
        const tone = tones[tIdx] || { name: "", out: "", sub: "" };
        if (groups.length > 1) syncRow(groupRow, groups, "tool-tab", gIdx, (gr) => gr.label, (i) => { gIdx = i; pIdx = 0; tIdx = 0; render(); });
        syncRow(presetRow, presets, "tool-tab", pIdx, (pr) => pr.label, (i) => { pIdx = i; render(); });
        syncRow(toneRow, tones, "tool-chip", tIdx, (tn) => tn.name, (i) => { tIdx = i; render(); });
        if (srcEl) { srcEl.textContent = p.raw; srcEl.dir = p.dir || g.dir || "ltr"; srcEl.lang = p.lang || g.lang || "en"; }
        if (badgeEl) badgeEl.textContent = `${tone.name} result`;
        if (outEl) { outEl.textContent = tone.out; outEl.lang = tone.lang || p.outLang || g.outLang || "en"; }
        if (subEl) { subEl.textContent = tone.sub || ""; subEl.hidden = !tone.sub; }
        setCopy(tone.out);
      };
      render();
    } else if (root.dataset.tool === "notes") {
      const presets = cfg.presets || [], modes = cfg.modes || [];
      const presetRow = root.querySelector("[data-preset-row]"), modeRow = root.querySelector("[data-mode-row]"), inputEl = root.querySelector("[data-notes-input]");
      let activePreset = presets.findIndex((pr) => pr.raw === (inputEl ? inputEl.value : "")), activeMode = 0;
      const render = () => {
        const modeObj = modes[activeMode] || { id: "bullets", name: "Bullet points" };
        const res = formatRoughNotes(inputEl ? inputEl.value : "", modeObj.id);
        syncRow(presetRow, presets, "tool-tab", activePreset, (pr) => pr.label, (i) => { activePreset = i; if (inputEl) inputEl.value = presets[i].raw; render(); });
        syncRow(modeRow, modes, "tool-chip", activeMode, (md) => md.name, (i) => { activeMode = i; render(); });
        if (badgeEl) badgeEl.textContent = `${modeObj.name} result`;
        if (outEl) { outEl.textContent = res.text; outEl.dataset.empty = String(res.empty); }
        if (copyBtn) copyBtn.disabled = res.empty;
        setCopy(res.empty ? "" : res.text);
      };
      inputEl?.addEventListener("input", () => { activePreset = -1; render(); });
      render();
    }
  };

  if (typeof module !== "undefined" && module.exports) module.exports = { stripListMarker, formatRoughNotes };
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
  }
})();
