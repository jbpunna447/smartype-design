/* SmarType home: the story's motion, with GSAP + ScrollTrigger and native scrolling. Headings are typed over their own
   faint outline as they come into view. With reduced motion, or if a library fails to load, the page stays as written. */
(() => {
  const root = document.documentElement;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !window.gsap || !window.ScrollTrigger) return;
  root.classList.add("js");
  gsap.registerPlugin(ScrollTrigger);
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const seg = window.Intl && Intl.Segmenter ? new Intl.Segmenter(undefined, { granularity: "grapheme" }) : null;
  const graphemes = (t) => (seg ? [...seg.segment(t)].map((x) => x.segment) : Array.from(t));
  const onScreen = (el, fn) => ScrollTrigger.create({ trigger: el, start: "top bottom", end: "bottom top", onToggle: (s) => fn(s.isActive) });

  // ---------- typing ----------
  // A heading keeps its text, faint, as the layout and for screen readers; a copy on top is typed in over it, keeping
  // its <em> and <br>, then removed. Prepared up front so a heading never jumps from full to empty.
  function prepareHeading(el) {
    const src = document.createElement("span");
    src.className = "tw-src";
    while (el.firstChild) src.appendChild(el.firstChild);
    el.appendChild(src);
    const out = src.cloneNode(true);
    out.className = "tw-out";
    out.setAttribute("aria-hidden", "true");
    const texts = [];
    const walk = (n) => n.childNodes.forEach((c) => (c.nodeType === 3 ? texts.push([c, graphemes(c.textContent)]) : walk(c)));
    walk(out);
    // The untyped rest stays in place, hidden, so the copy always wraps exactly like the heading (also when centred).
    const rests = texts.map(([n]) => {
      const rest = document.createElement("span");
      rest.className = "tw-rest";
      rest.textContent = n.textContent;
      n.textContent = "";
      n.after(rest);
      return rest;
    });
    el.appendChild(out);
    const caret = document.createElement("i");
    caret.className = "caret";
    return async ({ speed = 26, pause = 160 } = {}) => {
      for (const [k, [n, chars]] of texts.entries()) {
        n.after(caret);
        for (const [j, ch] of chars.entries()) {
          n.textContent += ch;
          rests[k].textContent = chars.slice(j + 1).join("");
          await wait(/[.!?,]/.test(ch) ? pause : speed + Math.random() * 18);
        }
      }
      await wait(700);
      while (src.firstChild) el.insertBefore(src.firstChild, src);
      src.remove(); out.remove();
    };
  }

  // Types into a plain-text element, first deleting back to what the old and new text share.
  const jobs = new WeakMap();
  async function retype(el, text, { speed = 30, del = 12 } = {}) {
    const job = {};
    jobs.set(el, job);
    const now = graphemes(el.textContent), next = graphemes(text);
    let same = 0;
    while (same < now.length && same < next.length && now[same] === next[same]) same++;
    for (let i = now.length; i > same; i--) {
      if (jobs.get(el) !== job) return false;
      el.textContent = now.slice(0, i - 1).join("");
      await wait(del);
    }
    for (let i = same; i < next.length; i++) {
      if (jobs.get(el) !== job) return false;
      el.textContent = next.slice(0, i + 1).join("");
      await wait(speed + Math.random() * 24);
    }
    return true;
  }
  const markTypo = (el, word) => {
    if (word && el.textContent.includes(word)) el.innerHTML = el.textContent.replace(word, `<span class="typo">${word}</span>`);
  };

  $$("[data-type]").forEach((el) => {
    const play = prepareHeading(el);
    if (el.dataset.type === "hero") play({ speed: 48, pause: 320 });
    else ScrollTrigger.create({ trigger: el, start: "top 92%", once: true, onEnter: () => play() });
  });
  $$("[data-typeon]").forEach((el) => {
    const text = el.textContent;
    el.textContent = "";
    ScrollTrigger.create({ trigger: el, start: "top 88%", once: true, onEnter: () => {
      const i = $$("[data-typeon]", el.parentElement).indexOf(el);
      setTimeout(() => retype(el, text, { speed: 26 }), 250 + i * 400);
    } });
  });

  // ---------- reveals ----------
  gsap.to(".hero2 [data-reveal]", { opacity: 1, y: 0, duration: 1, ease: "expo.out", stagger: 0.12, delay: 0.2 });
  ScrollTrigger.batch(".hero2 ~ section [data-reveal]", {
    start: "top 92%", once: true,
    onEnter: (els) => gsap.to(els, { opacity: 1, y: 0, duration: 0.8, ease: "expo.out", stagger: 0.07 }),
  });

  // ---------- hero ----------
  gsap.from(".float", { scale: 0.5, opacity: 0, duration: 1.1, ease: "back.out(1.7)", stagger: 0.12, delay: 0.4 });
  gsap.from(".composer", { y: 50, opacity: 0, duration: 1.1, ease: "expo.out", delay: 0.3 });
  gsap.from(".hero2-art", { scale: 0.8, opacity: 0, duration: 1.2, ease: "back.out(1.4)", delay: 0.1 });

  // The composer shows three different moments: a typo fixed, a tone changed, a message translated.
  const cm = $(".cm-text"), cmAi = $(".cm-ai"), chip = (k) => $(`.cm-chip[data-k="${k}"]`);
  const moments = [
    { typed: "can we resceduel to friday", typo: "resceduel", button: cmAi, result: "Can we reschedule to Friday?" },
    { typed: "send me the report today", button: chip("pro"), result: "Could you send me the report by the end of today?" },
    { typed: "Thank you so much!", button: chip("hi"), result: "बहुत-बहुत धन्यवाद!" },
  ];
  let heroOn = true;
  onScreen(".hero2", (on) => (heroOn = on));
  (async function loop() {
    cm.textContent = "";
    await wait(1400);
    for (let i = 0; ; i = (i + 1) % moments.length) {
      while (!heroOn) await wait(400);
      const m = moments[i];
      await retype(cm, m.typed, { speed: 55 });
      markTypo(cm, m.typo);
      await wait(800);
      m.button.classList.add("lit");
      await wait(600);
      cm.textContent = m.typed;
      await retype(cm, m.result, { speed: 24 });
      await wait(400);
      m.button.classList.remove("lit");
      await wait(2200);
      await retype(cm, "", { del: 8 });
      await wait(400);
    }
  })();

  // Gentle parallax: the hero's bubbles follow the pointer a little; glows drift with the scroll.
  $$(".hero2 .float, .hero2 .composer").forEach((el) => {
    const d = +el.dataset.depth || 0.3;
    const x = gsap.quickTo(el, "x", { duration: 1.4, ease: "power3.out" }), y = gsap.quickTo(el, "y", { duration: 1.4, ease: "power3.out" });
    addEventListener("pointermove", (e) => { x((e.clientX / innerWidth - 0.5) * 36 * d); y((e.clientY / innerHeight - 0.5) * 24 * d); });
  });
  $$(".glow").forEach((el) => gsap.to(el, { yPercent: -40 * (+el.dataset.depth || 0.3), ease: "none",
    scrollTrigger: { trigger: el.closest("section"), start: "top top", end: "bottom top", scrub: true } }));

  $$(".magnetic").forEach((b) => {
    const x = gsap.quickTo(b, "x", { duration: 0.4, ease: "power3.out" }), y = gsap.quickTo(b, "y", { duration: 0.4, ease: "power3.out" });
    b.addEventListener("pointermove", (e) => {
      const r = b.getBoundingClientRect();
      x((e.clientX - r.left - r.width / 2) * 0.2); y((e.clientY - r.top - r.height / 2) * 0.3);
    });
    b.addEventListener("pointerleave", () => gsap.to(b, { x: 0, y: 0, duration: 0.9, ease: "elastic.out(1, .4)" }));
  });

  // ---------- story: auto-advancing accordion demo ----------
  const field = $(".field-text"), states = $$(".field .st").map((s) => ({ text: s.textContent, typo: s.dataset.typo }));
  const keys = $$(".phone-keys i"), pbs = $$(".pb[data-for]");
  const items = $$(".acc-item"), fills = $$(".acc-fill");
  let currentStep = -1, tapping = null, progressTween = null, isPaused = false, storyInView = false;
  const STEP_DURATION = 4.8;

  function tapKeys(on) {
    clearInterval(tapping);
    keys.forEach((k) => k.classList.remove("tap"));
    if (on) tapping = setInterval(() => {
      const k = keys[(Math.random() * keys.length) | 0];
      k.classList.add("tap"); setTimeout(() => k.classList.remove("tap"), 110);
    }, 95);
  }

  async function show(i) {
    if (i === currentStep) return;
    currentStep = i;
    items.forEach((item, j) => {
      item.classList.toggle("on", j === i);
      item.setAttribute("aria-selected", j === i ? "true" : "false");
    });
    pbs.forEach((p) => p.classList.toggle("lit", p.dataset.for === String(i)));
    tapKeys(i === 0);
    if (i === 3) field.textContent = "";
    const done = await retype(field, states[i].text, { speed: i === 0 ? 55 : 24 });
    tapKeys(false);
    if (done) markTypo(field, states[i].typo);
  }

  function startStep(i) {
    if (progressTween) progressTween.kill();
    fills.forEach((f, j) => gsap.set(f, { scaleX: 0 }));
    show(i);
    progressTween = gsap.to(fills[i], {
      scaleX: 1,
      duration: STEP_DURATION,
      ease: "none",
      onComplete: () => {
        if (!isPaused && storyInView) {
          startStep((currentStep + 1) % items.length);
        }
      }
    });
    if (!storyInView || isPaused) progressTween.pause();
  }

  items.forEach((item, i) => {
    item.addEventListener("click", () => startStep(i));
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        startStep(i);
      }
    });
  });

  const acc = $(".accordion");
  if (acc) {
    acc.addEventListener("pointerenter", () => {
      isPaused = true;
      if (progressTween) progressTween.pause();
    });
    acc.addEventListener("pointerleave", () => {
      isPaused = false;
      if (storyInView && progressTween) progressTween.resume();
    });
  }

  ScrollTrigger.create({
    trigger: ".story",
    start: "top 75%",
    end: "bottom 20%",
    onToggle: (self) => {
      storyInView = self.isActive;
      if (self.isActive) {
        if (currentStep === -1) startStep(0);
        else if (progressTween && !isPaused) progressTween.resume();
      } else {
        if (progressTween) progressTween.pause();
      }
    }
  });

  // ---------- tones: a sliding pill and the text retyped ----------
  const chips = $$(".chip"), pill = $(".chip-pill"), toneText = $(".tone-words");
  let toneIdx = 0, toneTimer, userPicked = false;
  const placePill = (c, instant) => gsap.to(pill, { x: c.offsetLeft, y: c.offsetTop, width: c.offsetWidth, height: c.offsetHeight,
    duration: instant ? 0 : 0.6, ease: "back.out(1.6)" });
  function pickTone(i, instant) {
    toneIdx = i;
    chips.forEach((c, j) => { c.classList.toggle("on", j === i); c.setAttribute("aria-pressed", j === i); });
    placePill(chips[i], instant);
    if (!instant) retype(toneText, chips[i].dataset.tone, { speed: 16, del: 5 });
  }
  pickTone(0, true);
  addEventListener("resize", () => placePill(chips[toneIdx], true));
  chips.forEach((c, i) => c.addEventListener("click", () => { userPicked = true; clearInterval(toneTimer); pickTone(i); }));
  ScrollTrigger.create({ trigger: ".tone", start: "top 60%", end: "bottom 30%", onToggle: (s) => {
    clearInterval(toneTimer);
    if (s.isActive && !userPicked) toneTimer = setInterval(() => pickTone((toneIdx + 1) % chips.length), 4500);
  } });

  // ---------- stacking cards: each one sinks back as the next arrives ----------
  const cards = $$(".card");
  cards.forEach((c, i) => {
    c.style.setProperty("--i", i);
    const next = cards[i + 1];
    if (!next) return;
    gsap.to(c, { scale: 0.94 + i * 0.012, ease: "none",
      scrollTrigger: { trigger: next, start: "top bottom", end: () => `top ${parseFloat(getComputedStyle(next).top)}px`, scrub: true } });
  });

  // ---------- voice: an equalizer that moves like speech (words, then pauses), with the words as they are heard ----------
  const voice = $(".mini.voice");
  if (voice) {
    const bars = $$(".eq i", voice), raw = $(".raw", voice), out = $(".mb.out", voice);
    const heard = raw.textContent.split(" "), tidy = out.textContent;
    let voiceOn = false, level = 0, target = 0;
    onScreen(voice, (on) => (voiceOn = on));
    raw.textContent = ""; out.textContent = "";
    out.style.visibility = "hidden";
    // Each bar has its own frequency band: the middle ones carry more of the voice.
    const weight = bars.map((_, i) => 0.45 + 0.55 * Math.sin((i / (bars.length - 1)) * Math.PI));
    const noise = bars.map(() => Math.random());
    gsap.ticker.add(() => {
      if (!voiceOn) return;
      level += (target - level) * 0.35;
      bars.forEach((b, i) => {
        noise[i] += (Math.random() - noise[i]) * 0.45;
        const h = 0.08 + level * weight[i] * (0.35 + 0.65 * noise[i]);
        b.style.transform = `scaleY(${Math.min(1, h).toFixed(3)})`;
      });
    });
    (async function speak() {
      for (;;) {
        while (!voiceOn) await wait(400);
        raw.textContent = ""; out.textContent = ""; out.style.visibility = "hidden";
        await wait(700);
        for (const w of heard) {
          // A word: a few syllables of varying loudness, then a short gap; fillers are quieter and longer.
          const filler = /^(uh|um,?)$/.test(w);
          const syllables = filler ? 1 : Math.max(1, Math.round(w.length / 3));
          for (let k = 0; k < syllables; k++) {
            target = (filler ? 0.35 : 0.6) + Math.random() * 0.4;
            await wait(filler ? 260 : 90 + Math.random() * 90);
            target = 0.25 + Math.random() * 0.15;
            await wait(40 + Math.random() * 40);
          }
          raw.textContent += (raw.textContent ? " " : "") + w;
          target = 0.02;
          await wait(w.endsWith(",") ? 320 : 70 + Math.random() * 120);
        }
        target = 0;
        await wait(700);
        out.style.visibility = "";
        await retype(out, tidy, { speed: 22 });
        await wait(3200);
      }
    })();
  }

  // ---------- languages: the globe key types one greeting at a time ----------
  const word = $(".hello-word"), names = $$(".lang-names li"), globe = $(".globe");
  let langsOn = false;
  onScreen(".langs", (on) => (langsOn = on));
  (async function greet() {
    for (let i = 0; ; i = (i + 1) % names.length) {
      while (!langsOn) await wait(400);
      names.forEach((n, j) => n.classList.toggle("on", j === i));
      gsap.fromTo(globe, { scale: 0.88 }, { scale: 1, duration: 0.5, ease: "back.out(3)" });
      await retype(word, "", { del: 30 });
      await retype(word, names[i].dataset.hello, { speed: 70 });
      await wait(1700);
    }
  })();

  // ---------- privacy: words drift inside the phone's ring and never get out ----------
  const orbit = $(".orbit");
  const words = $$(".kw").map((el) => ({ el, x: 0, y: 0, vx: 0, vy: 0, w: 0, h: 0 }));
  let R = 0, cx = 0, cy = 0, inView = false;
  function layout() {
    const s = orbit.offsetWidth;
    R = s / 2 - 8; cx = cy = s / 2;
    words.forEach((w, i) => {
      w.w = w.el.offsetWidth; w.h = w.el.offsetHeight;
      if (!w.x) {
        const a = (i / words.length) * Math.PI * 2, r = R * 0.62;
        w.x = cx + Math.cos(a) * r; w.y = cy + Math.sin(a) * r;
        w.vx = (Math.random() - 0.5) * 0.8; w.vy = (Math.random() - 0.5) * 0.8;
      }
    });
  }
  root.classList.add("physics");
  layout();
  addEventListener("resize", layout);
  onScreen(orbit, (on) => (inView = on));
  const coreR = () => orbit.offsetWidth * 0.15 + 10;
  gsap.ticker.add(() => {
    if (!inView) return;
    for (const w of words) {
      const sp = Math.hypot(w.vx, w.vy);
      if (sp < 0.3) { w.vx *= 1.05; w.vy *= 1.05; } else if (sp > 0.7) { w.vx *= 0.97; w.vy *= 0.97; }
      w.x += w.vx; w.y += w.vy;
      const dx = w.x - cx, dy = w.y - cy, d = Math.hypot(dx, dy), reach = Math.hypot(w.w, w.h) / 2;
      if (d + reach > R) {
        const nx = dx / d, ny = dy / d, dot = w.vx * nx + w.vy * ny;
        if (dot > 0) { w.vx -= 2 * dot * nx; w.vy -= 2 * dot * ny; }
        w.x = cx + nx * (R - reach); w.y = cy + ny * (R - reach);
      }
      const cr = coreR() + reach * 0.6;
      if (d < cr) {
        const nx = dx / (d || 1), ny = dy / (d || 1), dot = w.vx * nx + w.vy * ny;
        if (dot < 0) { w.vx -= 2 * dot * nx; w.vy -= 2 * dot * ny; }
        w.x = cx + nx * cr; w.y = cy + ny * cr;
      }
      w.el.style.transform = `translate(${w.x - w.w / 2}px, ${w.y - w.h / 2}px)`;
    }
  });
  gsap.from(".ring", { scale: 0.8, opacity: 0, duration: 1.2, ease: "expo.out", stagger: 0.1, scrollTrigger: { trigger: orbit, start: "top 80%" } });
  gsap.from(".off", { opacity: 0, x: -12, duration: 0.6, ease: "power3.out", stagger: 0.3, scrollTrigger: { trigger: ".pw", start: "top 85%" } });
})();
