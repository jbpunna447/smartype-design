/* SmarType: the header on every page. It turns more solid once the page scrolls, opens the Menu sheet on phones and,
   on the home page, moves its highlight to the link of the section crossing the middle of the screen. */
(() => {
  const root = document.documentElement;
  const scrolled = () => root.classList.toggle("scrolled", scrollY > 8);
  addEventListener("scroll", scrolled, { passive: true });
  scrolled();

  const btn = document.querySelector(".menu-btn"), menu = document.getElementById("menu");
  if (btn && menu) {
    const open = (on) => {
      menu.hidden = !on;
      btn.setAttribute("aria-expanded", String(on));
      btn.textContent = on ? "Close" : "Menu";
    };
    btn.addEventListener("click", () => open(menu.hidden));
    menu.addEventListener("click", (e) => { if (e.target.closest("a")) open(false); });
    document.addEventListener("click", (e) => { if (!menu.hidden && !e.target.closest(".top")) open(false); });
    addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !menu.hidden) { open(false); btn.focus(); }
    });
    matchMedia("(min-width: 861px)").addEventListener("change", (m) => { if (m.matches) open(false); });
  }

  // Styles belongs to Features in the header.
  const owner = { how: "how", styles: "features", features: "features", privacy: "privacy" };
  const sections = Object.keys(owner).map((id) => document.getElementById(id)).filter(Boolean);
  const nav = document.querySelector(".top-nav"), hl = document.querySelector(".nav-hl");
  if (!nav || !hl || !sections.length) return;
  const links = [...document.querySelectorAll("a[data-sec]")];
  let current = null;
  const place = () => {
    const a = current && nav.querySelector(`a[data-sec="${current}"]`);
    if (!a) { hl.style.opacity = "0"; return; }
    // Appearing, the highlight starts under its link instead of sliding in from the left.
    const fresh = hl.style.opacity !== "1";
    if (fresh) hl.style.transition = "opacity .25s";
    hl.style.width = `${a.offsetWidth}px`;
    hl.style.transform = `translateX(${a.offsetLeft}px)`;
    if (fresh) { void hl.offsetWidth; hl.style.transition = ""; }
    hl.style.opacity = "1";
  };
  const show = (key) => {
    if (key === current) return;
    current = key;
    links.forEach((a) => a.classList.toggle("on", a.dataset.sec === key));
    place();
  };
  const inBand = new Set();
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => (e.isIntersecting ? inBand.add(e.target) : inBand.delete(e.target)));
    const s = sections.find((x) => inBand.has(x));
    show(s ? owner[s.id] : null);
  }, { rootMargin: "-45% 0px -45% 0px" });
  sections.forEach((s) => io.observe(s));
  addEventListener("resize", place);
  if (document.fonts) document.fonts.ready.then(place);
})();
