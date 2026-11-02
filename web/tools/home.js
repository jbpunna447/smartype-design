/* SmarType home: the story's motion (GSAP + ScrollTrigger, native scrolling) and its interactions.
   One section moves at a time: the one crossing the middle of the screen; the others wait. Headings are typed over
   their own faint outline as they come into view. The steps, the styles and the privacy promises still switch on a tap
   with reduced motion, which shows each final state at once; without JavaScript the page shows everything as written. */
(() => {
  const root = document.documentElement;
  const motion = !matchMedia("(prefers-reduced-motion: reduce)").matches && !!(window.gsap && window.ScrollTrigger);
  root.classList.add("js");
  if (motion) {
    root.classList.add("motion");
    gsap.registerPlugin(ScrollTrigger);
  }
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const seg = window.Intl && Intl.Segmenter ? new Intl.Segmenter(undefined, { granularity: "grapheme" }) : null;
  const graphemes = (t) => (seg ? [...seg.segment(t)].map((x) => x.segment) : Array.from(t));
  // One-shot "when it scrolls into view": IntersectionObserver stays right when content above changes height.
  const whenSeen = (el, fn, margin = "0px 0px -10% 0px") => {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { io.disconnect(); fn(); } }), { rootMargin: margin });
    io.observe(el);
  };
  const press = (el, ms = 160) => {
    if (!el) return;
    el.classList.add("tap");
    setTimeout(() => el.classList.remove("tap"), ms);
  };

  // ---------- focus: only the part crossing the middle of the screen plays ----------
  const watchers = new Map();
  const band = new IntersectionObserver((es) => es.forEach((e) => {
    e.target.classList.toggle("is-focus", e.isIntersecting);
    (watchers.get(e.target) || []).forEach((fn) => fn(e.isIntersecting));
  }), { rootMargin: "-45% 0px -45% 0px" });
  const onFocus = (el, fn) => {
    if (!watchers.has(el)) { watchers.set(el, []); band.observe(el); }
    watchers.get(el).push(fn);
  };

  // A scene plays one sequence at a time: starting a new one ends the old one, and the scene can pause.
  function scene() {
    let run = 0;
    const s = {
      paused: false,
      start: () => ++run,
      // Waits ms of unpaused time; false once a newer sequence has started.
      async hold(id, ms) {
        while (ms > 0) {
          if (id !== run) return false;
          const t = Math.min(ms, 40);
          await wait(t);
          if (!s.paused) ms -= t;
        }
        return id === run;
      },
    };
    return s;
  }

  // Types into a plain-text element, first deleting back to what the old and new text share.
  async function typeTo(el, text, { speed = 30, del = 12, hold = (ms) => wait(ms).then(() => true), onChar } = {}) {
    const now = graphemes(el.textContent), next = graphemes(text);
    let same = 0;
    while (same < now.length && same < next.length && now[same] === next[same]) same++;
    for (let i = now.length; i > same; i--) {
      if (!(await hold(del))) return false;
      el.textContent = now.slice(0, i - 1).join("");
    }
    for (let i = same; i < next.length; i++) {
      if (!(await hold(speed + Math.random() * 24))) return false;
      el.textContent = next.slice(0, i + 1).join("");
      if (onChar) onChar(next[i]);
    }
    return true;
  }
  // Underlines a misspelt word, as the keyboard does.
  const markTypo = (el, word) => {
    const t = el.textContent, at = t.indexOf(word);
    if (!word || at < 0) return;
    const span = document.createElement("span");
    span.className = "typo";
    span.textContent = word;
    el.replaceChildren(t.slice(0, at), span, t.slice(at + word.length));
  };

  // ---------- headings: typed over their own faint outline ----------
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
      setTimeout(() => {
        while (src.firstChild) el.insertBefore(src.firstChild, src);
        src.remove();
        out.remove();
      }, 700);
    };
  }

  if (motion) {
    let heroTyped = Promise.resolve();
    $$("[data-type]").forEach((el) => {
      const play = prepareHeading(el);
      if (el.dataset.type === "hero") heroTyped = play({ speed: 30, pause: 180 });
      else whenSeen(el, () => play(), "0px 0px -8% 0px");
    });
    $$("[data-typeon]").forEach((el) => {
      const text = el.textContent;
      el.textContent = "";
      whenSeen(el, () => {
        const i = $$("[data-typeon]", el.parentElement).indexOf(el);
        setTimeout(() => typeTo(el, text, { speed: 26 }), 250 + i * 400);
      }, "0px 0px -12% 0px");
    });

    // ---------- reveals: the hero's words at once, its picture once the heading is typed ----------
    gsap.to(".hero2 [data-reveal]", { opacity: 1, y: 0, duration: 1, ease: "expo.out", stagger: 0.1, delay: 0.15 });
    Promise.race([heroTyped, wait(2400)]).then(() => gsap.to(".hero2-art", { opacity: 1, duration: 0.9, ease: "power2.out" }));
    $$(".hero2 ~ section [data-reveal]").forEach((el) => whenSeen(el, () => {
      const sibs = $$("[data-reveal]", el.parentElement);
      gsap.to(el, { opacity: 1, y: 0, duration: 0.8, ease: "expo.out", delay: Math.max(0, sibs.indexOf(el)) * 0.07 });
    }, "0px 0px -8% 0px"));
    // The glows drift a little with the scroll; nothing moves on its own.
    $$(".glow").forEach((el) => gsap.to(el, { yPercent: -40 * (+el.dataset.depth || 0.3), ease: "none",
      scrollTrigger: { trigger: el.closest("section"), start: "top top", end: "bottom top", scrub: true } }));
  }

  // ---------- how it works: each step plays on the phone ----------
  const story = $("#how"), acc = $(".accordion");
  if (story && acc) {
    const items = $$(".acc-item"), heads = $$(".acc-head"), fills = $$(".acc-fill");
    const ph = $(".phone", story), field = $(".field-text", story), ime = $(".ime", story), sugg = $$(".ime-sugg span", story);
    const T = { rough: ph.dataset.rough, fixed: ph.dataset.fixed, hindi: ph.dataset.hindi, spoken: ph.dataset.spoken };
    const keys = new Map($$(".krow i[data-c]", ime).map((k) => [k.dataset.c, k]));
    const keyFor = (ch) => keys.get(ch.toLowerCase()) || (/[,.!?]/.test(ch) ? keys.get(".") : null);
    const bar = (k) => $(`.ime-bar .sb[data-k="${k}"]`, ime);
    const result = (k) => $(`.ip-${k} .ip-text`, ime);
    const replace = (k) => $(`.ip-${k} .ip-btn.ai`, ime);
    const recT = $(".rec-t", ime), eq = $$(".veq i", ime);
    const SUGG = { great: ["great", "Great", "greatly"], can: ["can", "can't", "call"], u: ["u", "you", "us"],
      send: ["send", "sending", "sent"], the: ["the", "them", "they"], adress: ["adress", "address", "addresses"] };
    const DUR = [5, 6.8, 6.6, 7];
    const sc = scene();
    let step = 0, auto = true, inView = false, hovering = false, listening = false, started = false;
    const setSugg = (w) => sugg.forEach((s, i) => (s.textContent = w[i] || ""));
    const setField = (text, typo) => { field.textContent = text; if (typo) markTypo(field, typo); };
    const closeAll = () => { ime.dataset.open = ""; ime.classList.remove("voice", "tidy"); listening = false; };

    // Where each step starts, so any step can play on its own, and where it ends (shown at once with reduced motion).
    function begin(i) {
      closeAll();
      result("fix").textContent = ""; result("tr").textContent = "";
      if (i === 0) { setField(""); setSugg(["I", "Great", "The"]); }
      if (i === 1) { setField(T.rough, "adress"); setSugg(SUGG.adress); }
      if (i === 2) { setField(T.fixed); setSugg(["Thanks", "Sure", "See"]); }
      if (i === 3) { setField(""); setSugg(["I", "Can't", "See"]); }
    }
    function end(i) {
      begin(i);
      result("fix").textContent = T.fixed; result("tr").textContent = T.hindi;
      if (i === 0) setField(T.rough, "adress");
      if (i === 1) setField(T.fixed);
      if (i === 2) setField(T.hindi);
      if (i === 3) setField(T.spoken);
    }

    async function play(i) {
      const id = sc.start(), hold = (ms) => sc.hold(id, ms);
      begin(i);
      if (i === 0) {
        if (!(await hold(500))) return;
        let word = "";
        const done = await typeTo(field, T.rough, { speed: 62, hold, onChar: (ch) => {
          press(keyFor(ch), 130);
          word = /[a-z]/i.test(ch) ? word + ch.toLowerCase() : "";
          const w = word && Object.keys(SUGG).find((k) => k.startsWith(word));
          if (w) setSugg(SUGG[w]);
        } });
        if (done) markTypo(field, "adress");
      } else if (i === 1 || i === 2) {
        // Tap Rewrite or Translate: its panel takes the keyboard's place; Replace puts the result in the message.
        const k = i === 1 ? "fix" : "tr", out = i === 1 ? T.fixed : T.hindi, r = result(k);
        if (!(await hold(700))) return;
        press(bar(k), 260);
        if (!(await hold(320))) return;
        ime.dataset.open = k;
        r.classList.add("wait");
        if (!(await hold(1000))) { r.classList.remove("wait"); return; }
        r.classList.remove("wait");
        if (!(await typeTo(r, out, { speed: 14, hold }))) return;
        if (!(await hold(900))) return;
        press(replace(k), 260);
        if (!(await hold(380))) return;
        ime.dataset.open = "";
        setField(out);
      } else {
        // Speak: the voice bar takes the smartbar's place; the words are tidied up and land in the message.
        if (!(await hold(600))) return;
        press(bar("mic"), 260);
        if (!(await hold(300))) return;
        ime.classList.add("voice");
        listening = true;
        for (let t = 0; t <= 3; t++) {
          recT.textContent = `0:0${t}`;
          if (!(await hold(t === 3 ? 400 : 900))) return;
        }
        listening = false;
        ime.classList.add("tidy");
        if (!(await hold(1100))) return;
        ime.classList.remove("voice", "tidy");
        await typeTo(field, T.spoken, { speed: 18, hold });
      }
    }

    // The equalizer moves like speech: bursts of syllables of varying loudness, with short gaps between words.
    if (motion) {
      const weight = eq.map((_, i) => 0.45 + 0.55 * Math.sin((i / (eq.length - 1)) * Math.PI));
      const noise = eq.map(() => Math.random());
      let level = 0, target = 0, next = 0;
      gsap.ticker.add(() => {
        const live = listening && !sc.paused;
        if (!live && level < 0.01) return;
        const now = performance.now();
        if (live && now > next) {
          const gap = Math.random() < 0.18;
          target = gap ? 0.04 : 0.45 + Math.random() * 0.55;
          next = now + (gap ? 180 + Math.random() * 160 : 90 + Math.random() * 110);
        }
        if (!live) target = 0;
        level += (target - level) * 0.3;
        eq.forEach((b, i) => {
          noise[i] += (Math.random() - noise[i]) * 0.45;
          b.style.transform = `scaleY(${Math.min(1, 0.08 + level * weight[i] * (0.35 + 0.65 * noise[i])).toFixed(3)})`;
        });
      });
    }

    // Steps advance on their own, with the bar filling, until you pick one; then that step stays.
    function select(i, user) {
      step = i;
      if (user) auto = false;
      items.forEach((it, j) => {
        it.classList.toggle("on", j === i);
        heads[j].setAttribute("aria-expanded", String(j === i));
      });
      fills.forEach((f) => { f.classList.remove("run"); f.style.transform = ""; });
      if (auto && motion) {
        void fills[i].offsetWidth;
        fills[i].style.setProperty("--dur", `${DUR[i]}s`);
        fills[i].classList.add("run");
      } else fills[i].style.transform = "scaleX(1)";
      if (motion) play(i); else end(i);
    }
    fills.forEach((f, i) => f.addEventListener("animationend", () => { if (auto && i === step) select((i + 1) % items.length); }));
    // A step you pick plays at once, also before the section reaches the middle of the screen.
    heads.forEach((h, i) => h.addEventListener("click", () => { started = inView = true; sync(); select(i, true); }));
    // Out of focus everything waits. A pointer resting on the steps only holds the bar, so the step being read stays
    // while its phone plays on.
    const sync = () => {
      sc.paused = !inView;
      acc.classList.toggle("paused", !inView || hovering);
    };
    acc.addEventListener("pointerenter", (e) => { if (e.pointerType === "mouse") { hovering = true; sync(); } });
    acc.addEventListener("pointerleave", () => { hovering = false; sync(); });
    if (motion) {
      begin(0);
      onFocus(story, (on) => {
        inView = on;
        if (on && !started) { started = true; select(0); }
        sync();
      });
    } else select(0);
  }

  // ---------- styles: a sliding pill and the message retyped ----------
  const toneSec = $("#styles");
  if (toneSec) {
    const chips = $$(".chip", toneSec), pill = $(".chip-pill", toneSec), words = $(".tone-words", toneSec), text = $(".tone-text", toneSec);
    const ts = scene();
    let idx = 0, picked = false, started = false;
    const place = (instant) => {
      const c = chips[idx];
      if (instant) pill.style.transition = "none";
      pill.style.width = `${c.offsetWidth}px`;
      pill.style.height = `${c.offsetHeight}px`;
      pill.style.transform = `translate(${c.offsetLeft}px, ${c.offsetTop}px)`;
      if (instant) { void pill.offsetWidth; pill.style.transition = ""; }
    };
    // Until you pick one, each style is typed in, stays long enough to read and hands over to the next.
    const READ = 2600;
    async function pick(i) {
      idx = i;
      chips.forEach((c, j) => { c.classList.toggle("on", j === i); c.setAttribute("aria-pressed", String(j === i)); });
      place();
      if (!motion) { words.textContent = chips[i].dataset.tone; return; }
      const id = ts.start(), hold = (ms) => ts.hold(id, ms);
      if (!(await typeTo(words, chips[i].dataset.tone, { speed: 16, del: 5, hold }))) return;
      if (!picked && (await hold(READ))) pick((i + 1) % chips.length);
    }
    chips.forEach((c, i) => c.addEventListener("click", () => {
      picked = true;
      ts.paused = false;
      text.setAttribute("aria-live", "polite");
      pick(i);
    }));
    place(true);
    addEventListener("resize", () => place(true));
    if (document.fonts) document.fonts.ready.then(() => place(true));
    if (motion) onFocus(toneSec, (on) => {
      ts.paused = !on;
      if (!on || started || picked) return;
      started = true;
      const id = ts.start();
      ts.hold(id, READ).then((go) => { if (go && !picked) pick(1); });
    });
  }

  // ---------- everything around it: stacking cards ----------
  const cards = $$(".card");
  if (motion && cards.length) {
    // Card i's scale is 1 - STEP x (how many later cards have arrived), so in the finished stack each card is one step
    // smaller than the one above it, and the visible edges are equally spaced (the sticky tops are 16 px apart).
    const STEP = 0.035, arrived = cards.map(() => 0);
    const setScale = cards.map((c) => gsap.quickSetter(c, "scale"));
    const restack = () => cards.forEach((c, i) => setScale[i](1 - STEP * arrived.slice(i + 1).reduce((a, b) => a + b, 0)));
    cards.forEach((c, i) => {
      c.style.setProperty("--i", i);
      if (i === 0) return;
      ScrollTrigger.create({ trigger: c, start: "top bottom", end: () => `top ${parseFloat(getComputedStyle(c).top)}px`,
        onUpdate: (st) => { arrived[i] = st.progress; restack(); } });
    });
  } else cards.forEach((c, i) => c.style.setProperty("--i", i));

  // The languages card types one greeting at a time while it is in front.
  const langs = $(".c-langs");
  if (langs) {
    const word = $(".hello-word", langs), names = $$(".lang-names li", langs), globe = $(".globe", langs);
    names[0].classList.add("on");
    if (motion) {
      const ls = scene();
      let started = false;
      const loop = async () => {
        const id = ls.start(), hold = (ms) => ls.hold(id, ms);
        for (let i = 1; ; i = (i + 1) % names.length) {
          if (!(await hold(1600))) return;
          names.forEach((n, j) => n.classList.toggle("on", j === i));
          gsap.fromTo(globe, { scale: 0.86 }, { scale: 1, duration: 0.5, ease: "back.out(3)" });
          if (!(await typeTo(word, "", { del: 28, hold }))) return;
          if (!(await typeTo(word, names[i].dataset.hello, { speed: 70, hold }))) return;
        }
      };
      onFocus(langs, (on) => {
        ls.paused = !on;
        if (on && !started) { started = true; loop(); }
      });
    }
  }

  // ---------- privacy: one promise at a time, shown as where your text goes ----------
  const vault = $("#privacy"), seal = $(".seal");
  if (vault && seal) {
    const vows = $$(".vow", vault), btns = $$(".vow button", vault);
    const text = $(".seal-text", seal), label = $(".seal-label", seal), badge = $(".seal-badge", seal), packet = $(".packet", seal);
    const tag = $(".pipe-tag span", seal), ai = $(".seal-ai", seal), spark = $('.seal-bar .sb[data-k="fix"]', seal);
    const S = { rough: seal.dataset.rough, fixed: seal.dataset.fixed, dots: "••••••••" };
    const HEX = "0123456789abcdef";
    const cipher = (n) => Array.from({ length: n }, () => HEX[(Math.random() * 16) | 0] + HEX[(Math.random() * 16) | 0]).join(" ");
    const ps = scene();
    let auto = true, started = false, scramble = null;
    const stopScramble = () => { clearInterval(scramble); scramble = null; };

    function state(i) {
      stopScramble();
      seal.classList.remove("p0", "p1", "p2", "pw");
      seal.classList.add(`p${i}`);
      seal.classList.toggle("pw", i === 2);
      label.textContent = i === 2 ? "Password" : "Message";
      badge.textContent = ["Stays here", "Sent on your tap", "Password field"][i];
      tag.textContent = i === 1 ? "Encrypted" : "Nothing leaves";
      packet.classList.remove("go");
      ai.classList.remove("busy");
      text.classList.remove("sel");
    }
    function end(i) {
      state(i);
      text.textContent = [S.rough, S.fixed, S.dots][i];
      if (i === 1) { packet.textContent = cipher(3); packet.style.top = "50%"; packet.classList.add("go"); }
    }
    // Back on the phone the message is readable again: the code resolves into the fixed text, left to right.
    async function decode(el, to, hold) {
      const chars = graphemes(to);
      for (let k = 0; k <= chars.length; k += 2) {
        el.textContent = chars.slice(0, k).join("") + chars.slice(k).map((c) => (c === " " ? " " : HEX[(Math.random() * 16) | 0])).join("");
        if (!(await hold(30))) return false;
      }
      el.textContent = to;
      return true;
    }
    async function run(i) {
      const id = ps.start(), hold = (ms) => ps.hold(id, ms);
      state(i);
      if (i === 0) {
        text.textContent = "";
        if (!(await hold(500))) return;
        if (!(await typeTo(text, S.rough, { speed: 60, hold }))) return;
      } else if (i === 1) {
        text.textContent = S.rough;
        if (!(await hold(700))) return;
        press(spark, 260);
        text.classList.add("sel");
        if (!(await hold(450))) return;
        // Only now does anything leave: sealed as code, down the line to AI and back.
        packet.textContent = cipher(3);
        scramble = setInterval(() => (packet.textContent = cipher(3)), 70);
        packet.style.transition = "none";
        packet.style.top = "0%";
        void packet.offsetWidth;
        packet.style.transition = "";
        packet.classList.add("go");
        packet.style.top = "100%";
        if (!(await hold(950))) return;
        ai.classList.add("busy");
        if (!(await hold(800))) return;
        ai.classList.remove("busy");
        packet.style.top = "0%";
        if (!(await hold(950))) return;
        stopScramble();
        packet.classList.remove("go");
        text.classList.remove("sel");
        if (!(await decode(text, S.fixed, hold))) return;
      } else {
        text.textContent = "";
        if (!(await hold(500))) return;
        if (!(await typeTo(text, S.dots, { speed: 110, hold }))) return;
      }
      if (!(await hold(i === 1 ? 1600 : 1900))) return;
      if (auto) select((i + 1) % vows.length);
    }
    function select(i, user) {
      if (user) auto = false;
      vows.forEach((v, j) => { v.classList.toggle("on", j === i); btns[j].setAttribute("aria-pressed", String(j === i)); });
      if (motion) run(i); else end(i);
    }
    btns.forEach((b, i) => b.addEventListener("click", () => { started = true; ps.paused = false; select(i, true); }));
    if (motion) {
      state(0);
      text.textContent = "";
      onFocus(vault, (on) => {
        ps.paused = !on;
        if (on && !started) { started = true; select(0); }
      });
    } else select(0);
  }
})();
