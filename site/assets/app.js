/* IES Training — portal estático de cursos. Rutas por hash, progreso en localStorage. */
(() => {
  "use strict";
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
  const main = $("#main");
  const KEY = "iesTraining.v2";
  const framed = (() => { try { return window.self !== window.top; } catch { return true; } })();

  /* ---------- forma IES (del logo) ---------- */
  const FORMA = "M14,160 C14,60 60,14 160,14 L620,16 C1000,28 1450,95 1700,180 C1880,245 1934,360 1934,540 L1934,1370 C1934,1480 1880,1518 1770,1518 L1200,1518 C820,1508 450,1460 260,1385 C80,1315 14,1210 14,1050 Z";
  const CLIP = "M 0 0.0971 C 0 0.0306 0.024 0 0.076 0 L 0.3156 0.0013 C 0.5135 0.0093 0.7479 0.0539 0.8781 0.1104 C 0.9719 0.1536 1 0.2301 1 0.3497 L 1 0.9016 C 1 0.9747 0.9719 1 0.9146 1 L 0.6177 1 C 0.4198 0.9934 0.2271 0.9614 0.1281 0.9116 C 0.0344 0.865 0 0.7952 0 0.6888 Z";
  document.body.insertAdjacentHTML("afterbegin", `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><clipPath id="formaIES" clipPathUnits="objectBoundingBox"><path d="${CLIP}"/></clipPath></svg>`);
  const shape = (stroke = "rgba(23,168,212,.75)", w = 10) => `<svg class="shape" viewBox="0 0 1952 1536" aria-hidden="true"><path d="${FORMA}" fill="none" stroke="${stroke}" stroke-width="${w}"/><path d="${FORMA}" transform="translate(976 768) scale(.8) translate(-976 -768)" fill="none" stroke="${stroke}" stroke-opacity=".45" stroke-width="${w * .8}"/></svg>`;

  /* ---------- íconos (trazo) ---------- */
  const P = {
    router: '<rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 16.5h.01M11 16.5h.01"/><path d="M8.5 9.5a5 5 0 0 1 7 0M6 7a8.5 8.5 0 0 1 12 0"/><path d="M12 13v-1.5"/>',
    phone: '<rect x="4" y="3" width="9" height="18" rx="2"/><path d="M7 7h3M15 7h5v12h-5M17 11h1M17 14h1"/>',
    wifi: '<path d="M5 12.5a10 10 0 0 1 14 0M8 15.5a5.5 5.5 0 0 1 8 0M2 9.5a14.5 14.5 0 0 1 20 0"/><circle cx="12" cy="19" r="1.2"/>',
    ap: '<ellipse cx="12" cy="13" rx="8" ry="3"/><path d="M4 13v2c0 1.7 3.6 3 8 3s8-1.3 8-3v-2"/><path d="M8.5 6.5a5 5 0 0 1 7 0M10.5 8.7a2 2 0 0 1 3 0"/>',
    door: '<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><circle cx="12" cy="7.5" r="2"/><path d="M9.5 12.5h5M9.5 15.5h5M10.5 18.5h3"/>',
    camera: '<path d="M3 8.5 15 5l2 5-12 3.5z"/><path d="m17 10 3.5 1.5M9 13l1 4M6 17h8"/><circle cx="12.5" cy="8.5" r="1"/>',
    server: '<rect x="3.5" y="3" width="17" height="7" rx="1.8"/><rect x="3.5" y="14" width="17" height="7" rx="1.8"/><path d="M7 6.5h.01M7 17.5h.01M11 6.5h5M11 17.5h5M12 10v4"/>',
    layers: '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/><path d="m3 17.5 9 4.5 9-4.5" opacity=".6"/>',
    window: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M12 9v11M6 6.5h.01M8.5 6.5h.01"/>',
    terminal: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 10 3 2.5L7 15M12.5 15.5H17"/>',
    check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    chev: '<path d="m9 5 7 7-7 7"/>',
    back: '<path d="M15 5 8 12l7 7"/>',
    book: '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
    flask: '<path d="M9 3h6M10 3v6l-5.5 9.5A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.5L14 9V3"/><path d="M7.5 15h9"/>',
    quiz: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.6 2.6 0 0 1 5 .8c0 1.7-2.5 2.2-2.5 3.7M12 17h.01"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    award: '<circle cx="12" cy="9" r="6"/><path d="m8.5 13.8-1.5 7.2 5-2.5 5 2.5-1.5-7.2"/>',
    pin: '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    doc: '<path d="M14 3H6.5A1.5 1.5 0 0 0 5 4.5v15A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V8z"/><path d="M14 3v5h5M8.5 13h7M8.5 16.5h5"/>',
    link: '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3A4.5 4.5 0 0 0 13 4.6l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3A4.5 4.5 0 0 0 11 19.4l1-1"/>',
    chat: '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    split: '<path d="M6 3v6a4 4 0 0 0 4 4h4a4 4 0 0 1 4 4v4M18 3v4M6 21v-4"/>',
    shield: '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6z"/><path d="m9 12 2 2 4-4"/>',
    flame: '<path d="M12 21c-3.9 0-6.5-2.6-6.5-6.2 0-3.2 2.2-5.3 3.6-7.6.4 1.6 1.3 2.7 2.4 3.3.1-2.8 1.3-5.2 3.4-7.5.3 3 1.7 4.6 3 6.4.9 1.3 1.6 2.8 1.6 4.9 0 3.9-3 6.7-7.5 6.7z"/><path d="M12 21c-1.8 0-3-1.2-3-2.9 0-1.6 1.2-2.6 2-3.8.9 1.4 2.9 2.3 3.6 3.8.5 1.5-.6 2.9-2.6 2.9z"/>',
    upload: '<path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 15v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/>',
    grip: '<circle cx="9" cy="6" r="1.2"/><circle cx="15" cy="6" r="1.2"/><circle cx="9" cy="12" r="1.2"/><circle cx="15" cy="12" r="1.2"/><circle cx="9" cy="18" r="1.2"/><circle cx="15" cy="18" r="1.2"/>',
    lock: '<rect x="5" y="10.5" width="14" height="10.5" rx="2.2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
    grid: '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
    pulse: '<path d="M3 12h4l2.5-6 5 12 2.5-6h4"/>',
    eye: '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    download: '<path d="M12 4v12M7 11l5 5 5-5"/><path d="M4 15v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/>',
    userplus: '<circle cx="10" cy="8" r="3.5"/><path d="M3.5 20a6.5 6.5 0 0 1 13 0M19 8v6M16 11h6"/>',
    search: '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    building: '<path d="M4 21V5.5A1.5 1.5 0 0 1 5.5 4h8A1.5 1.5 0 0 1 15 5.5V21M15 10h3.5A1.5 1.5 0 0 1 20 11.5V21M2.5 21h19M7.5 8h4M7.5 11.5h4M7.5 15h4"/>',
    key: '<circle cx="8" cy="15" r="4"/><path d="m11 12 8.5-8.5M16 7l2.5 2.5M14 9l2 2"/>',
    edit: '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    history: '<path d="M3.5 12a8.5 8.5 0 1 0 2.5-6L3.5 8.5"/><path d="M3.5 4v4.5H8M12 8v4.5l3 2"/>',
    sort: '<path d="M7 4v16M3.5 7.5 7 4l3.5 3.5M17 20V4M13.5 16.5 17 20l3.5-3.5"/>',
    clip: '<rect x="8" y="3" width="8" height="4" rx="1"/><path d="M8 5H6a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2"/>',
    trash: '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
    image: '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="9.5" r="1.8"/><path d="m21 16-5-5-9 9"/>',
    login: '<path d="M14 4h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4M10 16l4-4-4-4M14 12H3"/>',
    dot: '<circle cx="12" cy="12" r="3"/>',
    users: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14a6.5 6.5 0 0 1 3.5 6"/>'
  };
  const icon = (n, cls = "i") => `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true">${P[n] || ""}</svg>`;

  const META = {
    mikrotik: {cat: "redes", glyph: "router"}, unifi: {cat: "redes", glyph: "ap"}, omada: {cat: "redes", glyph: "wifi"},
    grandstream: {cat: "telefonia", glyph: "phone"}, akuvox: {cat: "seguridad", glyph: "door"}, hikcentral: {cat: "seguridad", glyph: "camera"},
    proxmox: {cat: "servidores", glyph: "server"}, vmware: {cat: "servidores", glyph: "layers"},
    windows: {cat: "sistemas", glyph: "window"}, linux: {cat: "sistemas", glyph: "terminal"},
    paradox: {cat: "seguridad", glyph: "shield"}, "bosch-incendio": {cat: "seguridad", glyph: "flame"}
  };
  const CATS = [["todos", "Todos"], ["redes", "Redes y WiFi"], ["telefonia", "Telefonía IP"], ["seguridad", "Seguridad electrónica"], ["servidores", "Virtualización"], ["sistemas", "Sistemas operativos"]];
  const PATHS = [
    {title: "Técnico de redes", text: "Del router del cliente al WiFi bien hecho, con gestión remota y multi-sitio.", courses: ["mikrotik", "unifi", "omada"], feat: true},
    {title: "Seguridad electrónica", text: "Portería IP, videovigilancia, alarmas, detección de incendio y la central telefónica que las une.", courses: ["akuvox", "hikcentral", "paradox", "bosch-incendio", "grandstream"]},
    {title: "Servidores e infraestructura", text: "Los equipos donde corren el VMS, la central y los servicios: sistemas operativos y virtualización.", courses: ["linux", "windows", "proxmox", "vmware"]}
  ];

  /* ---------- progreso ---------- */
  const store = {
    data: (() => { try { return JSON.parse(localStorage.getItem(KEY)) || {l: {}, name: ""}; } catch { return {l: {}, name: ""}; } })(),
    save() { try { localStorage.setItem(KEY, JSON.stringify(this.data)); } catch {} },
    get(slug, n) { return this.data.l[`${slug}/${n}`] || {}; },
    set(slug, n, patch) {
      const k = `${slug}/${n}`; const cur = {...(this.data.l[k] || {}), ...patch};
      if (patch.done === undefined && cur.lab && cur.quiz && cur.quiz.done) cur.done = true;
      this.data.l[k] = cur; this.save();
    },
    level(slug, n) { const p = this.get(slug, n); return p.done ? 2 : (p.seen || p.lab || (p.quiz && p.quiz.a && p.quiz.a.length)) ? 1 : 0; },
    courseDone(slug, lessons) { return lessons.filter(l => this.get(slug, lid(l)).done).length; },
    started(slug, lessons) { return lessons.some(l => this.level(slug, lid(l)) > 0); },
    totals() {
      const v = Object.values(this.data.l);
      return {done: v.filter(x => x.done).length, labs: v.filter(x => x.lab).length, quizzes: v.filter(x => x.quiz && x.quiz.done).length, rules: v.filter(x => x.rule).length};
    },
    reset() { this.data = {l: {}, name: this.data.name || ""}; this.save(); }
  };

  /* ---------- datos ---------- */
  let catalog = null; const courses = {};
  // caché en memoria por 2 minutos: una pestaña abierta mucho tiempo ve lo que se publica después
  const FRESH = 120000; let catT = 0; const courseT = {};
  const getCatalog = async () => { if (catalog && Date.now() - catT < FRESH) return catalog; catT = Date.now(); return (catalog = await (await fetch("data/catalog.json", {cache: "no-cache"})).json()); };
  const getCourse = async slug => {
    if (courses[slug] && Date.now() - (courseT[slug] || 0) < FRESH) return courses[slug];
    courseT[slug] = Date.now();
    const r = await fetch(`api/course.php?slug=${encodeURIComponent(slug)}`, {cache: "no-store", credentials: "same-origin"});
    if (!r.ok) { const e = new Error("curso"); e.status = r.status; throw e; }
    return (courses[slug] = (await r.json()).course);
  };
  const forgetCourses = () => Object.keys(courses).forEach(k => delete courses[k]);
  const allCourses = async () => { const c = await getCatalog(); return Promise.all(c.order.filter(s => c.courses.some(x => x.slug === s && (!x.draft || session.staff()))).map(getCourse)); };

  const hours = c => { const m = (c.lab_minutes ?? c.lessons.reduce((a, l) => a + (l.lab?.minutes || 0), 0)) + c.lessons.length * 6; return (Math.round(m / 30) / 2).toLocaleString("es-UY") + " h"; };
  const toast = msg => { const t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); t.textContent = msg; document.body.append(t); setTimeout(() => t.remove(), 2000); };
  const rich = s => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>");
  const lid = l => String(l.id ?? l.n);
  const arcLessons = (c, a) => a.lessons.map(r => c.lessons.find(l => lid(l) === String(r)) || c.lessons.find(l => l.n === +r)).filter(Boolean);
  const pct = (a, b) => b ? Math.round(a / b * 100) : 0;

  function cover(c, big = false) {
    const m = META[c.slug] || {glyph: "doc"};
    const art = c.logo ? `<span class="logo-tile"><img src="${esc(c.logo)}" alt="" loading="lazy"></span>` : `<span class="glyph">${icon(m.glyph)}</span>`;
    return `<div class="cover${big ? " big" : ""}${c.logo ? " has-logo" : ""}" aria-hidden="true">${shape()}<span class="ven">${esc(c.vendor)}</span>${art}<span class="ttl">${esc(shortTitle(c.title))}</span></div>`;
  }
  const shortTitle = t => t.split(":")[0].replace(/ para .*/i, "");

  function courseCard(c) {
    const done = store.courseDone(c.slug, c.lessons), started = store.started(c.slug, c.lessons);
    return `<a class="ccard" href="#/curso/${c.slug}" data-cat="${META[c.slug]?.cat || ""}">
      ${cover(c)}
      <div class="cb">
        <h3>${esc(c.title)}</h3>
        <span class="by">Equipo técnico IES</span>
        ${started ? `<div class="prog"><div class="bar"><i style="width:${pct(done, c.lessons.length)}%"></i></div><span>${done === c.lessons.length ? "Curso completo, con constancia disponible" : `${done} de ${c.lessons.length} lecciones completas`}</span></div>`
          : `<span class="by" style="color:var(--ink-2)">${esc(c.tagline || "")}</span>`}
        <div class="meta"><span class="pill info">${esc(c.level || "Inicial a intermedio")}</span><span class="pill plain">${c.lessons.length} lecciones</span><span class="pill plain">${hours(c)}</span></div>
      </div></a>`;
  }

  /* ---------- inicio ---------- */
  async function viewHome() {
    const list = await allCourses();
    const totLessons = list.reduce((a, c) => a + c.lessons.length, 0);
    const totLab = list.reduce((a, c) => a + c.lessons.reduce((x, l) => x + (l.lab.minutes || 0), 0), 0);
    const totSrc = list.reduce((a, c) => a + (c.sources_count || 0), 0);
    const going = list.filter(c => store.started(c.slug, c.lessons) && store.courseDone(c.slug, c.lessons) < c.lessons.length);
    const bySlug = Object.fromEntries(list.map(c => [c.slug, c]));
    main.innerHTML = `
      <section class="hero"><div class="wrap hero-in">
        <div>
          <span class="badge"><span class="p"></span>Formación técnica IES</span>
          <h1>Lo que hay que saber antes de llegar a la obra.</h1>
          <p class="lead">Cursos para técnicos de redes, telefonía IP, seguridad electrónica y servidores. Cada lección es una idea, un laboratorio con los comandos exactos y un quiz con casos reales.</p>
          <form class="hero-search" id="heroSearch" role="search"><label class="sr" for="hq">Buscar</label><input id="hq" type="search" placeholder="Probá con VLAN, DTMF, backup, RTSP…"><button class="btn">Buscar</button></form>
          ${session.user ? "" : `<div class="row hero-cta"><a class="btn" href="#/registro">Crear cuenta gratis</a><a class="btn ghost" href="#/ingresar">Ingresar</a><span>Las lecciones y los exámenes son para técnicos registrados.</span></div>`}
          <div class="hero-tags">${["VLAN", "Failover", "DTMF", "RTSP", "Backup", "RDP", "SSH"].map(t => `<a href="#/buscar/${encodeURIComponent(t)}">${t}</a>`).join("")}</div>
        </div>
        <div class="hero-art">
          <div class="forma"><img src="assets/hero.jpg" alt="" width="1400" height="788"></div>
          <div class="hero-tag"><div><b>${list.length}</b><span>cursos</span></div><div><b>${totLessons}</b><span>lecciones</span></div><div><b>${Math.round(totLab / 60)} h</b><span>de laboratorio</span></div></div>
        </div>
      </div></section>

      ${going.length ? `<section class="wrap sec"><div class="sec-h"><div><span class="k">Tu avance</span><h2>Seguí donde lo dejaste</h2></div><a class="btn ghost" href="#/aprendizaje">Ver mi aprendizaje</a></div>
        <div class="continue">${going.map(c => { const d = store.courseDone(c.slug, c.lessons); const nx = c.lessons.find(l => !store.get(c.slug, lid(l)).done) || c.lessons[0];
          return `<a class="card cont" href="#/curso/${c.slug}/${nx.n}">${cover(c)}<div><h3>${esc(c.title)}</h3><p>Lección ${nx.n}: ${esc(nx.handle)}</p><div class="bar"><i style="width:${pct(d, c.lessons.length)}%"></i></div></div></a>`; }).join("")}</div></section>` : ""}

      <section class="wrap sec" id="catalogo">
        <div class="sec-h"><div><span class="k">Catálogo</span><h2>Todos los cursos</h2><p>${list.length} cursos, ${totLessons} lecciones y ${totSrc} fuentes leídas, entre documentación oficial de cada fabricante y técnicos que escriben sobre su trabajo.</p></div></div>
        <div class="chips" role="group" aria-label="Filtrar por área">${CATS.map(([k, t], i) => `<button class="chip" data-cat="${k}" aria-pressed="${i === 0}">${t}</button>`).join("")}</div>
        <div class="grid" id="grid" style="margin-top:20px">${list.map(courseCard).join("")}</div>
      </section>

      <section class="wrap sec">
        <div class="sec-h"><div><span class="k">Rutas</span><h2>Por dónde empezar según tu trabajo</h2><p>Tres recorridos que juntan los cursos que se usan en la misma obra.</p></div></div>
        <div class="paths">${PATHS.map(p => `
          <div class="card path${p.feat ? " feat" : ""}">
            <span class="k">${p.courses.length} cursos</span><h3>${p.title}</h3><p>${p.text}</p>
            <ol>${p.courses.filter(s => bySlug[s]).map(s => `<li><a href="#/curso/${s}"><span>${esc(shortTitle(bySlug[s].title))}</span><small>${pct(store.courseDone(s, bySlug[s].lessons), 12)}%</small></a></li>`).join("")}</ol>
            <div class="foot2"><span>${p.courses.reduce((a, s) => a + (bySlug[s]?.lessons.length || 0), 0)} lecciones</span><span>${p.courses.filter(s => bySlug[s]).reduce((a, s) => a + parseFloat(hours(bySlug[s]).replace(",", ".")), 0).toLocaleString("es-UY")} h</span></div>
          </div>`).join("")}</div>
      </section>

      <section class="wrap sec">
        <div class="sec-h"><div><span class="k">Cómo funciona</span><h2>Cada lección, en cinco pasos</h2></div></div>
        <div class="steps">
          <div class="st"><span class="dot">01</span><h3>Leé la idea</h3><p>Tres líneas, qué mejora en la obra y cuántas fuentes lo respaldan.</p></div>
          <div class="st"><span class="dot">02</span><h3>Hacé el laboratorio</h3><p>Pasos con comandos y menús exactos, para un equipo de prueba.</p></div>
          <div class="st"><span class="dot">03</span><h3>Rendí el examen</h3><p>Tres casos de obra con la explicación de cada respuesta.</p></div>
          <div class="st"><span class="dot">04</span><h3>Guardá la regla</h3><p>Una frase por lección que va a tu manual de bolsillo.</p></div>
          <div class="st"><span class="dot">05</span><h3>Obtené la constancia</h3><p>Al completar todas las lecciones de un curso.</p></div>
        </div>
      </section>`;
    $$(".chip").forEach(b => b.addEventListener("click", () => {
      $$(".chip").forEach(x => x.setAttribute("aria-pressed", x === b));
      $$("#grid .ccard").forEach(card => { card.hidden = !(b.dataset.cat === "todos" || card.dataset.cat === b.dataset.cat); });
    }));
    $("#heroSearch").addEventListener("submit", e => { e.preventDefault(); const v = $("#hq").value.trim(); if (v) location.hash = `#/buscar/${encodeURIComponent(v)}`; });
    document.title = "IES Training";
  }

  /* ---------- curso ---------- */
  async function viewCourse(slug) {
    const c = await getCourse(slug);
    const done = store.courseDone(slug, c.lessons), started = store.started(slug, c.lessons);
    const next = c.lessons.find(l => !store.get(slug, lid(l)).done) || c.lessons[0];
    const labMin = c.lessons.reduce((a, l) => a + (l.lab.minutes || 0), 0);
    const quizN = c.lessons.reduce((a, l) => a + (l.quiz_n ?? (l.quiz || []).length), 0);
    const arcs = (c.arcs || [{title: "Lecciones", why: "", lessons: c.lessons.map(l => l.n)}]).map((a, i) => {
      const ls = arcLessons(c, a);
      return `<details class="acc" ${i === 0 || ls.some(l => l.n === next.n) ? "open" : ""}>
        <summary>${icon("chev", "i chev")}<div><span class="k">Módulo ${i + 1}</span><h3>${esc(a.title)}</h3></div><span class="am">${ls.length} lecciones<br>${ls.reduce((x, l) => x + (l.lab.minutes || 0), 0)} min de laboratorio</span></summary>
        ${a.why ? `<p class="why">${esc(a.why)}</p>` : ""}
        ${(a.objetivos || []).length ? `<ul class="mod-obj">${a.objetivos.map(o => `<li>${icon("check")}<span>${esc(o)}</span></li>`).join("")}</ul>` : ""}
        <ol class="lrows">${ls.map(l => { const off = !c.locked && !isOpen(c, l); return `<li class="lrow${c.locked || off ? " locked" : ""}"><a href="#/curso/${slug}/${l.n}" ${off ? 'title="Se habilita al completar la lección anterior"' : ""}>
          ${c.locked || off ? `<span class="state lock">${icon("lock")}</span>` : `<span class="state" data-s="${store.level(slug, lid(l))}">${store.level(slug, lid(l)) === 2 ? icon("check") : ""}</span>`}
          <span><span class="lt"><small>${String(l.n).padStart(2, "0")}</small>${esc(l.handle)}</span>${l.summary || (l.objetivos || [])[0] ? `<span class="ls">${esc(l.summary || l.objetivos[0])}</span>` : ""}</span>
          <span class="ld">${l.lab.minutes ? `${l.lab.minutes} min` : ""}</span></a></li>`; }).join("")}</ol>
      </details>`;
    }).join("");
    const allDone = done === c.lessons.length;
    main.innerHTML = `
      <section class="c-band">${shape("rgba(23,168,212,.55)", 6)}<div class="wrap c-band-in"><div>
        <nav class="crumbs" aria-label="Ruta"><a href="#/">Explorar</a><span>/</span><a href="#/#catalogo">${esc(CATS.find(x => x[0] === META[slug]?.cat)?.[1] || "Cursos")}</a><span>/</span><span>${esc(c.vendor)}</span></nav>
        <div class="c-title">${c.logo ? `<span class="logo-tile sm"><img src="${esc(c.logo)}" alt="${esc(c.vendor)}"></span>` : ""}<h1>${esc(c.title)}</h1></div>
        <p class="tag">${esc(c.tagline)}</p>
        <div class="c-facts">
          <span class="pill info">${esc(c.level || "Inicial a intermedio")}</span>
          <span>${icon("book")}${c.lessons.length} lecciones</span>
          <span>${icon("clock")}${hours(c)} en total</span>
          <span>${icon("doc")}${c.sources_count || "?"} fuentes leídas</span>
          <span>${icon("pin")}Español rioplatense</span>
        </div>
        <p class="by">Creado por <b>Equipo técnico IES</b>. Actualizado en octubre de 2026.</p>
        ${session.staff() ? `<a class="btn light sm edit-btn" href="#/curso/${slug}/editar">${icon("edit")}Editar este curso</a>` : ""}
      </div><div></div></div></section>
      <div class="wrap c-layout">
        <div>
          <section class="card learn"><h2>Qué vas a aprender</h2><ul>${(c.outcomes || []).map(o => `<li>${icon("check")}<span>${esc(o)}</span></li>`).join("")}</ul></section>
          <section class="block"><h2>Tu ruta de aprendizaje</h2>
            ${c.objetivo || c.recorrido ? `<div class="card route-box">${c.objetivo ? `<p class="c-goal"><span class="k">Al terminar el curso</span>${esc(c.objetivo)}</p>` : ""}${c.recorrido ? `<p>${esc(c.recorrido)}</p>` : ""}</div>` : ""}
            <p class="sub">${(c.arcs || []).length} módulos en orden, ${c.lessons.length} lecciones, ${labMin} min de laboratorio y ${quizN} preguntas de examen.${c.secuencial !== false ? " Cada lección se habilita al completar la anterior." : ""}</p>${arcs}</section>
          ${(c.prerequisites || []).length ? `<section class="block"><h2>Requisitos</h2><ul class="reqs">${c.prerequisites.map(x => `<li>${esc(x)}</li>`).join("")}</ul></section>` : ""}
          <section class="block desc"><h2>Descripción</h2><p>${esc(c.description)}</p>${c.audience ? `<p><b>Para quién es:</b> ${esc(c.audience)}</p>` : ""}${c.version_note ? `<p><b>Versiones:</b> ${esc(c.version_note)}</p>` : ""}</section>
          ${!c.locked && (c.splits || []).length ? `<section class="block"><h2>Donde las fuentes no coinciden</h2><p class="sub">Decisiones que conviene tomar con criterio propio: gente que sabe opina distinto.</p>
            ${c.splits.map(s => `<div class="card split"><span class="pill warn">Decisión de criterio</span><h3>${s.topic}</h3><p>${s.sides}</p>${s.decide ? `<p><b>Cómo decidir:</b> ${s.decide}</p>` : ""}</div>`).join("")}</section>` : ""}
        </div>
        <aside class="card buy" aria-label="Tu curso">
          ${cover(c, true)}
          <div class="buy-b">
            ${c.locked ? `<p class="lock-t">${icon("lock")}Las lecciones y los exámenes son para técnicos registrados. Es gratis.</p><a class="btn wide" href="#/registro">Crear cuenta gratis</a><a class="btn ghost wide" href="#/ingresar">Ya tengo cuenta</a>` : ""}
            ${c.locked ? "" : started ? `<div class="pct"><span>Tu avance</span><b>${pct(done, c.lessons.length)}%</b></div><div class="bar"><i style="width:${pct(done, c.lessons.length)}%"></i></div>` : ""}
            ${c.locked ? "" : allDone ? `<a class="btn wide" href="#/constancia/${slug}">${icon("award")}Ver mi constancia</a><a class="btn ghost wide" href="#/curso/${slug}/1">Repasar el curso</a>`
              : `<a class="btn wide" href="#/curso/${slug}/${next.n}">${started ? `Seguir con la lección ${next.n}` : "Empezar el curso"}</a>`}
            <ul class="inc">
              <li>${icon("book")}${c.lessons.length} lecciones de lectura corta</li>
              <li>${icon("flask")}${c.lessons.length} laboratorios con comandos</li>
              <li>${icon("quiz")}${quizN} preguntas de examen con explicación</li>
              <li>${icon("split")}${c.splits_count ?? (c.splits || []).length} decisiones de criterio</li>
              <li>${icon("award")}Constancia de finalización</li>
            </ul>
            ${c.locked ? "" : `<a class="btn ghost wide" href="#/curso/${slug}/pdf">${icon("download")}Curso completo en PDF</a>`}
          </div>
        </aside>
      </div>`;
    document.title = `${c.title} · IES Training`;
  }

  /* ---------- lección ---------- */
  async function viewLesson(slug, n, tab = "resumen") {
    const c = await getCourse(slug);
    const i = c.lessons.findIndex(l => l.n === n);
    if (i < 0) return viewCourse(slug);
    if (c.locked) return viewLessonLocked(c, c.lessons[i]);
    if (!isOpen(c, c.lessons[i])) return viewLessonGate(c, c.lessons[i]);
    const l = c.lessons[i], prev = c.lessons[i - 1], next = c.lessons[i + 1];
    const key = lid(l);
    if (!store.get(slug, key).seen) store.set(slug, key, {seen: true});
    const p = store.get(slug, key);
    const arcIdx = (c.arcs || []).findIndex(a => arcLessons(c, a).includes(l));
    const done = store.courseDone(slug, c.lessons), total = c.lessons.length;
    const C = 2 * Math.PI * 14;
    const side = (c.arcs || [{title: "Lecciones", lessons: c.lessons.map(x => x.n)}]).map((a, ai) => `
      <details class="acc" ${ai === arcIdx || arcIdx < 0 ? "open" : ""}><summary>${icon("chev", "i chev")}<div><span class="k">Módulo ${ai + 1}</span><h3>${esc(a.title)}</h3></div></summary>
      <ul class="side-list">${arcLessons(c, a).map(x => `
        <li class="${x.n === n ? "cur" : ""}"><button class="ck" role="checkbox" aria-checked="${!!store.get(slug, lid(x)).done}" aria-label="Marcar la lección ${x.n} como completa" data-k="${esc(lid(x))}"><i>${icon("check")}</i></button>
        <a href="#/curso/${slug}/${x.n}" ${x.n === n ? 'aria-current="page"' : ""}>${x.n}. ${esc(x.handle)}<small>${x.lab.minutes ? `${x.lab.minutes} min de laboratorio` : ""}</small></a></li>`).join("")}</ul></details>`).join("");
    const quiz = (l.quiz || []).map((q, k) => `
      <div class="card q" data-q="${k}"><span class="k">Pregunta ${k + 1} de ${l.quiz.length}</span><fieldset><legend>${esc(q.q)}</legend>
        ${q.options.map((o, j) => `<button class="opt" data-j="${j}"><b>${"ABCD"[j] || j + 1}</b><span>${esc(o)}</span></button>`).join("")}
        <div class="qwhy" hidden></div></fieldset></div>`).join("");
    const lines = l.script.map(x => `<div class="line" data-s="${x.s}"><span class="av" aria-hidden="true">${x.s === "A" ? "L" : "M"}</span><p class="bub"><b>${x.s === "A" ? "Lucía" : "Martín"}</b>${esc(x.t)}</p></div>`).join("");
    const tick = `<span class="tick">${icon("check")}</span>`;
    const hasTheory = !!(l.theory || (l.concepts || []).length);
    const tabs = [["resumen", "Resumen", ""], ...(hasTheory ? [["teoria", "Teoría", ""]] : []), ["laboratorio", "Laboratorio", p.lab ? tick : ""], ["quiz", "Examen", p.quiz && p.quiz.done ? tick : ""], ["charla", "La charla", ""], ["fuentes", "Fuentes", ""]];
    if (!tabs.some(t => t[0] === tab)) tab = "resumen";
    main.innerHTML = `
      <div class="player-top"><div class="wrap player-top-in">
        <a class="back" href="#/curso/${slug}">${icon("back")}<span>${esc(c.title)}</span></a>
        <div class="prog"><span class="t">${done} de ${total} completas</span><svg class="ring" viewBox="0 0 34 34" aria-hidden="true"><circle class="bg" cx="17" cy="17" r="14"/><circle class="fg" cx="17" cy="17" r="14" stroke-dasharray="${C}" stroke-dashoffset="${C * (1 - done / total)}"/></svg></div>
      </div></div>
      <div class="wrap l-layout">
        <div>
          <section class="card l-head">
            <div class="row"><span class="pill info">Lección ${n} de ${total}</span>${(() => { const mo = modOf(c, l); return mo ? `<span class="pill plain">Módulo ${mo.ai + 1}: ${esc(mo.a.title)} · ${mo.k} de ${mo.m}</span>` : ""; })()}${p.done ? '<span class="pill ok">Completa</span>' : ""}</div>
            <h1>${esc(l.handle)}</h1>
            ${l.summary ? `<p>${esc(l.summary)}</p>` : ""}
            <div class="row l-acts"><a class="btn ghost sm" href="#/curso/${slug}/${n}/pdf">${icon("download")}PDF de la lección</a>${session.staff() ? `<a class="btn ghost sm" href="#/curso/${slug}/${n}/editar">${icon("edit")}Editar esta lección</a>` : ""}</div>
          </section>
          <div class="tabs" role="tablist" aria-label="Partes de la lección">${tabs.map(([k, t, ex]) => `<button class="tab" role="tab" id="t-${k}" aria-controls="p-${k}" aria-selected="${k === tab}" tabindex="${k === tab ? 0 : -1}" data-tab="${k}">${t}${ex}</button>`).join("")}</div>

          <section class="panel" role="tabpanel" id="p-resumen" aria-labelledby="t-resumen" ${tab !== "resumen" ? "hidden" : ""}>
            ${l.fig ? `<figure class="l-fig"><button class="zoom" aria-label="Ampliar la ilustración"><img src="${esc(l.fig.src)}" alt="${esc(l.fig.alt || "")}" width="1200" height="675"></button>${l.fig.caption ? `<figcaption>${esc(l.fig.caption)}</figcaption>` : ""}</figure>` : ""}
            ${(l.objetivos || []).length || l.conecta ? `<div class="card route-box">${l.conecta ? `<p class="conecta"><span class="k">De dónde venimos</span>${esc(l.conecta)}</p>` : ""}${(l.objetivos || []).length ? `<div class="objs"><span class="k">En esta lección vas a</span><ul>${l.objetivos.map(o => `<li>${icon("check")}<span>${esc(o)}</span></li>`).join("")}</ul></div>` : ""}</div>` : ""}
            <span class="k">La idea, en tres líneas</span>
            <ul class="ideas" style="margin-top:12px">${l.idea.map((x, ii) => `<li><i></i><span>${x}${pics((l.idea_pics || [])[ii])}</span></li>`).join("")}</ul>
            ${animsHTML(l)}
            <div class="kv">
              <div class="card"><span class="k">Qué mejora en la obra</span><p>${l.impact}</p></div>
              <div class="card"><span class="k">Quién lo dice</span><p>${l.who}</p></div>
            </div>
            <div class="rule"><span class="k">Regla para tu manual</span><blockquote>${rich(l.rule)}</blockquote>
              <div class="row"><button class="btn light" id="ruleBtn" aria-pressed="${!!p.rule}">${p.rule ? "Está en tu manual" : "Guardar en mi manual"}</button><span>Tu manual reúne las reglas de todos los cursos.</span></div></div>
            <div class="l-foot"><span></span><button class="btn" data-go="${hasTheory ? "teoria" : "laboratorio"}">${hasTheory ? "Ir a la teoría" : "Ir al laboratorio"} ${icon("chev")}</button></div>
          </section>

          ${hasTheory ? `<section class="panel" role="tabpanel" id="p-teoria" aria-labelledby="t-teoria" ${tab !== "teoria" ? "hidden" : ""}>
            ${l.theory ? `<article class="card theory">${l.theory}</article>` : ""}
            ${(l.concepts || []).length ? `<section class="concepts"><div class="concepts-h"><span class="k">Para qué sirve cada cosa</span><h2>Los conceptos, con ejemplos</h2></div>
              ${l.concepts.map((k, ki) => `<article class="card concept"><h3><span class="cn">${String(ki + 1).padStart(2, "0")}</span>${esc(k.name)}</h3>
                <div class="cgrid3"><div><span class="ck-l">${icon("quiz")}Para qué se creó</span><p>${mdLite(k.para_que)}</p></div><div><span class="ck-l">${icon("flask")}Cómo se usa</span><p>${mdLite(k.como)}</p></div><div class="ex"><span class="ck-l">${icon("pin")}Ejemplo en obra</span><p>${mdLite(k.ejemplo)}</p></div></div>${pics(k.pics)}</article>`).join("")}</section>` : ""}
            <div class="l-foot"><button class="btn ghost" data-go="resumen">${icon("back")}Resumen</button><button class="btn" data-go="laboratorio">Ir al laboratorio ${icon("chev")}</button></div>
          </section>` : ""}

          <section class="panel" role="tabpanel" id="p-laboratorio" aria-labelledby="t-laboratorio" ${tab !== "laboratorio" ? "hidden" : ""}>
            <div class="card lab">
              <div class="lab-h"><h2>Laboratorio</h2><div style="display:flex;gap:6px;flex-wrap:wrap">${l.lab.energy ? `<span class="pill info">${esc(l.lab.energy)}</span>` : ""}${l.lab.minutes ? `<span class="pill plain">${l.lab.minutes} min</span>` : ""}</div></div>
              <div class="lab-body">${l.lab.html}</div>
              ${l.auto?.codigo ? autoBox(l, slug) : ""}
              <div class="lab-done"><button class="btn ${p.lab ? "done" : ""}" id="labBtn" aria-pressed="${!!p.lab}">${p.lab ? `${icon("check")}Laboratorio hecho` : "Marcar laboratorio como hecho"}</button><span>Hacelo en un equipo de prueba, no en el de un cliente.</span></div>
            </div>
            <section class="card caps" id="caps" ${editor.on() ? "" : "hidden"} aria-labelledby="h-caps">
              <div class="caps-h"><h2 id="h-caps">Capturas y videos</h2>${editor.on() ? '<span class="pill ok">Modo editor</span>' : ""}</div>
              ${editor.on() ? `<div class="drop" id="drop" tabindex="0" role="button" aria-label="Agregar medios: pegá con Control V, arrastrá un archivo o elegí uno">
                ${icon("doc")}<div><b>Pegá una captura con Ctrl+V, o arrastrá imágenes, GIF animados y videos</b><span>O <u>elegí archivos</u>. Imágenes hasta 12 MB, GIF hasta 30 MB, videos MP4 o WebM hasta 60 MB.</span>
                <form class="emb-f" id="embF"><label class="sr" for="embU">Enlace de YouTube o Vimeo</label><input id="embU" placeholder="Pegá un enlace de YouTube o Vimeo" autocomplete="off"><button class="mini">Agregar video</button><button class="mini" type="button" id="gifB">Armar GIF con capturas</button></form></div>
                <input type="file" id="capFile" accept="image/png,image/jpeg,image/webp,image/gif,video/mp4,video/webm" multiple hidden></div>` : ""}
              <div class="caps-grid" id="capsGrid"></div>
            </section>
            <div class="l-foot"><button class="btn ghost" data-go="resumen">${icon("back")}Resumen</button><button class="btn" data-go="quiz">Ir al examen ${icon("chev")}</button></div>
          </section>

          <section class="panel" role="tabpanel" id="p-quiz" aria-labelledby="t-quiz" ${tab !== "quiz" ? "hidden" : ""}>
            <div class="quiz">${quiz}<div class="card qscore" id="qScore" hidden></div></div>
          </section>

          <section class="panel" role="tabpanel" id="p-charla" aria-labelledby="t-charla" ${tab !== "charla" ? "hidden" : ""}>
            <p class="note" style="margin:0 0 16px">Lucía y Martín, dos técnicos, cuentan la idea con un caso real. Es opcional.</p>
            <div class="chat">${lines}</div>
          </section>

          <section class="panel" role="tabpanel" id="p-fuentes" aria-labelledby="t-fuentes" ${tab !== "fuentes" ? "hidden" : ""}>
            <ul class="srcs">${l.sources.map(s => `<li><a class="card" href="${esc(s.url)}" target="_blank" rel="noopener"><span class="ico">${icon("link")}</span><span><b>${esc(s.label)}</b><small>${esc(s.url.replace(/^https?:\/\//, ""))}</small></span></a></li>`).join("")}</ul>
            <p class="note">Las páginas se leyeron en octubre de 2026. Las cifras de cada fuente son afirmaciones de esa fuente.</p>
          </section>

          <div class="l-foot">
            ${prev ? `<a class="btn ghost" href="#/curso/${slug}/${prev.n}">${icon("back")}Lección ${prev.n}</a>` : "<span></span>"}
            <div style="display:flex;gap:10px;flex-wrap:wrap">
              <button class="btn ${p.done ? "done" : "ghost"}" id="doneBtn" aria-pressed="${!!p.done}">${p.done ? `${icon("check")}Completa` : "Marcar como completa"}</button>
              ${next ? (seqOn(c) && !p.done ? `<span class="btn ghost is-off" title="Se habilita al completar esta lección">${icon("lock")}Siguiente lección</span>` : `<a class="btn" href="#/curso/${slug}/${next.n}">Siguiente lección ${icon("chev")}</a>`) : `<a class="btn" href="#/curso/${slug}">Terminar el curso ${icon("chev")}</a>`}
            </div>
          </div>
          ${next ? `<section class="card next-card"><span class="k">Qué sigue · Lección ${next.n}</span><h3>${esc(next.handle)}</h3>${l.sigue ? `<p>${esc(l.sigue)}</p>` : ""}
            ${seqOn(c) && !p.done ? `<p class="note">${icon("lock")} Se habilita cuando completes esta lección: hacé el laboratorio y aprobá el examen, o marcala como completa.</p>` : `<a class="btn" href="#/curso/${slug}/${next.n}">Ir a la lección ${next.n} ${icon("chev")}</a>`}</section>` : `<section class="card next-card"><span class="k">Final del curso</span><h3>Llegaste a la última lección</h3>${l.sigue ? `<p>${esc(l.sigue)}</p>` : ""}<a class="btn" href="#/curso/${slug}">Ver la ruta y la constancia</a></section>`}
        </div>
        <aside class="card side" aria-label="Contenido del curso">
          <div class="side-h"><h2>Contenido del curso</h2><div class="bar"><i style="width:${pct(done, total)}%"></i></div><p>${done} de ${total} lecciones completas</p></div>
          ${side}
        </aside>
      </div>`;
    document.title = `${l.handle} · ${c.title} · IES Training`;

    const show = k => {
      $$(".tab").forEach(t => { const on = t.dataset.tab === k; t.setAttribute("aria-selected", on); t.tabIndex = on ? 0 : -1; });
      $$(".panel").forEach(pn => pn.hidden = pn.id !== `p-${k}`);
      const top = $(".tabs").getBoundingClientRect().top + scrollY - 130;
      if (scrollY > top) scrollTo({top, behavior: "smooth"});
    };
    $$(".tab").forEach(t => t.addEventListener("click", () => show(t.dataset.tab)));
    $(".tabs").addEventListener("keydown", e => {
      if (!["ArrowRight", "ArrowLeft"].includes(e.key)) return;
      const ts = $$(".tab"), cur = ts.findIndex(t => t.getAttribute("aria-selected") === "true");
      const nx = ts[(cur + (e.key === "ArrowRight" ? 1 : -1) + ts.length) % ts.length]; nx.focus(); show(nx.dataset.tab);
    });
    $$("[data-go]").forEach(b => b.addEventListener("click", () => show(b.dataset.go)));

    $$(".lab-body pre").forEach(pre => {
      const code = pre.querySelector("code"); const lang = (code?.className.match(/language-(\w+)/) || [])[1];
      if (lang) pre.dataset.lang = lang;
      const b = document.createElement("button"); b.className = "copy"; b.textContent = "Copiar";
      b.addEventListener("click", async () => {
        try { await navigator.clipboard.writeText(code ? code.innerText : pre.innerText); b.textContent = "Copiado"; }
        catch { const r = document.createRange(); r.selectNodeContents(code || pre); const s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = "Seleccionado"; }
        setTimeout(() => b.textContent = "Copiar", 1500);
      });
      pre.append(b);
    });

    const refresh = () => viewLesson(slug, n, $(".tab[aria-selected=true]")?.dataset.tab || "resumen").then(() => {});
    const keepScroll = fn => { const y = scrollY; fn(); refresh().then(() => scrollTo(0, y)); };
    $("#labBtn").addEventListener("click", () => keepScroll(() => { const on = !store.get(slug, key).lab; store.set(slug, key, {lab: on}); if (on) toast(store.get(slug, key).done ? "Lección completa" : "Laboratorio hecho"); }));
    $("#ruleBtn").addEventListener("click", e => {
      const on = !store.get(slug, key).rule; store.set(slug, key, {rule: on});
      e.currentTarget.textContent = on ? "Está en tu manual" : "Guardar en mi manual"; e.currentTarget.setAttribute("aria-pressed", on);
      if (on) toast("Regla guardada en tu manual");
    });
    $("#doneBtn").addEventListener("click", () => keepScroll(() => { const on = !store.get(slug, key).done; store.set(slug, key, {done: on}); if (on) toast("Lección completa"); }));
    $$(".side-list .ck").forEach(b => b.addEventListener("click", () => keepScroll(() => { const k = b.dataset.k; store.set(slug, k, {done: !store.get(slug, k).done}); })));

    capturas.mount(slug, key, n);
    ["#p-resumen", "#p-teoria", "#p-laboratorio .lab-body"].forEach(sel => glossify($(sel)));
    wireAuto(l, slug);
    // ampliar ilustraciones e imágenes del laboratorio
    ["#p-resumen .ideas", "#p-teoria", "#p-laboratorio .lab-body"].forEach(sel => figurize($(sel)));
    const zoomPics = [...$$(".l-fig img"), ...$$(".anims img"), ...$$(".pics img"), ...$$(".ideas img"), ...$$(".lab-body img"), ...$$(".theory img")];
    zoomPics.forEach((im, ix) => { im.style.cursor = "zoom-in"; (im.closest(".zoom") || im).addEventListener("click", () => lightbox(zoomPics.map(x => ({url: x.getAttribute("src"), texto: x.closest("figure")?.querySelector("figcaption")?.textContent || x.alt, tipo: /\.gif$/i.test(x.src) ? "gif" : "imagen"})), ix)); });

    // quiz
    const paintQ = (k, j) => {
      const q = l.quiz[k], box = $(`.q[data-q="${k}"]`);
      $$(".opt", box).forEach(b => { b.disabled = true; const jj = +b.dataset.j; if (jj === q.answer) b.classList.add("right"); else if (jj === j) b.classList.add("wrong"); });
      const w = $(".qwhy", box); w.hidden = false; w.innerHTML = `<b>${j === q.answer ? "Correcto." : "No es esa."}</b> ${mdLite(q.why)}`; glossify(w);
    };
    const score = () => {
      const a = (store.get(slug, key).quiz || {}).a || [];
      const answered = a.filter(x => x != null).length;
      const box = $("#qScore");
      if (!l.quiz.length || answered < l.quiz.length) { box.hidden = true; return; }
      const ok = a.filter((x, k) => x === l.quiz[k]?.answer).length;
      box.hidden = false;
      box.innerHTML = `<div><span class="k">Resultado</span><br><b>Acertaste ${ok} de ${l.quiz.length}</b></div><div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn ghost" id="qRetry">Responder de nuevo</button>${next ? `<a class="btn" href="#/curso/${slug}/${next.n}">Siguiente lección</a>` : ""}</div>`;
      $("#qRetry").addEventListener("click", () => { const cur = store.get(slug, key).quiz || {}; store.set(slug, key, {quiz: {a: [], done: cur.done}}); viewLesson(slug, n, "quiz"); });
    };
    ((p.quiz && p.quiz.a) || []).forEach((j, k) => { if (j != null && l.quiz[k]) paintQ(k, j); });
    score();
    $$(".opt").forEach(b => b.addEventListener("click", () => {
      const k = +b.closest(".q").dataset.q, j = +b.dataset.j;
      const cur = store.get(slug, key).quiz || {}; const a = [...(cur.a || [])]; a[k] = j;
      const wasDone = store.get(slug, key).done;
      const doneNow = cur.done || a.filter(x => x != null).length === l.quiz.length;
      store.set(slug, key, {quiz: {a, done: doneNow}});
      paintQ(k, j); score();
      if (!wasDone && store.get(slug, key).done) { toast("Lección completa"); setTimeout(() => keepScroll(() => {}), 900); }
    }));
  }

  // animaciones del resumen: cómo se ve en la red lo que explica la lección
  const animsHTML = l => (l.anims || []).length ? `<section class="anims"><span class="k">Cómo se ve en la red</span>${l.anims.map(a => `<figure class="lab-fig"><img src="${esc(a.src)}" alt="${esc(a.alt || "")}" loading="lazy" width="1200" height="675">${a.caption ? `<figcaption>${esc(a.caption)}</figcaption>` : ""}</figure>`).join("")}</section>` : "";
  // fotos asociadas a un punto de la lección (idea, concepto)
  const pics = arr => (arr || []).length ? `<span class="pics">${arr.map(x => `<figure><img src="${esc(x.src)}" alt="${esc(x.caption || "")}" loading="lazy">${x.caption ? `<figcaption>${esc(x.caption)}</figcaption>` : ""}</figure>`).join("")}</span>` : "";

  /* ---------- texto con formato liviano (negrita, cursiva, código, enlaces, imágenes, videos) ---------- */
  const mdLite = s => {
    let h = esc(s || "");
    h = h.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, (m, a, u) => /^(capturas|ilustraciones)\/|^https:\/\//.test(u) ? `<img class="inl" src="${u}" alt="${a}" loading="lazy">` : m);
    h = h.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    h = h.replace(/\*\*([^*\n]+)\*\*/g, "<b>$1</b>").replace(/(^|[^*\w])\*([^*\n]+)\*(?!\*)/g, "$1<i>$2</i>").replace(/`([^`\n]+)`/g, "<code>$1</code>");
    h = h.replace(/^(?:https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([A-Za-z0-9_-]{11})\S*|https?:\/\/(?:www\.)?vimeo\.com\/(\d{5,12})\S*)$/gm, (m, yt, vm) =>
      `<span class="embed"><iframe src="${yt ? `https://www.youtube-nocookie.com/embed/${yt}` : `https://player.vimeo.com/video/${vm}`}" title="Video" allow="fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe></span>`);
    return h.replace(/\n/g, "<br>");
  };

  /* ---------- glosario: términos con explicación al pasar el mouse o tocar ---------- */
  let GLOS = null, GLRE = null;
  async function loadGlos() {
    if (GLOS) return GLOS;
    try { const r = await fetch("data/glosario.json", {cache: "no-cache"}); GLOS = r.ok ? await r.json() : {terms: []}; } catch { GLOS = {terms: []}; }
    GLOS.terms = GLOS.terms || [];
    GLOS.byId = Object.fromEntries(GLOS.terms.map(t => [t.id, t]));
    const items = []; GLOS.terms.forEach(t => [t.term, ...(t.aliases || [])].forEach(w => w && items.push({w, t})));
    items.sort((a, b) => b.w.length - a.w.length);
    GLOS.map = new Map(); items.forEach(({w, t}) => { const k = t.case === false ? w.toLowerCase() : w; if (!GLOS.map.has(k)) GLOS.map.set(k, t); });
    const er = x => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const cs = items.filter(i => i.t.case !== false).map(i => er(i.w)), ci = items.filter(i => i.t.case === false).map(i => er(i.w));
    const B = "(?<![\\p{L}\\p{N}_/.-])", A = "(?![\\p{L}\\p{N}_-])";
    GLRE = [cs.length && new RegExp(`${B}(?:${cs.join("|")})${A}`, "gu"), ci.length && new RegExp(`${B}(?:${ci.join("|")})${A}`, "giu")].filter(Boolean);
    return GLOS;
  }
  async function glossify(root) {
    if (!root) return; await loadGlos(); if (!GLRE.length) return;
    const once = new Set();
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {acceptNode: n => n.parentElement.closest("code,pre,a,button,.gl,h1,h2,.ie,textarea,script,style,.no-gl,legend,.opt,.k,.ck-l") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT});
    const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
    for (const node of nodes) {
      const txt = node.nodeValue; if (!txt || txt.trim().length < 2) continue;
      let i = 0, changed = false; const frag = document.createDocumentFragment();
      while (i < txt.length) {
        let best = null;
        for (const re of GLRE) { re.lastIndex = i; const m = re.exec(txt); if (m && (!best || m.index < best.index || (m.index === best.index && m[0].length > best[0].length))) best = m; }
        if (!best) break;
        const t = GLOS.map.get(best[0]) || GLOS.map.get(best[0].toLowerCase());
        const end = best.index + best[0].length;
        if (!t || (t.cat !== "RFC" && once.has(t.id))) { frag.append(txt.slice(i, end)); i = end; continue; }
        once.add(t.id); changed = true;
        frag.append(txt.slice(i, best.index));
        const sp = document.createElement("span"); sp.className = "gl"; sp.tabIndex = 0; sp.dataset.g = t.id; sp.textContent = best[0];
        sp.setAttribute("role", "button"); sp.setAttribute("aria-label", `${best[0]}, ver la explicación`);
        frag.append(sp); i = end;
      }
      if (changed) { frag.append(txt.slice(i)); node.replaceWith(frag); }
    }
  }
  const gtip = document.createElement("div"); gtip.className = "gtip"; gtip.setAttribute("role", "tooltip"); gtip.hidden = true; document.body.append(gtip);
  let gFor = null, gT = null;
  function showTip(el) {
    const t = GLOS?.byId?.[el.dataset.g]; if (!t) return;
    clearTimeout(gT); gFor = el;
    gtip.innerHTML = `<div class="gt-h"><b>${esc(t.term)}</b>${t.year ? `<span class="gy">${esc(String(t.year))}</span>` : ""}${t.cat ? `<span class="gc">${esc(t.cat)}</span>` : ""}</div><p>${esc(t.short || "")}</p>${t.long ? `<p class="gl-long">${esc(t.long)}</p>` : ""}<a href="#/glosario/${esc(t.id)}">Ver en el glosario</a>`;
    gtip.hidden = false;
    const r = el.getBoundingClientRect(), w = Math.min(380, innerWidth - 24);
    gtip.style.width = w + "px";
    const left = Math.max(12, Math.min(r.left + r.width / 2 - w / 2, innerWidth - w - 12));
    const below = r.bottom + 10 + gtip.offsetHeight < innerHeight;
    gtip.style.left = left + scrollX + "px";
    gtip.style.top = (below ? r.bottom + 10 : r.top - gtip.offsetHeight - 10) + scrollY + "px";
    gtip.dataset.pos = below ? "below" : "above";
  }
  const hideTip = (now) => { clearTimeout(gT); gT = setTimeout(() => { gtip.hidden = true; gFor = null; }, now ? 0 : 180); };
  document.addEventListener("mouseover", e => { const el = e.target.closest?.(".gl"); if (el) showTip(el); else if (e.target.closest?.(".gtip")) clearTimeout(gT); });
  document.addEventListener("mouseout", e => { if (e.target.closest?.(".gl,.gtip")) hideTip(); });
  document.addEventListener("focusin", e => { const el = e.target.closest?.(".gl"); if (el) showTip(el); });
  document.addEventListener("focusout", e => { if (e.target.closest?.(".gl")) hideTip(); });
  document.addEventListener("click", e => { const el = e.target.closest?.(".gl"); if (el) { e.preventDefault(); gFor === el && !gtip.hidden ? hideTip(true) : showTip(el); } else if (!e.target.closest?.(".gtip")) hideTip(true); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") hideTip(true); });
  window.addEventListener("hashchange", () => hideTip(true));

  async function viewGlossary(id) {
    const g = await loadGlos();
    const cats = [...new Set(g.terms.map(t => t.cat || "Otros"))].sort((a, b) => a === "RFC" ? 1 : b === "RFC" ? -1 : a.localeCompare(b, "es"));
    main.innerHTML = `<div class="wrap"><div class="page-h"><span class="badge"><span class="p"></span>Glosario</span><h1>Términos y protocolos</h1><p>${g.terms.length} términos que aparecen en los cursos, con para qué se crearon y qué resuelven. En las lecciones, los términos subrayados muestran esta explicación al pasar el mouse o tocarlos.</p>
      <label class="search-s gsearch">${icon("search")}<span class="sr">Buscar en el glosario</span><input id="gq" type="search" placeholder="Buscá un término: DTMF, VLAN, RFC 3261…"></label></div>
      <div class="gcats">${cats.map(cat => `<section class="gcat" data-cat="${esc(cat)}"><h2>${esc(cat)}</h2><dl>${g.terms.filter(t => (t.cat || "Otros") === cat).sort((a, b) => a.term.localeCompare(b.term, "es", {numeric: true})).map(t => `<div class="gitem" id="g-${esc(t.id)}" data-q="${esc((t.term + " " + (t.aliases || []).join(" ") + " " + t.short).toLowerCase())}"><dt>${esc(t.term)}${t.year ? ` <span class="gy">${esc(String(t.year))}</span>` : ""}</dt><dd><p>${esc(t.short || "")}</p>${t.long ? `<p class="gl-long">${esc(t.long)}</p>` : ""}</dd></div>`).join("")}</dl></section>`).join("")}</div></div>`;
    $("#gq").addEventListener("input", e => { const q = e.target.value.toLowerCase().trim(); $$(".gitem").forEach(x => x.hidden = q && !x.dataset.q.includes(q)); $$(".gcat").forEach(s => s.hidden = !$$(".gitem", s).some(x => !x.hidden)); });
    if (id) setTimeout(() => { const el = document.getElementById(`g-${id}`); if (el) { el.scrollIntoView({block: "center"}); el.classList.add("hl"); } }, 50);
    document.title = "Glosario · IES Training";
  }

  /* ---------- ruta lineal: módulos, objetivos, avance secuencial ---------- */
  const seqOn = c => c.secuencial !== false && !session.staff();
  const isOpen = (c, l) => { if (!seqOn(c)) return true; const i = c.lessons.indexOf(l); return i <= 0 || !!store.get(c.slug, lid(c.lessons[i - 1])).done; };
  const modOf = (c, l) => { const ai = (c.arcs || []).findIndex(a => a.lessons.map(String).includes(lid(l))); return ai < 0 ? null : {ai, a: c.arcs[ai], k: c.arcs[ai].lessons.map(String).indexOf(lid(l)) + 1, m: c.arcs[ai].lessons.length}; };
  function viewLessonGate(c, l) {
    const i = c.lessons.indexOf(l), prev = c.lessons[i - 1], mo = modOf(c, l);
    main.innerHTML = `<div class="player-top"><div class="wrap player-top-in"><a class="back" href="#/curso/${c.slug}">${icon("back")}<span>${esc(c.title)}</span></a></div></div>
      <div class="wrap"><section class="card lock-card"><span class="lock-ic">${icon("lock")}</span>
        <span class="k">${mo ? `Módulo ${mo.ai + 1} · ${esc(mo.a.title)}` : ""}</span><h1>${esc(l.handle)}</h1>
        <p>Esta lección se habilita cuando completes la anterior: <b>${esc(prev.handle)}</b>. El curso está pensado como un camino: cada lección usa lo que viste en la previa.</p>
        ${(l.objetivos || []).length ? `<div class="objs"><span class="k">En esta lección vas a</span><ul>${l.objetivos.map(o => `<li>${icon("check")}<span>${esc(o)}</span></li>`).join("")}</ul></div>` : ""}
        <div class="row"><a class="btn" href="#/curso/${c.slug}/${prev.n}">Ir a la lección ${prev.n}</a><a class="btn ghost" href="#/curso/${c.slug}">Ver la ruta del curso</a></div></section></div>`;
    document.title = `${l.handle} · ${c.title} · IES Training`;
  }

  /* imágenes del portapapeles (botón "Pegar"; pide permiso al navegador la primera vez) */
  async function clipImages() {
    if (!navigator.clipboard?.read) return [];
    try {
      const out = [];
      for (const it of await navigator.clipboard.read()) {
        const t = it.types.find(x => /^image\/(png|jpeg|webp|gif)$/.test(x)) || it.types.find(x => x.startsWith("image/"));
        if (t) { const b = await it.getType(t); out.push(new File([b], `portapapeles.${(t.split("/")[1] || "png").replace("jpeg", "jpg")}`, {type: b.type || t})); }
      }
      return out;
    } catch { return []; }
  }
  // imágenes sueltas de un texto (Markdown ![..](..) o img.inl) pasan a figura centrada, del mismo tamaño que las ilustraciones
  const GENERIC_ALT = /^(foto|imagen|captura|descripción de la (foto|imagen))$/i;
  function figurize(root) {
    if (!root) return;
    // figuras que arma pandoc con ![..](..): mismo estilo; el pie genérico ("foto") no se muestra
    $$("figure:not(.lab-fig)", root).forEach(fg => { if (fg.closest(".pics, .pics-ed, .l-fig, .gm, .caps") || !fg.querySelector("img, video")) return; fg.classList.add("lab-fig", "ufig"); const fc = fg.querySelector("figcaption"); if (fc && GENERIC_ALT.test(fc.textContent.trim())) fc.remove(); });
    $$("img", root).forEach(im => {
      if (im.closest("figure, .fx-media, .gm, .caps, .pics-ed, .ctx")) return;
      const p = im.parentElement;
      const alone = p && p.tagName === "P" && [...p.childNodes].every(n => n === im || n.nodeName === "BR" || (n.nodeType === 3 && !n.textContent.trim()));
      const fig = document.createElement("figure"); fig.className = "lab-fig ufig";
      const alt = (im.getAttribute("alt") || "").trim();
      im.classList.remove("inl");
      if (alone) p.replaceWith(fig);
      else if (p && p.tagName === "P") { p.after(fig); im.remove(); }  // imagen metida en medio de un párrafo: va debajo del párrafo
      else im.replaceWith(fig);
      fig.append(im);
      if (alt && !GENERIC_ALT.test(alt)) { const fc = document.createElement("figcaption"); fc.textContent = alt; fig.append(fc); }
    });
  }

  /* ---------- armador de GIF: pegá capturas una tras otra ---------- */
  function gifMaker() {
    return new Promise(resolve => {
      const frames = []; let width = 960, delay = 1.5, loop = true, playT = null, result = null;
      const ov = document.createElement("div"); ov.className = "gm"; ov.setAttribute("role", "dialog"); ov.setAttribute("aria-modal", "true"); ov.setAttribute("aria-label", "Armar un GIF");
      ov.innerHTML = `<div class="gm-card">
        <div class="gm-h"><div><span class="k">Armar GIF</span><h2>Pegá capturas, una por paso</h2><p>Sacá una captura (Win+Shift+S), volvé acá y pegala con <b>Ctrl+V</b>. Repetí con cada paso. También podés arrastrar o elegir archivos.</p></div><button class="gm-x" type="button" aria-label="Cerrar">×</button></div>
        <div class="gm-body"><div class="gm-left">
          <label class="gm-drop" tabindex="0">${icon("image")}<b>Pegá con Ctrl+V o arrastrá capturas</b><span>o elegí archivos</span><input type="file" accept="image/png,image/jpeg,image/webp" multiple hidden></label>
          <button class="btn ghost sm gm-paste" type="button">${icon("clip")}Pegar la captura copiada</button>
          <ol class="gm-strip"></ol></div>
          <div class="gm-right"><div class="gm-prev"><span class="note">La vista previa aparece cuando haya capturas.</span></div>
            <div class="gm-opts"><label>Ancho<select data-o="w"><option value="640">640 px</option><option value="960" selected>960 px</option><option value="1200">1200 px</option></select></label>
              <label>Cada cuadro<select data-o="d">${[0.8, 1, 1.5, 2, 3, 4].map(x => `<option value="${x}" ${x === 1.5 ? "selected" : ""}>${String(x).replace(".", ",")} s</option>`).join("")}</select></label>
              <label class="check"><input type="checkbox" data-o="l" checked> Repetir</label></div>
            <div class="gm-f"><span class="note" id="gmS"></span><button class="btn ghost" type="button" data-a="cancel">Cancelar</button><button class="btn" type="button" data-a="make" disabled>Crear GIF</button></div></div></div></div>`;
      document.body.append(ov);
      const strip = $(".gm-strip", ov), prev = $(".gm-prev", ov), st = $("#gmS", ov), make = $("[data-a=make]", ov);
      const close = f => { clearTimeout(playT); document.removeEventListener("paste", onPaste, true); document.removeEventListener("keydown", onKey); frames.forEach(x => URL.revokeObjectURL(x.url)); ov.remove(); resolve(f); };
      const paint = () => {
        strip.innerHTML = frames.map((x, i) => `<li><img src="${x.url}" alt="Cuadro ${i + 1}"><span class="gm-n">${i + 1}</span><span class="gm-t"><button type="button" class="mini" data-l="${i}" ${i === 0 ? "disabled" : ""} aria-label="Antes">←</button><button type="button" class="mini" data-r="${i}" ${i === frames.length - 1 ? "disabled" : ""} aria-label="Después">→</button><button type="button" class="mini" data-x="${i}" aria-label="Quitar">×</button></span></li>`).join("");
        $$("[data-l]", strip).forEach(b => b.onclick = () => { const i = +b.dataset.l; [frames[i - 1], frames[i]] = [frames[i], frames[i - 1]]; paint(); });
        $$("[data-r]", strip).forEach(b => b.onclick = () => { const i = +b.dataset.r; [frames[i + 1], frames[i]] = [frames[i], frames[i + 1]]; paint(); });
        $$("[data-x]", strip).forEach(b => b.onclick = () => { URL.revokeObjectURL(frames[+b.dataset.x].url); frames.splice(+b.dataset.x, 1); paint(); });
        make.disabled = frames.length < 2; result = null;
        st.textContent = frames.length ? `${frames.length} ${frames.length === 1 ? "captura" : "capturas"}${frames.length < 2 ? " · pegá al menos 2" : ""}` : "";
        play();
      };
      const play = () => { clearTimeout(playT); if (!frames.length) { prev.innerHTML = `<span class="note">La vista previa aparece cuando haya capturas.</span>`; return; } let k = 0; const step = () => { prev.innerHTML = `<img src="${frames[k % frames.length].url}" alt="Vista previa"><span class="gm-n">${(k % frames.length) + 1}/${frames.length}</span>`; k++; playT = setTimeout(step, delay * 1000); }; step(); };
      const add = async files => { for (const f of files) { if (!/^image\/(png|jpeg|webp)$/.test(f.type)) continue; try { const bmp = await createImageBitmap(f); frames.push({bmp, url: URL.createObjectURL(f)}); } catch {} } paint(); };
    const onPaste = e => { const fs = [...(e.clipboardData?.items || [])].filter(i => i.kind === "file" && /^image\//.test(i.type)).map(i => i.getAsFile()).filter(Boolean); if (!fs.length) return; e.preventDefault(); e.stopImmediatePropagation(); add(fs); };
      const onKey = e => { if (e.key === "Escape") close(null); };
      document.addEventListener("paste", onPaste, true); document.addEventListener("keydown", onKey);
      const drop = $(".gm-drop", ov), inp = $("input[type=file]", ov);
      $(".gm-paste", ov).onclick = async () => { const fs = await clipImages(); if (fs.length) add(fs); else toast("No hay ninguna imagen copiada. Sacá una captura (Win+Shift+S) y volvé a tocar."); };
      inp.onchange = () => { add([...inp.files]); inp.value = ""; };
      ["dragenter", "dragover"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add("over"); }));
      ["dragleave", "drop"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove("over"); }));
      drop.addEventListener("drop", e => add([...(e.dataTransfer?.files || [])]));
      $("[data-o=w]", ov).onchange = e => { width = +e.target.value; result = null; };
      $("[data-o=d]", ov).onchange = e => { delay = +e.target.value; result = null; play(); };
      $("[data-o=l]", ov).onchange = e => { loop = e.target.checked; result = null; };
      $(".gm-x", ov).onclick = () => close(null); $("[data-a=cancel]", ov).onclick = () => close(null);
      make.onclick = async () => {
        if (result) { close(result); return; }
        make.disabled = true;
        try {
          const {GIFEncoder, quantize, applyPalette} = await import("./vendor/gifenc.esm.js");
          const f0 = frames[0].bmp, w = width, h = Math.round(width * f0.height / f0.width);
          const cv = document.createElement("canvas"); cv.width = w; cv.height = h; const ctx = cv.getContext("2d", {willReadFrequently: true});
          const enc = GIFEncoder();
          for (let i = 0; i < frames.length; i++) {
            st.textContent = `Armando cuadro ${i + 1} de ${frames.length}…`;
            const b = frames[i].bmp, s = Math.min(w / b.width, h / b.height), dw = b.width * s, dh = b.height * s;
            ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, w, h); ctx.drawImage(b, (w - dw) / 2, (h - dh) / 2, dw, dh);
            const data = ctx.getImageData(0, 0, w, h).data, pal = quantize(data, 256), idx = applyPalette(data, pal);
            enc.writeFrame(idx, w, h, {palette: pal, delay: Math.round(delay * 1000), ...(i === 0 ? {repeat: loop ? 0 : -1} : {})});
            await new Promise(r => setTimeout(r, 0));
          }
          enc.finish();
          result = new File([enc.bytes()], `gif-${Date.now()}.gif`, {type: "image/gif"});
          const mb = result.size / 1048576;
          st.textContent = `GIF listo: ${frames.length} cuadros, ${mb < 1 ? Math.round(mb * 1024) + " KB" : mb.toFixed(1).replace(".", ",") + " MB"}${mb > 30 ? " · supera 30 MB: bajá el ancho" : ""}`;
          prev.innerHTML = `<img src="${URL.createObjectURL(result)}" alt="GIF armado">`; clearTimeout(playT);
          make.textContent = "Usar este GIF"; make.disabled = mb > 30;
        } catch (err) { st.textContent = "No se pudo armar el GIF: " + err.message; make.disabled = false; }
      };
      paint(); drop.focus();
    });
  }

  /* ---------- barra de formato para los campos de texto en modo edición ---------- */
  const fmt = document.createElement("div"); fmt.className = "fmt"; fmt.hidden = true; fmt.setAttribute("role", "toolbar"); fmt.setAttribute("aria-label", "Formato");
  fmt.innerHTML = `<button type="button" data-f="b" title="Negrita (Ctrl+B)"><b>N</b></button><button type="button" data-f="i" title="Cursiva (Ctrl+I)"><i>C</i></button><button type="button" data-f="code" title="Código">&lt;/&gt;</button><button type="button" data-f="link" title="Enlace">${icon("link")}</button>
    <span class="blk"><button type="button" data-f="h3" title="Subtítulo">T</button><button type="button" data-f="ul" title="Lista">•</button><button type="button" data-f="ol" title="Lista numerada">1.</button><button type="button" data-f="quote" title="Cita">❝</button></span>
    <button type="button" data-f="img" title="Imagen (o pegala con Ctrl+V)">${icon("image")}</button><button type="button" data-f="gif" title="Armar un GIF con capturas">GIF</button><button type="button" data-f="video" title="Video de YouTube o Vimeo">▶</button>`;
  document.body.append(fmt);
  let fmtEl = null, fmtHook = null;
  function fmtShow(el) {
    fmtEl = el; fmt.hidden = false; fmt.classList.toggle("block", el.tagName === "TEXTAREA");
    const r = el.getBoundingClientRect(); fmt.style.left = Math.max(8, Math.min(r.left, innerWidth - fmt.offsetWidth - 8)) + scrollX + "px"; fmt.style.top = Math.max(70, r.top - fmt.offsetHeight - 6) + scrollY + "px";
  }
  document.addEventListener("focusin", e => {
    const el = e.target;
    if (el.matches?.(".ie[data-md]") && el.dataset.mode !== "raw") { el.dataset.mode = "raw"; el.textContent = el.dataset.md || ""; }
    if (el.matches?.(".ie[data-md], .edit-mode textarea")) fmtShow(el);
  });
  document.addEventListener("focusout", e => {
    const el = e.target;
    if (el.matches?.(".ie[data-md]")) { el.dataset.md = ieText(el); el.dataset.mode = "view"; el.innerHTML = mdLite(el.dataset.md); }
    setTimeout(() => { if (!fmt.contains(document.activeElement) && !document.activeElement?.matches?.(".ie[data-md], .edit-mode textarea")) fmt.hidden = true; }, 120);
  });
  window.addEventListener("hashchange", () => { fmt.hidden = true; fmtEl = null; });
  fmt.addEventListener("mousedown", e => e.preventDefault());
  const wrapSel = (pre, post = pre, ph = "texto") => {
    const el = fmtEl; if (!el) return;
    if (el.tagName === "TEXTAREA") { const a = el.selectionStart, b = el.selectionEnd, t = el.value.slice(a, b) || ph; el.setRangeText(pre + t + post, a, b, "end"); el.dispatchEvent(new Event("input")); el.focus(); return; }
    el.focus(); const t = getSelection().toString() || ph; document.execCommand("insertText", false, pre + t + post);
  };
  const linePrefix = p => { const el = fmtEl; if (el?.tagName !== "TEXTAREA") return; const a = el.selectionStart, ls = el.value.lastIndexOf("\n", a - 1) + 1; el.setRangeText(p, ls, ls, "end"); el.dispatchEvent(new Event("input")); el.focus(); };
  const insertText = txt => { const el = fmtEl; if (!el) return; if (el.tagName === "TEXTAREA") { el.setRangeText(txt, el.selectionStart, el.selectionEnd, "end"); el.dispatchEvent(new Event("input")); el.focus(); } else { el.focus(); document.execCommand("insertText", false, txt); } };
  fmt.addEventListener("click", async e => {
    const b = e.target.closest("[data-f]"); if (!b || !fmtEl) return;
    const f = b.dataset.f;
    if (f === "b") wrapSel("**"); else if (f === "i") wrapSel("*"); else if (f === "code") wrapSel("`", "`", "comando");
    else if (f === "link") { const u = prompt("Dirección del enlace (https://…)"); if (u && /^https?:\/\//.test(u)) wrapSel("[", `](${u})`, "texto del enlace"); }
    else if (f === "h3") linePrefix("### "); else if (f === "ul") linePrefix("- "); else if (f === "ol") linePrefix("1. "); else if (f === "quote") linePrefix("> ");
    else if (f === "video") { const u = prompt("Pegá el enlace de YouTube o Vimeo"); if (u && /(youtube\.com|youtu\.be|vimeo\.com)\//.test(u)) insertText(`\n${u.trim()}\n`); else if (u) toast("Ese enlace no es de YouTube ni de Vimeo."); }
    else if (f === "img" || f === "gif") {
      const el = fmtEl;
      const file = f === "gif" ? await gifMaker() : await new Promise(res => { const i = document.createElement("input"); i.type = "file"; i.accept = "image/png,image/jpeg,image/webp,image/gif"; i.onchange = () => res(i.files[0] || null); i.click(); });
      if (file && fmtHook) { fmtEl = el; await fmtHook(file, el); }
    }
  });
  document.addEventListener("keydown", e => { if (!fmtEl || fmt.hidden || !(e.ctrlKey || e.metaKey)) return; if (e.key === "b") { e.preventDefault(); wrapSel("**"); } if (e.key === "i") { e.preventDefault(); wrapSel("*"); } });

  /* ---------- versión para imprimir o guardar en PDF ---------- */
  async function viewPrint(slug, n) {
    if (!session.user) { main.innerHTML = lockedPage("El PDF es para técnicos registrados", "Creá tu cuenta gratis o ingresá para descargar las lecciones."); return; }
    const c = await getCourse(slug);
    const ls = n ? c.lessons.filter(l => l.n === n) : c.lessons;
    if (!ls.length) { location.hash = `#/curso/${slug}`; return; }
    const date = new Date().toLocaleDateString("es-UY", {day: "numeric", month: "long", year: "numeric"});
    const lessonHTML = l => { const mo = modOf(c, l); return `<article class="pl">
      <header class="pl-h"><span class="k">${esc(c.title)} · ${mo ? `Módulo ${mo.ai + 1}: ${esc(mo.a.title)} · ` : ""}Lección ${l.n}</span><h2>${esc(l.handle)}</h2>${l.summary ? `<p class="sum">${esc(l.summary)}</p>` : ""}</header>
      ${(l.objetivos || []).length ? `<div class="objs"><span class="k">En esta lección vas a</span><ul>${l.objetivos.map(o => `<li>${esc(o)}</li>`).join("")}</ul></div>` : ""}
      ${l.conecta ? `<p class="conecta"><b>De dónde venimos.</b> ${esc(l.conecta)}</p>` : ""}
      ${l.fig ? `<figure class="l-fig"><img src="${esc(l.fig.src)}" alt="${esc(l.fig.alt || "")}">${l.fig.caption ? `<figcaption>${esc(l.fig.caption)}</figcaption>` : ""}</figure>` : ""}
      <h3>La idea, en tres líneas</h3><ul class="ideas-p">${(l.idea || []).map((x, i) => `<li>${x}${pics((l.idea_pics || [])[i])}</li>`).join("")}</ul>
      ${animsHTML(l)}
      <p><b>Qué mejora en la obra.</b> ${l.impact || ""}</p><p><b>Quién lo dice.</b> ${l.who || ""}</p>
      ${l.theory ? `<h3>Historia y teoría</h3><div class="theory-p">${l.theory}</div>` : ""}
      ${(l.concepts || []).length ? `<h3>Los conceptos, con ejemplos</h3>${l.concepts.map(k => `<div class="concept-p"><h4>${esc(k.name)}</h4><p><b>Para qué se creó.</b> ${mdLite(k.para_que)}</p><p><b>Cómo se usa.</b> ${mdLite(k.como)}</p><p><b>Ejemplo en obra.</b> ${mdLite(k.ejemplo)}</p>${pics(k.pics)}</div>`).join("")}` : ""}
      <h3>Laboratorio${l.lab?.minutes ? ` · ${l.lab.minutes} min` : ""}</h3><div class="lab-body">${l.lab?.html || ""}</div>
      ${l.auto?.codigo ? `<h3>Script para automatizar: ${esc(l.auto.titulo || "")}</h3>${l.auto.descripcion ? `<p>${esc(l.auto.descripcion)}</p>` : ""}${(l.auto.variables || []).length ? `<p class="note">Variables: ${l.auto.variables.map(v => `<code>${esc(v.nombre)}</code> = ${esc(v.valor)} (${esc(v.detalle || "")})`).join("; ")}</p>` : ""}<div class="lab-body"><pre><code>${esc(autoFill(l.auto, Object.fromEntries((l.auto.variables || []).map(v => [v.nombre, v.valor]))))}</code></pre></div>` : ""}
      <div class="rule-p"><span class="k">Regla para tu manual</span><p>${rich(l.rule || "")}</p></div>
      ${(l.quiz || []).length ? `<h3>Examen</h3><ol class="quiz-p">${l.quiz.map(q => `<li><p>${esc(q.q)}</p><ol type="A">${q.options.map(o => `<li>${esc(o)}</li>`).join("")}</ol></li>`).join("")}</ol>
        <details class="ans" open><summary>Respuestas</summary><ol>${l.quiz.map(q => `<li><b>${"ABCD"[q.answer]}.</b> ${mdLite(q.why || "")}</li>`).join("")}</ol></details>` : ""}
      ${l.sigue ? `<p class="conecta"><b>Qué sigue.</b> ${esc(l.sigue)}</p>` : ""}
      ${(l.sources || []).length ? `<h3>Fuentes</h3><ul class="src-p">${l.sources.map(s => `<li>${esc(s.label)}: <a href="${esc(s.url)}">${esc(s.url)}</a></li>`).join("")}</ul>` : ""}
    </article>`; };
    main.innerHTML = `<div class="print-bar no-print"><div class="wrap row"><a class="btn ghost sm" href="#/curso/${slug}${n ? "/" + n : ""}">${icon("back")}Volver</a><span class="note">${n ? "Lección" : "Curso completo"} listo para imprimir. En la ventana de impresión elegí <b>Guardar como PDF</b>.</span><button class="btn sm" id="doPrint">${icon("download")}Imprimir o guardar PDF</button></div></div>
      <div class="print-doc">
        <section class="pd-cover"><img src="assets/ies-escudo-claro.svg" alt="IES" width="70"><span class="k">IES Training · Formación técnica</span><h1>${esc(n ? ls[0].handle : c.title)}</h1><p class="tag">${esc(n ? `${c.title} · Lección ${n}` : c.tagline || "")}</p>
          ${!n && c.objetivo ? `<p><b>Objetivo del curso.</b> ${esc(c.objetivo)}</p>` : ""}${!n && c.recorrido ? `<p>${esc(c.recorrido)}</p>` : ""}
          ${!n ? `<ol class="toc">${(c.arcs || []).map((a, i) => `<li><b>Módulo ${i + 1}. ${esc(a.title)}</b><ol>${arcLessons(c, a).map(l => `<li>Lección ${l.n}. ${esc(l.handle)}</li>`).join("")}</ol></li>`).join("")}</ol>` : ""}
          <p class="pd-meta">${esc(session.user.name)} · ${date} · entrenamientos.ies.com.uy</p></section>
        ${ls.map(lessonHTML).join("")}
        <section class="pl" id="pdGlos" hidden><h2>Glosario</h2><dl></dl></section>
      </div>`;
    document.title = `${n ? ls[0].handle + " · " : ""}${c.title} · PDF · IES Training`;
    figurize($(".print-doc"));
    $("#doPrint").onclick = () => print();
    const doc = $(".print-doc"); await glossify(doc);
    const used = [...new Set($$(".gl", doc).map(x => x.dataset.g))].map(id => GLOS.byId[id]).filter(Boolean).sort((a, b) => a.term.localeCompare(b.term, "es", {numeric: true}));
    if (used.length) { const box = $("#pdGlos"); box.hidden = false; $("dl", box).innerHTML = used.map(t => `<dt>${esc(t.term)}</dt><dd>${esc(t.short || "")}${t.long ? " " + esc(t.long) : ""}</dd>`).join(""); }
  }

  /* ---------- script para automatizar lo aprendido ---------- */
  const autoFill = (a, vals) => (a.codigo || "").replace(/\{\{([A-Z0-9_]+)\}\}/g, (m, k) => vals[k] ?? m);
  /* cada curso pega su script en otra terminal: extensión, resaltado, fin de línea y consejo */
  const AUTO_KIND = {
    routeros: {ext: "rsc", lang: "routeros", crlf: true, nota: "Pegalo en New Terminal de WinBox o por SSH. Probalo antes en un equipo de banco y en Safe Mode (Ctrl+X)."},
    bash: {ext: "sh", lang: "bash", crlf: false, nota: "Pegalo en la terminal del equipo (por SSH, como root o con sudo). Probalo antes en un equipo de prueba."},
    esxi: {ext: "sh", lang: "bash", crlf: false, nota: "Pegalo en la shell del host ESXi por SSH (habilitá SSH solo mientras lo usás). Probalo antes en un host de laboratorio."},
    powershell: {ext: "ps1", lang: "powershell", crlf: true, nota: "Pegalo en PowerShell abierto como administrador. Probalo antes en un equipo de prueba."},
  };
  const autoKind = (l, slug) => AUTO_KIND[l.auto?.lang] || AUTO_KIND[{linux: "bash", proxmox: "bash", vmware: "esxi", windows: "powershell"}[slug]] || AUTO_KIND.routeros;
  function autoBox(l, slug) {
    const a = l.auto, vars = a.variables || [], K = autoKind(l, slug);
    return `<section class="auto" data-auto>
      <div class="auto-h"><span class="auto-ic">${icon("terminal")}</span><div><span class="k">Script para automatizar lo aprendido</span><h3>${esc(a.titulo || "Script de la lección")}</h3>${a.descripcion ? `<p>${esc(a.descripcion)}</p>` : ""}</div></div>
      ${vars.length ? `<div class="auto-vars"><span class="k">Completá tus datos antes de copiar</span><div class="av-grid">${vars.map(v => `<label><span>${esc(v.detalle || v.nombre)}</span><input data-v="${esc(v.nombre)}" value="${esc(v.valor || "")}" spellcheck="false" autocomplete="off"></label>`).join("")}</div></div>` : ""}
      <pre class="auto-code" data-lang="${K.lang}"><code class="language-${K.lang}"></code></pre>
      <div class="row auto-act"><button class="btn" type="button" data-copy>${icon("doc")}Copiar script</button><button class="btn ghost" type="button" data-dl>${icon("download")}Descargar .${K.ext}</button><span class="note">${K.nota}</span></div>
      ${(a.notas || []).length ? `<ul class="auto-notas">${a.notas.map(x => `<li>${mdLite(x)}</li>`).join("")}</ul>` : ""}
    </section>`;
  }
  function wireAuto(l, slug) {
    const box = $("[data-auto]"); if (!box) return;
    const vals = () => Object.fromEntries($$("[data-v]", box).map(i => [i.dataset.v, i.value.trim()]));
    const paint = () => { $(".auto-code code", box).textContent = autoFill(l.auto, vals()); };
    $$("[data-v]", box).forEach(i => i.addEventListener("input", paint)); paint();
    $("[data-copy]", box).onclick = async e => { const b = e.currentTarget; try { await navigator.clipboard.writeText(autoFill(l.auto, vals())); b.lastChild.textContent = "Copiado"; } catch { const r = document.createRange(); r.selectNodeContents($(".auto-code", box)); getSelection().removeAllRanges(); getSelection().addRange(r); b.lastChild.textContent = "Seleccionado: Ctrl+C"; } setTimeout(() => b.lastChild.textContent = "Copiar script", 1800); };
    const K = autoKind(l, slug);
    $("[data-dl]", box).onclick = () => { const txt = autoFill(l.auto, vals()); const blob = new Blob([K.crlf ? txt.replace(/\n/g, "\r\n") : txt], {type: "text/plain"}); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `ies-${slug}-leccion-${l.n}.${K.ext}`; document.body.append(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500); };
  }

  /* ---------- contenido solo para registrados ---------- */
  function lockedPage(title, text, inner = "") {
    return `<div class="wrap"><section class="card lock-card"><span class="lock-ic">${icon("lock")}</span><h1>${title}</h1><p>${text}</p>
      <div class="row"><a class="btn" href="#/registro">Crear cuenta gratis</a><a class="btn ghost" href="#/ingresar">Ya tengo cuenta</a></div>${inner}</section></div>`;
  }
  function viewLessonLocked(c, l) {
    try { sessionStorage.setItem("ies.back", location.hash); } catch {}
    const ai = (c.arcs || []).findIndex(a => a.lessons.map(String).includes(lid(l)));
    main.innerHTML = `
      <div class="player-top"><div class="wrap player-top-in"><a class="back" href="#/curso/${c.slug}">${icon("back")}<span>${esc(c.title)}</span></a></div></div>
      <div class="wrap l-layout">
        <div>
          <section class="card l-head"><div class="row"><span class="pill info">Lección ${l.n} de ${c.lessons.length}</span>${ai >= 0 ? `<span class="pill plain">Módulo ${ai + 1}: ${esc(c.arcs[ai].title)}</span>` : ""}</div><h1>${esc(l.handle)}</h1></section>
          <section class="card lock-card in"><span class="lock-ic">${icon("lock")}</span><h2>Esta lección es para técnicos registrados</h2>
            <p>Con una cuenta gratis ves cada lección completa (la idea, los conceptos con ejemplos, el laboratorio paso a paso con ilustraciones), rendís los exámenes y tu avance queda guardado para la constancia.</p>
            <ul class="lock-list"><li>${icon("book")}${c.lessons.length} lecciones</li><li>${icon("flask")}${c.lessons.reduce((a, x) => a + (x.lab?.minutes || 0), 0)} min de laboratorio</li><li>${icon("quiz")}${c.lessons.reduce((a, x) => a + (x.quiz_n || 0), 0)} preguntas de examen</li><li>${icon("award")}Constancia al terminar</li></ul>
            <div class="row"><a class="btn" href="#/registro">Crear cuenta gratis</a><a class="btn ghost" href="#/ingresar">Ya tengo cuenta</a></div></section>
        </div>
        <aside class="card side" aria-label="Contenido del curso"><div class="side-h"><h2>Contenido del curso</h2><p>${c.lessons.length} lecciones</p></div>
          ${(c.arcs || []).map((a, i) => `<details class="acc" ${i === ai ? "open" : ""}><summary>${icon("chev", "i chev")}<div><span class="k">Módulo ${i + 1}</span><h3>${esc(a.title)}</h3></div></summary>
            <ul class="side-list">${arcLessons(c, a).map(x => `<li class="${x.n === l.n ? "cur" : ""}"><span class="ck lk">${icon("lock")}</span><a href="#/curso/${c.slug}/${x.n}">${x.n}. ${esc(x.handle)}</a></li>`).join("")}</ul></details>`).join("")}
        </aside>
      </div>`;
    document.title = `${l.handle} · ${c.title} · IES Training`;
  }

  /* ---------- edición en el portal (administradores y editores) ---------- */
  const ie = (val, ph, cls = "", tag = "div", md = false) => md
    ? `<${tag} class="ie md ${cls}" contenteditable="plaintext-only" spellcheck="true" data-ph="${esc(ph)}" data-md="${esc(val || "")}" data-mode="view">${mdLite(val || "")}</${tag}>`
    : `<${tag} class="ie ${cls}" contenteditable="plaintext-only" spellcheck="true" data-ph="${esc(ph)}">${esc(val || "")}</${tag}>`;
  const ieText = el => el.innerText.replace(/ /g, " ").replace(/\n{3,}/g, "\n\n").trim();
  function editBar(slug, d, onSave, back) {
    const bar = document.createElement("div"); bar.className = "ebar"; bar.setAttribute("role", "region"); bar.setAttribute("aria-label", "Edición");
    bar.innerHTML = `<div class="wrap ebar-in"><span class="ebar-k">${icon("edit")}Modo edición</span><span class="dirty" id="edDirty" ${d.dirty ? "" : "hidden"}>Cambios sin guardar</span>
      <div class="row"><a class="btn ghost sm" href="${back}" id="edBack">Ver como alumno</a><button class="btn ghost sm" id="edUndo" ${d.dirty ? "" : "hidden"}>Descartar</button><button class="btn sm" id="edSave">${icon("check")}Guardar cambios</button></div></div>`;
    document.body.append(bar);
    const mark = () => { d.dirty = true; $("#edDirty").hidden = false; $("#edUndo").hidden = false; };
    $("#edSave").onclick = async () => { const b = $("#edSave"); b.disabled = true; b.lastChild.textContent = "Guardando…"; try { await onSave(); } catch (e) { toast(e.status === 409 ? "Otra persona guardó este curso mientras editabas. Descartá y volvé a abrir." : e.message); b.disabled = false; b.lastChild.textContent = "Guardar cambios"; } };
    $("#edUndo").onclick = async () => { await loadDraft(slug, true); toast("Cambios descartados"); route(); };
    $("#edBack").onclick = e => { if (d.dirty && !confirmLeave()) e.preventDefault(); };
    return mark;
  }
  const confirmLeave = () => window.confirm("Hay cambios sin guardar. ¿Salir igual? Quedan guardados como borrador en esta pestaña.");
  const removeBars = () => $$(".ebar").forEach(x => x.remove());
  window.addEventListener("hashchange", removeBars);
  window.addEventListener("beforeunload", e => { if (Object.values(drafts).some(d => d.dirty) && $(".ebar")) { e.preventDefault(); e.returnValue = ""; } });

  async function viewLessonEdit(slug, n) {
    if (!session.staff()) { location.hash = `#/curso/${slug}/${n}`; return; }
    const d = await loadDraft(slug); const c = d.course;
    const l = c.lessons.find(x => x.n === n) || c.lessons[n - 1];
    if (!l) { location.hash = `#/curso/${slug}`; return; }
    const m = await loadMarked();
    l.idea_md = (l.idea_md && l.idea_md.length ? l.idea_md : ["", "", ""]); l.quiz = l.quiz || []; l.sources = l.sources || []; l.lab = l.lab || {}; l.concepts = l.concepts || [];
    l.idea_pics = l.idea_md.map((_, i) => (l.idea_pics || [])[i] || []); l.concepts.forEach(k => { k.pics = k.pics || []; }); l.theory_md = l.theory_md || "";
    const pos = c.lessons.indexOf(l) + 1, ai = (c.arcs || []).findIndex(a => a.lessons.includes(lid(l)));
    const prev = c.lessons[pos - 2], next = c.lessons[pos];
    let target = null;
    const ptArr = key => key[0] === "i" ? l.idea_pics[+key.slice(1)] : key[0] === "k" ? l.concepts[+key.slice(1)]?.pics : null;
    const conceptEd = (k, ki) => `<article class="card concept ed" data-ki="${ki}"><h3><span class="cn">${String(ki + 1).padStart(2, "0")}</span>${ie(k.name, "Nombre del concepto (ej. Safe Mode)", "", "span")}<button class="mini del" data-delk="${ki}" type="button">Quitar</button></h3>
      <div class="cgrid3"><div><span class="ck-l">${icon("quiz")}Para qué se creó</span>${ie(k.para_que, "El problema que vino a resolver…", "p", "div", true)}</div><div><span class="ck-l">${icon("flask")}Cómo se usa</span>${ie(k.como, "Dónde se activa, qué se configura, qué cuidar…", "p", "div", true)}</div><div class="ex"><span class="ck-l">${icon("pin")}Ejemplo en obra</span>${ie(k.ejemplo, "Un caso concreto: edificio, cliente, barrera…", "p", "div", true)}</div></div>${picsEd(k.pics, `k${ki}`)}</article>`;
    const qEd = (q, qi) => `<div class="card q ed" data-qi="${qi}"><div class="q-top"><span class="k">Pregunta ${qi + 1}</span><button class="mini del" type="button" data-delq="${qi}">Quitar pregunta</button></div>
      ${ie(q.q, "Escribí la pregunta, mejor como situación de obra", "q-q")}
      ${[0, 1, 2, 3].map(j => `<label class="opt ed ${q.answer === j ? "right" : ""}"><input type="radio" name="ans${qi}" value="${j}" ${q.answer === j ? "checked" : ""} aria-label="Marcar ${"ABCD"[j]} como correcta"><b>${"ABCD"[j]}</b>${ie(q.options[j] || "", `Opción ${"ABCD"[j]}`, "o-t", "span")}</label>`).join("")}
      <span class="ck-l">Por qué la correcta es correcta</span>${ie(q.why, "La explicación que ve el técnico al responder", "q-why", "div", true)}</div>`;
    main.innerHTML = `
      <div class="player-top edit"><div class="wrap player-top-in"><a class="back" href="#/curso/${slug}/${n}">${icon("back")}<span>${esc(c.title)}</span></a>
        <div class="row">${prev ? `<a class="btn ghost sm" href="#/curso/${slug}/${prev.n}/editar">${icon("back")}Lección ${prev.n}</a>` : ""}${next ? `<a class="btn ghost sm" href="#/curso/${slug}/${next.n}/editar">Lección ${next.n}${icon("chev")}</a>` : ""}<a class="btn ghost sm" href="#/admin/cursos/${slug}/${encodeURIComponent(lid(l))}">Editor completo</a></div></div></div>
      <div class="wrap l-layout edit-mode">
        <div>
          <section class="card l-head"><div class="row"><span class="pill info">Lección ${pos} de ${c.lessons.length}</span>${ai >= 0 ? `<span class="pill plain">Módulo ${ai + 1}: ${esc(c.arcs[ai].title)}</span>` : ""}<span class="pill warn">Editando</span></div>
            ${ie(l.handle, "Nombre de la lección (2 a 4 palabras)", "h1", "h1")}${ie(l.summary, "Resumen de una línea (aparece en el temario)", "sum", "p")}</section>
          <div class="tabs" role="tablist">${[["resumen", "Resumen"], ["teoria", "Teoría"], ["laboratorio", "Laboratorio"], ["quiz", "Examen"], ["fuentes", "Fuentes"]].map(([k, t], i) => `<button class="tab" role="tab" aria-selected="${i === 0}" data-tab="${k}">${t}</button>`).join("")}</div>

          <section class="panel" id="p-resumen">
            <div class="card route-box ed"><p class="conecta"><span class="k">De dónde venimos</span>${ie(l.conecta, "Cómo se conecta con la lección anterior (1 o 2 oraciones)", "e-con", "span")}</p>
              <div class="objs"><span class="k">En esta lección vas a</span><ul id="objs"></ul><button class="mini" type="button" id="addObj">+ Objetivo</button></div>
              <p class="conecta"><span class="k">Qué sigue</span>${ie(l.sigue, "Qué deja planteado para la próxima lección", "e-sig", "span")}</p></div>
            <figure class="l-fig ed figx" id="figBox" tabindex="0" data-pt="fig" aria-label="Ilustración principal: hacé clic y pegá con Ctrl+V, arrastrá una imagen o subila"></figure>
            <span class="k">La idea, en tres líneas</span>
            <ul class="ideas ed" id="ideas"></ul>
            <div class="row" style="margin:-6px 0 18px"><button class="mini" type="button" id="addIdea">+ Agregar línea</button><span class="note">Admite \`código\` y **negrita**.</span></div>
            <div id="animsEd"></div>
            <div class="kv">
              <div class="card"><span class="k">Qué mejora en la obra</span>${ie(l.impact_md, "Una línea: qué mejora en obra o soporte", "p", "p", true)}</div>
              <div class="card"><span class="k">Quién lo dice</span>${ie(l.who_md, "N de M fuentes coinciden; quién discrepa…", "p", "p", true)}</div>
            </div>
            <div class="rule"><span class="k">Regla para tu manual</span><blockquote>${ie(l.rule, "Una oración para el manual de bolsillo", "rule-t", "span", true)}</blockquote></div>
          </section>

          <section class="panel" id="p-teoria" hidden>
            <div class="card lab"><div class="lab-h"><h2>Historia y teoría</h2><span class="note">Usá los subtítulos <code>### Un poco de historia</code> y <code>### Cómo funciona</code>.</span></div>
              <div class="lab-split"><label class="lab-src"><span class="sr">Teoría en Markdown</span><textarea id="thMd" spellcheck="true" placeholder="### Un poco de historia&#10;De dónde viene esta tecnología…&#10;&#10;### Cómo funciona&#10;Qué pasa por dentro…">${esc(l.theory_md)}</textarea></label><div class="lab-body theory" id="thPrev"></div></div></div>
            <section class="concepts"><div class="concepts-h"><span class="k">Para qué sirve cada cosa</span><h2>Los conceptos, con ejemplos</h2></div><div id="conc"></div>
              <button class="btn ghost sm" type="button" id="addK">${icon("plus")}Agregar concepto</button></section>
          </section>

          <section class="panel" id="p-laboratorio" hidden>
            <div class="card lab">
              <div class="lab-h"><h2>Laboratorio</h2><div class="row"><label class="sel-s"><span class="sr">Tipo</span><select id="labE">${["Rápido", "Foco", "Campo", "Admin"].map(x => `<option ${l.lab.energy === x ? "selected" : ""}>${x}</option>`).join("")}</select></label><label class="min-in"><input id="labM" type="number" min="0" max="240" value="${l.lab.minutes ?? ""}"> min</label></div></div>
              <div class="lab-tools"><label class="btn ghost sm">${icon("upload")}Imagen, GIF o video<input type="file" id="insF" accept="image/png,image/jpeg,image/webp,image/gif,video/mp4,video/webm" multiple hidden></label>
                <button class="btn ghost sm" type="button" id="insGif">GIF con capturas</button><button class="btn ghost sm" type="button" id="insY">${icon("link")}YouTube o Vimeo</button><button class="btn ghost sm" type="button" data-wrap="code">\`código\`</button><button class="btn ghost sm" type="button" data-block="routeros">Bloque de comandos</button><button class="btn ghost sm" type="button" data-block="warn">⚠️ Advertencia</button><span class="note" id="insS" role="status"></span></div>
              <div class="lab-split"><label class="lab-src"><span class="sr">Pasos en Markdown</span><textarea id="labMd" spellcheck="true">${esc(l.lab.md || "")}</textarea></label><div class="lab-body" id="labPrev" aria-live="polite"></div></div>
            </div>
            <div class="card lab auto-ed"><div class="lab-h"><h2>Script para automatizar</h2><span class="note">Las variables se escriben <code>{{NOMBRE}}</code> en el código; el alumno las completa antes de copiar.</span></div>
              <div class="form grid2"><label>Título<input id="auT" value="${esc(l.auto?.titulo || "")}" placeholder="Ej. Crear un usuario por técnico"></label><label>Qué deja configurado<input id="auD" value="${esc(l.auto?.descripcion || "")}"></label></div>
              <div id="auV"></div><button class="mini" type="button" id="auAdd">+ Variable</button>
              <label class="lab-src"><span class="sr">Código</span><textarea id="auC" spellcheck="false" placeholder="# Script de RouterOS…">${esc(l.auto?.codigo || "")}</textarea></label>
              <label class="form"><span class="note">Notas (una por línea)</span><textarea id="auN" rows="3">${esc((l.auto?.notas || []).join("\n"))}</textarea></label></div>
          </section>

          <section class="panel" id="p-quiz" hidden><div class="quiz" id="qz"></div><button class="btn ghost sm" type="button" id="addQ">${icon("plus")}Agregar pregunta</button></section>

          <section class="panel" id="p-fuentes" hidden><div class="card pad"><div id="srcs"></div><button class="btn ghost sm" type="button" id="addS">${icon("plus")}Agregar fuente</button></div></section>
        </div>
        <aside class="card side ed-help"><div class="side-h"><h2>Cómo editar</h2></div>
          <ul class="help-l"><li>Hacé clic sobre cualquier texto y escribí: se edita en el lugar, con el mismo aspecto que ve el alumno.</li><li>El laboratorio se escribe a la izquierda y se ve a la derecha tal como queda.</li><li><b>Fotos, GIF y videos en cualquier punto:</b> hacé clic en una idea, un concepto, un paso del laboratorio o un párrafo de la teoría y pegá con <kbd>Ctrl</kbd>+<kbd>V</kbd>, o arrastrá los archivos encima. También con los botones de cada punto o con <b>clic derecho</b> (Pegar, Subir, Armar GIF, Video).</li><li>Clic derecho sobre una foto: ver grande, pie, reemplazar, ordenar o quitar. <kbd>Shift</kbd> + clic derecho abre el menú del navegador.</li><li>Nada se publica hasta que tocás <b>Guardar cambios</b>. Cada guardado queda en el historial del curso.</li></ul>
          <p class="note">Lección ${pos}: ${l.idea_md.filter(x => x.trim()).length} ideas, ${l.concepts.length} conceptos, ${l.quiz.length} preguntas, ${l.sources.length} fuentes.</p></aside>
      </div>`;
    document.title = `Editar: ${l.handle} · IES Training`;
    const mark = editBar(slug, d, async () => { await saveDraft(slug); forgetCourses(); toast("Lección guardada"); location.hash = `#/curso/${slug}/${pos}`; }, `#/curso/${slug}/${pos}`);
    const clearDirty = () => { d.dirty = false; const a = $("#edDirty"), b = $("#edUndo"); if (a) a.hidden = true; if (b) b.hidden = true; };
    const bind = (el, fn) => el.addEventListener("input", () => { fn(ieText(el)); mark(); });
    $$(".tab").forEach(t => t.onclick = () => { $$(".tab").forEach(x => x.setAttribute("aria-selected", x === t)); $$(".panel").forEach(p => p.hidden = p.id !== `p-${t.dataset.tab}`); });
    bind($(".l-head .h1"), v => l.handle = v); bind($(".l-head .sum"), v => l.summary = v);
    bind($(".e-con"), v => l.conecta = v); bind($(".e-sig"), v => l.sigue = v);
    l.objetivos = l.objetivos || [];
    const paintObj = () => { $("#objs").innerHTML = l.objetivos.map((o, i) => `<li>${icon("check")}${ie(o, "Al terminar vas a poder…", "", "span")}<button class="mini del" type="button" data-oi="${i}" aria-label="Quitar">×</button></li>`).join(""); $$("#objs .ie").forEach((el, i) => bind(el, v => l.objetivos[i] = v)); $$("[data-oi]").forEach(b => b.onclick = () => { l.objetivos.splice(+b.dataset.oi, 1); mark(); paintObj(); }); };
    paintObj(); $("#addObj").onclick = () => { l.objetivos.push(""); paintObj(); $$("#objs .ie").pop().focus(); };
    $$(".kv .ie").forEach((el, i) => bind(el, v => { if (i === 0) l.impact_md = v; else l.who_md = v; }));
    bind($(".rule-t"), v => l.rule = v);
    // ilustración principal: pegar (Ctrl+V o botón), arrastrar o subir; se sube y se guarda sola
    const FIG_OK = /^image\/(png|jpeg|webp|gif)$/;
    let figBusy = false;
    const figSaved = (txt, cls = "ok") => { const ch = $("#figState"); if (!ch) return; ch.className = `fx-state ${cls}`; ch.innerHTML = `${cls === "ok" ? icon("check") : cls === "err" ? "" : '<i class="fx-spin"></i>'}<span>${esc(txt)}</span>`; };
    const paintFig = (anim) => {
      const f = $("#figBox");
      f.classList.toggle("has", !!l.fig); f.classList.remove("fx-out");
      f.innerHTML = (l.fig ? `<div class="fx-media${anim ? " fx-in" : ""}"><img src="${esc(l.fig.src)}" alt="${esc(l.fig.alt || "")}"></div>
          <figcaption>${ie(l.fig.caption, "Qué mirar en la imagen (una línea)", "", "span")}</figcaption>`
        : `<div class="fx-empty"><span class="fx-ico">${icon("image")}</span><b>Ilustración principal</b><span>Hacé clic acá y pegá con <kbd>Ctrl</kbd>+<kbd>V</kbd>, arrastrá una imagen o subila.</span><span class="fx-fmt">PNG · JPG · WebP · GIF animado</span></div>`)
        + `<div class="fx-tools" role="toolbar" aria-label="Ilustración principal">
            <button class="fx-b" type="button" id="figPaste" title="Pegar la imagen copiada">${icon("clip")}<span>Pegar</span></button>
            <label class="fx-b" title="Subir desde la computadora">${icon("upload")}<span>Subir</span><input type="file" accept="image/png,image/jpeg,image/webp,image/gif" hidden></label>
            ${l.fig ? `<button class="fx-b fx-danger" type="button" id="figX" title="Quitar la ilustración">${icon("trash")}<span>Quitar</span></button>` : ""}
          </div>
          <span class="fx-hint">${icon("clip")}Ctrl+V reemplaza la imagen</span>
          <span class="fx-state" id="figState" hidden></span>
          <div class="fx-drop"><span>${icon("upload")}Soltá la imagen para reemplazarla</span></div>
          <div class="fx-prog" hidden><svg viewBox="0 0 44 44"><circle cx="22" cy="22" r="19"/><circle class="fx-arc" cx="22" cy="22" r="19"/></svg><b>0%</b></div>`;
      $("input[type=file]", f).onchange = e => { const file = e.target.files[0]; e.target.value = ""; if (file) setFig(file); };
      $("#figPaste").onclick = e => { e.stopPropagation(); pasteFig(); };
      $("#figX")?.addEventListener("click", async e => { e.stopPropagation(); if (!window.confirm("¿Quitar la ilustración principal de esta lección?")) return; f.classList.add("fx-out"); await new Promise(r => setTimeout(r, 220)); delete l.fig; mark(); paintFig(); await saveFig("Ilustración quitada"); });
      const cap = $("figcaption .ie", f); if (cap) bind(cap, v => { l.fig.caption = v; });
    };
    async function pasteFig() {
      if (!navigator.clipboard?.read) { $("#figBox").focus(); toast("Hacé clic en la imagen y pegá con Ctrl+V."); return; }
      try {
        for (const it of await navigator.clipboard.read()) {
          const t = it.types.find(x => FIG_OK.test(x)) || it.types.find(x => x.startsWith("image/"));
          if (t) { const b = await it.getType(t); return setFig(new File([b], `portapapeles.${(t.split("/")[1] || "png").replace("jpeg", "jpg")}`, {type: b.type || t})); }
        }
        toast("No hay ninguna imagen copiada. Copiá una captura (Win+Shift+S) y volvé a tocar Pegar.");
      } catch { $("#figBox").focus(); toast("El navegador no dejó leer el portapapeles: con la imagen marcada, pegá con Ctrl+V."); }
    }
    async function saveFig(okText) {
      figSaved("Guardando…", "busy"); $("#figState").hidden = false;
      try { await saveDraft(slug, true); forgetCourses(); clearDirty(); figSaved(okText); setTimeout(() => { const st = $("#figState"); if (st) st.classList.add("fx-fade"); }, 2600); }
      catch (e) { figSaved(e.status === 409 ? "No se guardó: otra persona guardó el curso" : "No se guardó: tocá Guardar cambios", "err"); }
    }
    async function setFig(file) {
      if (figBusy) return;
      if (!FIG_OK.test(file.type)) { toast("Solo imágenes PNG, JPG, WebP o GIF."); return; }
      const f = $("#figBox"); figBusy = true; setTarget("fig");
      const local = URL.createObjectURL(file);
      // vista previa inmediata, desenfocada mientras sube
      f.classList.add("has", "fx-up");
      let media = $(".fx-media", f);
      if (!media) { $(".fx-empty", f)?.remove(); f.insertAdjacentHTML("afterbegin", `<div class="fx-media"><img alt=""></div>`); media = $(".fx-media", f); }
      $("img", media).src = local;
      const prog = $(".fx-prog", f), arc = $(".fx-arc", f), pct = $(".fx-prog b", f); prog.hidden = false;
      const setP = p => { arc.style.strokeDashoffset = String(119.4 * (1 - p / 100)); pct.textContent = `${p}%`; };
      setP(2);
      try {
        const j = await uploadInline(slug, l, file, setP); setP(100);
        // imagen nueva: el texto alternativo de la anterior ya no la describe; el pie queda para editarlo
        l.fig = {src: j.captura.url, alt: `Ilustración de la lección ${l.handle || ""}`.trim(), caption: l.fig?.caption || ""};
        await new Promise(r => { const im = new Image(); im.onload = im.onerror = r; im.src = j.captura.url; });
        mark(); f.classList.remove("fx-up"); paintFig(true); f.classList.add("fx-flash"); setTimeout(() => f.classList.remove("fx-flash"), 900);
        await saveFig("Imagen guardada");
      } catch (err) { f.classList.remove("fx-up"); paintFig(); toast(err.message); }
      finally { URL.revokeObjectURL(local); figBusy = false; }
    }
    { // arrastrar y soltar sobre la ilustración
      const f = $("#figBox"); let depth = 0;
      f.addEventListener("dragenter", e => { if ([...(e.dataTransfer?.types || [])].includes("Files")) { e.preventDefault(); depth++; f.classList.add("fx-over"); } });
      f.addEventListener("dragover", e => { if ([...(e.dataTransfer?.types || [])].includes("Files")) e.preventDefault(); });
      f.addEventListener("dragleave", () => { if (--depth <= 0) { depth = 0; f.classList.remove("fx-over"); } });
      f.addEventListener("drop", e => { e.preventDefault(); depth = 0; f.classList.remove("fx-over"); const file = [...(e.dataTransfer?.files || [])].find(x => FIG_OK.test(x.type)); if (file) setFig(file); else toast("Soltá una imagen PNG, JPG, WebP o GIF."); });
      f.addEventListener("click", e => { if (!e.target.closest(".ie,.fx-tools")) f.focus(); });
    }
    paintFig();
    const paintAnims = () => {
      const box = $("#animsEd"); if (!box) return;
      box.innerHTML = (l.anims || []).length ? `<section class="anims ed"><span class="k">Cómo se ve en la red · animaciones</span>${l.anims.map((a, ai2) => `<figure class="lab-fig"><img src="${esc(a.src)}" alt="${esc(a.alt || "")}" loading="lazy" width="1200" height="675"><figcaption>${esc(a.caption || "")} <button class="mini del" type="button" data-dela="${ai2}">Quitar</button></figcaption></figure>`).join("")}</section>` : "";
      $$("[data-dela]", box).forEach(b => b.onclick = () => { if (!b.dataset.armed) { b.dataset.armed = 1; b.textContent = "¿Quitar?"; return; } l.anims.splice(+b.dataset.dela, 1); if (!l.anims.length) delete l.anims; mark(); paintAnims(); });
    };
    paintAnims();
    // ideas
    const paintIdeas = () => {
      $("#ideas").innerHTML = l.idea_md.map((x, i) => `<li data-pt="i${i}"><i></i><div>${ie(x, "Una idea en una línea", "", "span", true)}${picsEd(l.idea_pics[i], `i${i}`)}</div>${l.idea_md.length > 1 ? `<button class="mini del" type="button" data-deli="${i}" aria-label="Quitar línea">×</button>` : ""}</li>`).join("");
      $$("#ideas > li > div > .ie").forEach((el, i) => bind(el, v => l.idea_md[i] = v));
      $$("[data-deli]").forEach(b => b.onclick = () => { l.idea_md.splice(+b.dataset.deli, 1); l.idea_pics.splice(+b.dataset.deli, 1); mark(); paintIdeas(); });
      wirePics($("#ideas"));
    };
    paintIdeas();
    $("#addIdea").onclick = () => { if (l.idea_md.length < 6) { l.idea_md.push(""); l.idea_pics.push([]); paintIdeas(); $$("#ideas > li > div > .ie").pop().focus(); } };
    // conceptos
    const paintK = () => {
      $("#conc").innerHTML = l.concepts.map(conceptEd).join("") || `<p class="note">Todavía no hay conceptos. Sumá uno por cada idea que un técnico nuevo necesita entender: para qué se creó, cómo se usa y un ejemplo.</p>`;
      $$("#conc .concept").forEach(card => { card.dataset.pt = `k${card.dataset.ki}`; const k = l.concepts[+card.dataset.ki]; const [nm, a, b2, c2] = $$(".ie", card); bind(nm, v => k.name = v); bind(a, v => k.para_que = v); bind(b2, v => k.como = v); bind(c2, v => k.ejemplo = v); });
      wirePics($("#conc"));
      $$("[data-delk]").forEach(b => b.onclick = () => { if (!b.dataset.armed) { b.dataset.armed = 1; b.textContent = "¿Quitar?"; return; } l.concepts.splice(+b.dataset.delk, 1); mark(); paintK(); });
    };
    paintK();
    $("#addK").onclick = () => { l.concepts.push({name: "", para_que: "", como: "", ejemplo: "", pics: []}); mark(); paintK(); $$("#conc .concept .ie")[4 * (l.concepts.length - 1)]?.focus(); };
    // laboratorio: Markdown a la izquierda, vista previa a la derecha
    const ta = $("#labMd");
    const grow = () => { ta.style.height = "auto"; ta.style.height = Math.max(420, ta.scrollHeight + 4) + "px"; };
    const prevLab = () => {
      $("#labPrev").innerHTML = mdBlock(m, ta.value);
      $$("#labPrev pre").forEach(pre => { const lang = (pre.querySelector("code")?.className.match(/language-(\w+)/) || [])[1]; if (lang) pre.dataset.lang = lang; });
      $$("#labPrev ol > li").forEach((li, k) => {
        li.dataset.pt = `s${k}`; li.classList.toggle("ptarget", target === `s${k}`);
        li.insertAdjacentHTML("afterbegin", ptTools());
      });
      mediaTools($("#labPrev"), "lab");
    };
    ta.addEventListener("input", () => { l.lab.md = ta.value; mark(); prevLab(); grow(); });
    prevLab(); setTimeout(grow, 0);
    $("#labE").onchange = e => { l.lab.energy = e.target.value; mark(); };
    $("#labM").oninput = e => { l.lab.minutes = e.target.value === "" ? null : +e.target.value; mark(); };
    // ---- medios en cualquier punto de la lección ----
    // destinos (data-pt): fig ilustración principal · i<n> idea · k<n> concepto · s<n> paso del laboratorio · t<n> párrafo de la teoría
    // y lab / theory (en el cursor del texto Markdown). Se llega pegando (Ctrl+V), arrastrando, con los botones de cada punto o con clic derecho.
    const ac = new AbortController(), signal = ac.signal;
    window.addEventListener("hashchange", () => ac.abort(), {once: true});
    function setTarget(key) { target = key; $$("[data-pt]").forEach(x => x.classList.toggle("ptarget", x.dataset.pt === key)); }
    const keyOf = el => { if (!el?.closest || el.closest(".ctx")) return null; if (el.closest("#figBox")) return "fig"; if (el.closest("#labMd")) return "lab"; if (el.closest("#thMd")) return "theory"; const pt = el.closest("[data-pt]"); return pt ? pt.dataset.pt : null; };
    const elOf = key => key === "lab" ? $("#labMd")?.parentElement : key === "theory" ? $("#thMd")?.parentElement : $(`[data-pt="${key}"]`);
    const MD_KEY = k => k === "lab" || k === "theory" || /^[st]\d/.test(k || "");
    const ACC = k => MD_KEY(k) ? "image/png,image/jpeg,image/webp,image/gif,video/mp4,video/webm" : "image/png,image/jpeg,image/webp,image/gif";
    const WHERE = k => ({fig: "la ilustración principal", lab: "el laboratorio, donde está el cursor", theory: "la teoría, donde está el cursor"})[k] || ({i: "esta idea", k: "este concepto", s: "este paso", t: "este párrafo"})[k?.[0]] || "";
    main.addEventListener("focusin", e => { const k = keyOf(e.target); if (k) setTarget(k); }, {signal});
    main.addEventListener("click", e => { const k = keyOf(e.target); if (k && k !== target) setTarget(k); }, {signal});
    const figHTML = (u, cap = "", video = false) => `<figure class="lab-fig">${video ? `<video src="${u}" controls muted playsinline preload="metadata"></video>` : `<img src="${u}" alt="${esc(cap)}" loading="lazy">`}${cap ? `<figcaption>${esc(cap)}</figcaption>` : ""}</figure>`;
    const insertAfterStep = (md, k, html) => {
      const ls = md.split("\n"); let fence = false; const nums = [];
      ls.forEach((ln, i) => { if (/^\s*```/.test(ln)) fence = !fence; else if (!fence && /^\d+\.\s/.test(ln)) nums.push(i); });
      if (nums[k] === undefined) return md + `\n\n${html}\n`;
      let j = nums[k] + 1; fence = false;
      while (j < ls.length) { const ln = ls[j]; if (/^\s*```/.test(ln)) fence = !fence; else if (!fence && (/^\d+\.\s/.test(ln) || ln.startsWith("⚠️"))) break; j++; }
      while (j > nums[k] + 1 && !ls[j - 1].trim()) j--;
      return [...ls.slice(0, j), "", html, "", ...ls.slice(j)].join("\n");
    };
    // bloques de la teoría: separados por una línea en blanco, sin cortar bloques de código
    const thBlocks = md => { const out = []; let cur = [], fence = false; (md || "").split("\n").forEach(ln => { if (/^\s*```/.test(ln)) fence = !fence; if (!fence && !ln.trim()) { if (cur.length) { out.push(cur.join("\n")); cur = []; } } else cur.push(ln); }); if (cur.length) out.push(cur.join("\n")); return out; };
    const embedHTML = u => { const yt = u.match(/(?:youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/)|youtu\.be\/)([A-Za-z0-9_-]{11})/), vm = u.match(/vimeo\.com\/(?:video\/)?(\d{5,12})/);
      return yt || vm ? `<div class="embed"><iframe src="${yt ? `https://www.youtube-nocookie.com/embed/${yt[1]}` : `https://player.vimeo.com/video/${vm[1]}`}" title="Video" allow="fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>` : null; };
    // pone un bloque HTML en un destino de texto (laboratorio, teoría, paso o párrafo)
    function putHTML(key, html) {
      if (key === "lab") insert(`\n\n${html}\n\n`);
      else if (key === "theory") thInsert(`\n\n${html}\n\n`);
      else if (key[0] === "s") { ta.value = insertAfterStep(ta.value, +key.slice(1), html); l.lab.md = ta.value; mark(); prevLab(); grow(); }
      else if (key[0] === "t") { const b = thBlocks(th.value); b.splice(Math.min(+key.slice(1) + 1, b.length), 0, html); th.value = b.join("\n\n"); th.dispatchEvent(new Event("input")); }
    }
    // indicador de subida sobre el punto de destino
    const busy = (key, on, p) => {
      const el = elOf(key); if (!el) return; let b = el.querySelector(":scope > .up-ph");
      if (!on) { b?.remove(); el.classList.remove("up-on"); return; }
      if (!b) { b = document.createElement("div"); b.className = "up-ph"; b.innerHTML = `<i class="fx-spin"></i><span>Subiendo</span><b></b>`; el.append(b); el.classList.add("up-on"); }
      if (p != null) b.querySelector("b").textContent = `${p}%`;
    };
    async function addPhoto(file, key = target) {
      if (!key) { toast("Elegí dónde va: hacé clic en la idea, el concepto, el paso o el párrafo, y volvé a pegar o soltar."); return; }
      if (key === "fig") return setFig(file);
      const video = /^video\//.test(file.type);
      if (!MEDIA_OK.test(file.type)) { toast("Formato no admitido: imágenes PNG, JPG, WebP o GIF, y videos MP4 o WebM."); return; }
      if (video && !MD_KEY(key)) { toast("Los videos van en el laboratorio o en la teoría. Acá podés poner una imagen o un GIF."); return; }
      busy(key, true, 0);
      try {
        const j = await uploadInline(slug, l, file, p => busy(key, true, p));
        const u = j.captura.url;
        if (MD_KEY(key)) putHTML(key, figHTML(u, "", video));
        else { const arr = ptArr(key); if (!arr) return; arr.push({src: u, caption: ""}); mark(); key[0] === "i" ? paintIdeas() : paintK(); }
        setTarget(key); toast(video ? "Video agregado" : file.type === "image/gif" ? "GIF agregado" : "Foto agregada");
      } catch (err) { toast(err.message); }
      finally { busy(key, false); }
    }
    const addFiles = async (files, key = target) => { for (const f of files) await addPhoto(f, key); };
    fmtHook = async (file, el) => addPhoto(file, keyOf(el) || target);
    const pickFiles = (accept, multiple = true) => new Promise(res => { const i = document.createElement("input"); i.type = "file"; i.accept = accept; i.multiple = multiple; i.onchange = () => res([...i.files]); i.click(); });
    async function act(a, key, editable) {
      if (!key) return;
      setTarget(key);
      if (a === "file") { const fs = await pickFiles(ACC(key), key !== "fig"); if (!fs.length) return; key === "fig" ? setFig(fs[0]) : addFiles(fs, key); }
      else if (a === "paste") {
        const fs = await clipImages();
        if (fs.length) { key === "fig" ? setFig(fs[0]) : addFiles(fs, key); return; }
        const txt = editable ? await navigator.clipboard?.readText?.().catch(() => "") : "";
        if (txt) { editable.focus(); if (editable.tagName === "TEXTAREA") { editable.setRangeText(txt, editable.selectionStart, editable.selectionEnd, "end"); editable.dispatchEvent(new Event("input")); } else document.execCommand("insertText", false, txt); return; }
        toast("No hay ninguna imagen copiada (o el navegador no dejó leerla). Copiá una captura con Win+Shift+S, hacé clic acá y pegá con Ctrl+V.");
      }
      else if (a === "gif") { const f = await gifMaker(); if (f) key === "fig" ? setFig(f) : addPhoto(f, key); }
      else if (a === "video") { const u = prompt("Pegá el enlace de YouTube o Vimeo"); if (!u) return; const h = embedHTML(u.trim()); if (!h) { toast("Ese enlace no es de YouTube ni de Vimeo."); return; } putHTML(MD_KEY(key) ? key : "lab", h); toast("Video agregado"); }
    }
    // fotos de ideas y conceptos: ver, pie, reemplazar, ordenar, quitar
    async function picAct(a, key, i) {
      const arr = ptArr(key); if (!arr || !arr[i]) return; const rp = () => { key[0] === "i" ? paintIdeas() : paintK(); setTarget(key); };
      if (a === "zoom") { lightbox(arr.map(x => ({url: x.src, texto: x.caption, tipo: /\.gif$/i.test(x.src) ? "gif" : "imagen"})), i); return; }
      if (a === "up" && i > 0) [arr[i - 1], arr[i]] = [arr[i], arr[i - 1]];
      else if (a === "dn" && i < arr.length - 1) [arr[i + 1], arr[i]] = [arr[i], arr[i + 1]];
      else if (a === "del") arr.splice(i, 1);
      else if (a === "cap") { const v = prompt("Pie de la foto: qué mirar", arr[i].caption || ""); if (v === null) return; arr[i].caption = v.trim(); }
      else if (a === "rep") { const [f] = await pickFiles(ACC(key), false); if (!f) return; busy(key, true, 0); try { const j = await uploadInline(slug, l, f, p => busy(key, true, p)); arr[i].src = j.captura.url; } catch (err) { toast(err.message); return; } finally { busy(key, false); } }
      else return;
      mark(); rp(); if (a === "del") toast("Foto quitada: si fue sin querer, Deshacer en la barra de abajo");
    }
    // medios dentro del texto del laboratorio o de la teoría
    const mdEl = where => where === "lab" ? ta : th;
    const reEsc = x => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const mdFind = (md, src) => { const e = reEsc(src);
      for (const r of [new RegExp(`<figure\\b(?:(?!</figure>)[\\s\\S])*?${e}(?:(?!</figure>)[\\s\\S])*?</figure>`), new RegExp(`!\\[[^\\]]*\\]\\(${e}\\)`), new RegExp(`<video\\b[^>]*${e}[^>]*>\\s*</video>`), new RegExp(`<div class="embed">(?:(?!</div>)[\\s\\S])*?${e}[^>]*>\\s*</iframe>\\s*</div>`)]) { const mm = md.match(r); if (mm) return {i: mm.index, s: mm[0]}; }
      return null; };
    const mdSet = (where, v) => { const el = mdEl(where); el.value = v.replace(/\n{3,}/g, "\n\n"); el.dispatchEvent(new Event("input")); };
    async function mediaAct(a, where, src) {
      const md = mdEl(where).value, f = mdFind(md, src); if (!f) { toast("No encontré ese medio en el texto."); return; }
      const cut = rep => md.slice(0, f.i) + rep + md.slice(f.i + f.s.length);
      if (a === "zoom") { lightbox([{url: src, texto: "", tipo: /\.gif$/i.test(src) ? "gif" : "imagen"}], 0); return; }
      if (a === "del") { mdSet(where, cut("")); toast("Quitado: si fue sin querer, Deshacer en la barra de abajo"); return; }
      if (a === "cap") {
        const fc = f.s.match(/<figcaption>([\s\S]*?)<\/figcaption>/), pre = (fc?.[1].match(/^\s*<b>[^<]*<\/b>\s*/) || [""])[0];
        const now = fc ? fc[1].slice(pre.length).replace(/<[^>]+>/g, "").trim() : (f.s.match(/^!\[([^\]]*)\]/)?.[1] || "");
        const v = prompt("Pie de la imagen: qué mirar", GENERIC_ALT.test(now) ? "" : now); if (v === null) return;
        const cap = v.trim() || pre ? `<figcaption>${pre}${esc(v.trim())}</figcaption>` : "";
        const nx = f.s.startsWith("<figure") ? (fc ? f.s.replace(fc[0], cap) : f.s.replace(/<\/figure>$/, `${cap}</figure>`)) : f.s.startsWith("![") ? figHTML(src, v.trim()) : `<figure class="lab-fig">${f.s}${cap}</figure>`;
        mdSet(where, cut(nx)); return;
      }
      if (a === "rep") { const [file] = await pickFiles(ACC(where), false); if (!file) return; toast("Subiendo…"); try { const j = await uploadInline(slug, l, file); mdSet(where, cut(f.s.split(src).join(j.captura.url))); toast("Reemplazado"); } catch (err) { toast(err.message); } }
    }
    // barra de cada medio en la vista previa del laboratorio y de la teoría
    function mediaTools(root, where) {
      figurize(root);
      $$("figure, .embed", root).forEach(fg => {
        const md = fg.querySelector("img, video, iframe"); if (!md || fg.querySelector(":scope > .mt")) return;
        const src = md.getAttribute("src"); fg.dataset.src = src; fg.dataset.where = where;
        fg.insertAdjacentHTML("beforeend", `<span class="mt">${md.tagName === "IMG" ? `<button type="button" class="pe-b" data-ma="cap" title="Editar el pie">✎</button><button type="button" class="pe-b" data-ma="rep" title="Reemplazar">${icon("upload")}</button>` : ""}<button type="button" class="pe-b danger" data-ma="del" title="Quitar">${icon("trash")}</button></span>`);
        if (md.tagName === "IMG" && !fg.querySelector("figcaption")) fg.insertAdjacentHTML("beforeend", `<button type="button" class="fc-add" data-ma="cap">+ Agregar un pie</button>`);
      });
    }
    function picsEd(arr, key) {
      return `<div class="pics-ed" data-pk="${key}">${(arr || []).map((x, i) => `<figure class="pe" data-pi="${i}"><div class="pe-m"><img src="${esc(x.src)}" alt="">
          <span class="pe-t"><button type="button" class="pe-b" data-pa="up" ${i === 0 ? "disabled" : ""} title="Mover antes">↑</button><button type="button" class="pe-b" data-pa="dn" ${i === arr.length - 1 ? "disabled" : ""} title="Mover después">↓</button><button type="button" class="pe-b" data-pa="rep" title="Reemplazar">${icon("upload")}</button><button type="button" class="pe-b danger" data-pa="del" title="Quitar">${icon("trash")}</button></span></div>
          <figcaption>${ie(x.caption, "Pie de la foto: qué mirar (opcional)", "", "span")}</figcaption></figure>`).join("")}
        <div class="addbar" data-ab="${key}"><span class="ab-l">${icon("image")}Arrastrá, pegá con Ctrl+V o</span><button type="button" class="ab-b" data-aa="file">${icon("upload")}Subir</button><button type="button" class="ab-b" data-aa="paste">${icon("clip")}Pegar</button><button type="button" class="ab-b" data-aa="gif">GIF</button></div></div>`;
    }
    function wirePics(root) {
      $$(".pics-ed", root).forEach(box => { const arr = ptArr(box.dataset.pk); $$("figcaption .ie", box).forEach((el, i) => bind(el, v => { arr[i].caption = v; })); });
    }
    function ptTools() { return `<span class="pt-tools"><button type="button" data-aa="file" title="Subir foto, GIF o video acá">${icon("image")}</button><button type="button" data-aa="paste" title="Pegar la imagen copiada">${icon("clip")}</button><button type="button" data-aa="gif" title="Armar un GIF con capturas">GIF</button></span>`; }
    // clics de las barras (delegados: sirven para todo lo que se vuelve a pintar)
    main.addEventListener("click", e => {
      const b = e.target.closest("[data-aa]");
      if (b) { e.preventDefault(); e.stopPropagation(); act(b.dataset.aa, b.closest("[data-ab]")?.dataset.ab || keyOf(b)); return; }
      const pb = e.target.closest("[data-pa]");
      if (pb) { e.stopPropagation(); picAct(pb.dataset.pa, pb.closest("[data-pk]").dataset.pk, +pb.closest("[data-pi]").dataset.pi); return; }
      const mb = e.target.closest("[data-ma]");
      if (mb) { e.preventDefault(); e.stopPropagation(); const fg = mb.closest("[data-src]"); mediaAct(mb.dataset.ma, fg.dataset.where, fg.dataset.src); return; }
      const im = e.target.closest(".pe img");
      if (im) { const fg = im.closest("[data-pi]"); picAct("zoom", fg.closest("[data-pk]").dataset.pk, +fg.dataset.pi); }
    }, {signal});
    // arrastrar y soltar en cualquier punto
    let dropEl = null;
    const isFiles = e => [...(e.dataTransfer?.types || [])].includes("Files");
    const dropMark = el => { if (dropEl === el) return; dropEl?.classList.remove("drop-on"); dropEl = el; el?.classList.add("drop-on"); };
    main.addEventListener("dragover", e => { if (!isFiles(e) || e.target.closest("#figBox")) return; e.preventDefault(); const k = keyOf(e.target); e.dataTransfer.dropEffect = k ? "copy" : "none"; dropMark(k ? elOf(k) : null); }, {signal});
    main.addEventListener("dragleave", e => { if (!e.relatedTarget || !main.contains(e.relatedTarget)) dropMark(null); }, {signal});
    main.addEventListener("drop", e => {
      if (!isFiles(e) || e.target.closest("#figBox")) return; e.preventDefault(); const k = keyOf(e.target); dropMark(null);
      if (!k) { toast("Soltala sobre una idea, un concepto, un paso del laboratorio o un párrafo de la teoría."); return; }
      addFiles([...e.dataTransfer.files], k);
    }, {signal});
    document.addEventListener("dragover", e => { if (isFiles(e)) e.preventDefault(); }, {signal});  // que soltar fuera de un destino no abra el archivo
    document.addEventListener("drop", e => { if (isFiles(e) && !main.contains(e.target)) e.preventDefault(); }, {signal});
    // menú contextual (clic derecho); Shift + clic derecho deja el del navegador
    const ctx = document.createElement("div"); ctx.className = "ctx"; ctx.hidden = true; ctx.setAttribute("role", "menu"); document.body.append(ctx);
    signal.addEventListener("abort", () => ctx.remove());
    const ctxClose = () => { ctx.hidden = true; };
    const ctxOpen = (x, y, items) => {
      ctx.innerHTML = items.map((it, i) => it === "-" ? "<hr>" : it.note ? `<p class="ctx-n">${it.note}</p>` : `<button type="button" role="menuitem" data-ci="${i}" ${it.off ? "disabled" : ""}>${it.icon ? icon(it.icon) : `<span class="ctx-i">${it.glyph || ""}</span>`}<span>${it.label}</span>${it.kbd ? `<kbd>${it.kbd}</kbd>` : ""}</button>`).join("");
      ctx.hidden = false; const w = ctx.offsetWidth, h = ctx.offsetHeight;
      ctx.style.left = Math.max(8, Math.min(x, innerWidth - w - 8)) + scrollX + "px"; ctx.style.top = Math.max(8, Math.min(y, innerHeight - h - 8)) + scrollY + "px";
      $$("[data-ci]", ctx).forEach(b => b.onclick = () => { ctxClose(); items[+b.dataset.ci].run(); });
      $("[data-ci]:not([disabled])", ctx)?.focus({preventScroll: true});
    };
    ctx.addEventListener("keydown", e => { const bs = $$("[data-ci]:not([disabled])", ctx), i = bs.indexOf(document.activeElement); if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); bs[(i + (e.key === "ArrowDown" ? 1 : -1) + bs.length) % bs.length]?.focus(); } });
    document.addEventListener("pointerdown", e => { if (!ctx.hidden && !ctx.contains(e.target)) ctxClose(); }, {capture: true, signal});
    document.addEventListener("keydown", e => { if (e.key === "Escape") ctxClose(); }, {signal});
    window.addEventListener("scroll", ctxClose, {passive: true, signal});
    main.addEventListener("contextmenu", e => {
      if (e.shiftKey) return;
      const t = e.target, key = keyOf(t);
      const media = t.closest("#labPrev [data-src], #thPrev [data-src]"), pic = t.closest(".pics-ed [data-pi]");
      if (!key && !media && !pic) return;
      e.preventDefault();
      const editable = t.closest(".ie, textarea"), sel = getSelection().toString(), items = [];
      if (pic) {
        const k = pic.closest("[data-pk]").dataset.pk, i = +pic.dataset.pi, n = ptArr(k)?.length || 0;
        items.push({note: "Esta foto"}, {icon: "image", label: "Ver grande", run: () => picAct("zoom", k, i)}, {glyph: "✎", label: "Editar el pie", run: () => picAct("cap", k, i)}, {icon: "upload", label: "Reemplazar por otra…", run: () => picAct("rep", k, i)},
          {glyph: "↑", label: "Mover antes", off: i === 0, run: () => picAct("up", k, i)}, {glyph: "↓", label: "Mover después", off: i >= n - 1, run: () => picAct("dn", k, i)}, {icon: "trash", label: "Quitar la foto", run: () => picAct("del", k, i)}, "-");
      } else if (media) {
        const w = media.dataset.where, s = media.dataset.src, img = !!media.querySelector("img");
        items.push({note: img ? "Esta imagen" : "Este video"});
        if (img) items.push({icon: "image", label: "Ver grande", run: () => mediaAct("zoom", w, s)}, {glyph: "✎", label: "Editar el pie", run: () => mediaAct("cap", w, s)}, {icon: "upload", label: "Reemplazar por otra…", run: () => mediaAct("rep", w, s)});
        items.push({icon: "trash", label: img ? "Quitar la imagen" : "Quitar el video", run: () => mediaAct("del", w, s)}, "-");
      }
      if (sel && editable) items.push({glyph: "⧉", label: "Copiar", kbd: "Ctrl+C", run: () => document.execCommand("copy")});
      if (key) {
        items.push({note: `Agregar en ${WHERE(key)}`},
          {icon: "clip", label: editable ? "Pegar (imagen o texto)" : "Pegar la imagen copiada", kbd: "Ctrl+V", run: () => act("paste", key, editable)},
          {icon: "upload", label: MD_KEY(key) ? "Subir imagen, GIF o video…" : "Subir imagen o GIF…", run: () => act("file", key)},
          {glyph: "GIF", label: "Armar un GIF con capturas…", run: () => act("gif", key)});
        if (MD_KEY(key)) items.push({glyph: "▶", label: "Video de YouTube o Vimeo…", run: () => act("video", key)});
        if (key === "fig" && l.fig) items.push("-", {icon: "trash", label: "Quitar la ilustración principal", run: () => $("#figX")?.click()});
      }
      items.push("-", {note: "Menú del navegador: Shift + clic derecho"});
      if (key) setTarget(key);
      ctxOpen(e.clientX, e.clientY, items);
    }, {signal});
    // pegar con Ctrl+V en el punto elegido
    const onPaste = e => {
      if (e.defaultPrevented) return;
      const fs = [...(e.clipboardData?.items || [])].filter(i => i.kind === "file" && MEDIA_OK.test(i.type)).map(i => i.getAsFile()).filter(Boolean);
      if (!fs.length) return;
      e.preventDefault(); const k = keyOf(document.activeElement) || target; k === "fig" ? setFig(fs[0]) : addFiles(fs, k);
    };
    document.addEventListener("paste", onPaste, {signal});
    // teoría
    const th = $("#thMd");
    const thPrev = () => {
      $("#thPrev").innerHTML = thBlocks(th.value).map((b, i) => `<div class="th-b${target === `t${i}` ? " ptarget" : ""}" data-pt="t${i}">${ptTools()}${mdBlock(m, b)}</div>`).join("");
      mediaTools($("#thPrev"), "theory");
    };
    const thGrow = () => { th.style.height = "auto"; th.style.height = Math.max(360, th.scrollHeight + 4) + "px"; };
    th.addEventListener("input", () => { l.theory_md = th.value; mark(); thPrev(); thGrow(); });
    const thInsert = txt => { const a = th.selectionStart ?? th.value.length, b = th.selectionEnd ?? a; th.value = th.value.slice(0, a) + txt + th.value.slice(b); th.dispatchEvent(new Event("input")); };
    thPrev(); $(".tab[data-tab=teoria]").addEventListener("click", () => setTimeout(thGrow, 0));
    const insert = (txt, sel = 0) => { const a = ta.selectionStart ?? ta.value.length, b = ta.selectionEnd ?? a; ta.value = ta.value.slice(0, a) + txt + ta.value.slice(b); ta.selectionStart = ta.selectionEnd = a + txt.length - sel; ta.dispatchEvent(new Event("input")); ta.focus(); };
    $$("[data-wrap]").forEach(b => b.onclick = () => { const a = ta.selectionStart, z = ta.selectionEnd; const t = ta.value.slice(a, z) || "comando"; insert("`" + t + "`"); });
    $$("[data-block]").forEach(b => b.onclick = () => b.dataset.block === "warn" ? insert("\n⚠️ ") : insert("\n```routeros\n\n```\n", 5));
    $("#insF").onchange = e => { const fs = [...e.target.files]; e.target.value = ""; addFiles(fs, "lab"); };
    $("#insGif").onclick = () => act("gif", "lab");
    $("#insY").onclick = () => act("video", "lab");
    // script para automatizar
    const au = () => (l.auto = l.auto || {titulo: "", descripcion: "", variables: [], codigo: "", notas: []});
    const paintV = () => { const a = au(); $("#auV").innerHTML = a.variables.map((v, i) => `<div class="src-ed2"><input data-vi="${i}" data-f="nombre" value="${esc(v.nombre)}" placeholder="NOMBRE" spellcheck="false"><input data-vi="${i}" data-f="valor" value="${esc(v.valor)}" placeholder="Valor por defecto"><input data-vi="${i}" data-f="detalle" value="${esc(v.detalle || "")}" placeholder="Qué es"><button class="mini del" type="button" data-vdel="${i}">×</button></div>`).join("");
      $$("#auV input").forEach(inp => inp.oninput = () => { a.variables[+inp.dataset.vi][inp.dataset.f] = inp.dataset.f === "nombre" ? inp.value.toUpperCase().replace(/[^A-Z0-9_]/g, "_") : inp.value; mark(); });
      $$("[data-vdel]").forEach(b => b.onclick = () => { a.variables.splice(+b.dataset.vdel, 1); mark(); paintV(); }); };
    paintV(); $("#auAdd").onclick = () => { au().variables.push({nombre: "", valor: "", detalle: ""}); paintV(); };
    $("#auT").oninput = e => { au().titulo = e.target.value; mark(); }; $("#auD").oninput = e => { au().descripcion = e.target.value; mark(); };
    $("#auC").oninput = e => { au().codigo = e.target.value; mark(); }; $("#auN").oninput = e => { au().notas = e.target.value.split("\n").map(x => x.trim()).filter(Boolean); mark(); };
    // examen
    const paintQ = () => {
      $("#qz").innerHTML = l.quiz.map(qEd).join("") || `<p class="note">Sin preguntas todavía.</p>`;
      $$("#qz .q").forEach(box => { const q = l.quiz[+box.dataset.qi]; q.options = q.options || [];
        bind($(".q-q", box), v => q.q = v); bind($(".q-why", box), v => q.why = v);
        $$(".o-t", box).forEach((el, j) => bind(el, v => { q.options[j] = v; }));
        $$("input[type=radio]", box).forEach(r => r.onchange = () => { q.answer = +r.value; mark(); $$(".opt", box).forEach((o, j) => o.classList.toggle("right", j === q.answer)); }); });
      $$("[data-delq]").forEach(b => b.onclick = () => { if (!b.dataset.armed) { b.dataset.armed = 1; b.textContent = "¿Quitar?"; return; } l.quiz.splice(+b.dataset.delq, 1); mark(); paintQ(); });
    };
    paintQ();
    $("#addQ").onclick = () => { l.quiz.push({q: "", options: ["", "", "", ""], answer: 0, why: ""}); mark(); paintQ(); };
    // fuentes
    const paintS = () => {
      $("#srcs").innerHTML = l.sources.map((x, i) => `<div class="src-ed2"><input data-si="${i}" data-f="label" value="${esc(x.label)}" placeholder="Qué es (ej. Manual oficial, capítulo Firewall)"><input data-si="${i}" data-f="url" value="${esc(x.url)}" placeholder="https://…"><button class="mini del" type="button" data-dels="${i}">Quitar</button></div>`).join("") || `<p class="note">Sin fuentes.</p>`;
      $$("#srcs input").forEach(inp => inp.oninput = () => { l.sources[+inp.dataset.si][inp.dataset.f] = inp.value; mark(); });
      $$("[data-dels]").forEach(b => b.onclick = () => { l.sources.splice(+b.dataset.dels, 1); mark(); paintS(); });
    };
    paintS();
    $("#addS").onclick = () => { l.sources.push({label: "", url: ""}); mark(); paintS(); };
  }
  async function uploadInline(slug, l, file, onp) {
    const f = await shrink(file);
    if (f.size > LIMIT(f.type) * 1024 * 1024) throw new Error(`El archivo pesa más de ${LIMIT(f.type)} MB.`);
    const fd = new FormData(); fd.append("curso", slug); fd.append("leccion", lid(l)); fd.append("inline", "1"); fd.append("imagen", f, f.name || "medio");
    return sendFile(fd, onp || (() => {}));
  }

  async function viewCourseEdit(slug) {
    if (!session.staff()) { location.hash = `#/curso/${slug}`; return; }
    removeBars();
    const d = await loadDraft(slug); const c = d.course;
    c.outcomes = c.outcomes || []; c.prerequisites = c.prerequisites || []; c.arcs = c.arcs || [];
    c.arcs.forEach(a => { a.objetivos = a.objetivos || []; });
    const y = scrollY;
    const order = () => { const ids = []; c.arcs.forEach(a => ids.push(...a.lessons)); c.lessons.forEach(l => { if (!ids.includes(lid(l))) ids.push(lid(l)); }); c.lessons.sort((p, q) => ids.indexOf(lid(p)) - ids.indexOf(lid(q))); c.lessons.forEach((l, i) => l.n = i + 1); };
    const orphans = c.lessons.filter(l => !c.arcs.some(a => a.lessons.includes(lid(l))));
    const lrow = (x, ai, li, len) => `<li class="lrow ed" data-l="${esc(lid(x))}"><span class="lt"><small>${String(c.lessons.indexOf(x) + 1).padStart(2, "0")}</small></span>${ie(x.handle, "Nombre de la lección", "l-h", "span")}
      <span class="row l-tools"><button class="mini" type="button" data-up="${esc(lid(x))}" ${li === 0 ? "disabled" : ""} aria-label="Subir">↑</button><button class="mini" type="button" data-dn="${esc(lid(x))}" ${li === len - 1 ? "disabled" : ""} aria-label="Bajar">↓</button>
      <select data-mv="${esc(lid(x))}" aria-label="Mover a otra parte">${c.arcs.map((a, j) => `<option value="${j}" ${j === ai ? "selected" : ""}>Módulo ${j + 1}</option>`).join("")}<option value="-1" ${ai < 0 ? "selected" : ""}>Sin módulo</option></select>
      <a class="mini" href="#/curso/${slug}/${c.lessons.indexOf(x) + 1}/editar">Editar</a></span></li>`;
    main.innerHTML = `
      <section class="c-band">${shape("rgba(23,168,212,.55)", 6)}<div class="wrap c-band-in edit-band"><div>
        <div class="row"><span class="pill warn">Editando el curso</span><a class="btn light sm" href="#/admin/cursos/${slug}">Logo e historial</a></div>
        <div class="c-title">${c.logo ? `<span class="logo-tile sm"><img src="${esc(c.logo)}" alt=""></span>` : ""}${ie(c.title, "Título del curso", "h1 dark", "h1")}</div>
        ${ie(c.tagline, "Una frase con gancho", "tag dark", "p")}
        <div class="c-facts">${ie(c.level, "Nivel", "pill-ed dark", "span")}<span>${icon("book")}${c.lessons.length} lecciones</span><span>${icon("doc")}${c.sources_count || "?"} fuentes</span></div>
      </div><div></div></div></section>
      <div class="wrap c-layout edit-mode">
        <div>
          <section class="card learn"><h2>La ruta del curso</h2>
            <p class="sub">Objetivo del curso</p>${ie(c.objetivo, "Qué vas a poder hacer al terminar todo el curso (una oración)", "p c-obj", "p")}
            <p class="sub">El recorrido</p>${ie(c.recorrido, "El hilo del curso de punta a punta, en 2 o 3 oraciones", "p c-rec", "p")}
            <label class="check"><input type="checkbox" id="seqC" ${c.secuencial !== false ? "checked" : ""}> Avance secuencial: cada lección se habilita al completar la anterior (el equipo de IES ve todo)</label></section>
          <section class="card learn"><h2>Qué vas a aprender</h2><ul id="outs"></ul><button class="mini" type="button" id="addO">+ Agregar</button></section>
          <section class="block"><div class="sec-h"><div><h2>Módulos y lecciones</h2><p class="sub">Cambiá nombres tocándolos. Ordená con las flechas o mové una lección de módulo con el selector.</p></div>
            <div class="row"><button class="btn ghost sm" type="button" id="addArc">${icon("plus")}Agregar módulo</button><button class="btn sm" type="button" id="addL">${icon("plus")}Agregar lección</button></div></div>
            ${c.arcs.map((a, ai) => { const ls = a.lessons.map(id => c.lessons.find(x => lid(x) === id)).filter(Boolean); return `<div class="acc open ed-arc" data-ai="${ai}"><div class="ed-arc-h"><div class="row arc-top"><span class="k">Módulo ${ai + 1}</span><span class="row"><button class="mini" type="button" data-aup="${ai}" ${ai === 0 ? "disabled" : ""} aria-label="Subir módulo">↑</button><button class="mini" type="button" data-adn="${ai}" ${ai === c.arcs.length - 1 ? "disabled" : ""} aria-label="Bajar módulo">↓</button>${ls.length ? "" : `<button class="mini del" type="button" data-adel="${ai}">Quitar módulo</button>`}</span></div>
              ${ie(a.title, "Nombre del módulo", "arc-t", "h3")}${ie(a.why, "Por qué este módulo va acá (opcional)", "why", "p")}
              <ul class="aobj" data-ai="${ai}"></ul><button class="mini" type="button" data-addobj="${ai}">+ Objetivo del módulo</button></div>
              <ol class="lrows">${ls.map((x, li) => lrow(x, ai, li, ls.length)).join("") || '<li class="note">Módulo vacío: mové lecciones con el selector "Parte".</li>'}</ol></div>`; }).join("")}
            ${orphans.length ? `<div class="acc open ed-arc"><div class="ed-arc-h"><span class="k">Sin módulo</span></div><ol class="lrows">${orphans.map((x, li) => lrow(x, -1, li, orphans.length)).join("")}</ol></div>` : ""}
          </section>
          <section class="block"><h2>Requisitos</h2><ul class="reqs" id="reqs"></ul><button class="mini" type="button" id="addR">+ Agregar</button></section>
          <section class="block desc"><h2>Descripción</h2>${ie(c.description, "2 o 3 oraciones: qué vas a poder hacer al terminar", "p", "p")}
            <p><b>Para quién es:</b></p>${ie(c.audience, "Para quién es, una línea", "p aud", "p")}<p><b>Versiones:</b></p>${ie(c.version_note, "Versiones de firmware o software a las que aplica", "p ver", "p")}</section>
        </div>
        <aside class="card buy">${cover(c, true)}<div class="buy-b"><label class="check"><input type="checkbox" id="draftC" ${c.draft ? "checked" : ""}> Borrador: no aparece en el catálogo</label><p class="note">Nada se publica hasta que tocás Guardar cambios. Cada guardado queda en el historial del curso.</p></div></aside>
      </div>`;
    document.title = `Editar: ${c.title} · IES Training`;
    scrollTo(0, y);
    const mark = editBar(slug, d, async () => { order(); await saveDraft(slug); forgetCourses(); catalog = null; toast("Curso guardado"); location.hash = `#/curso/${slug}`; }, `#/curso/${slug}`);
    const redraw = () => { d.dirty = true; order(); viewCourseEdit(slug); };
    const bind = (el, fn) => el.addEventListener("input", () => { fn(ieText(el)); mark(); });
    bind($(".c-title .ie"), v => c.title = v); bind($(".tag"), v => c.tagline = v); bind($(".pill-ed"), v => c.level = v);
    bind($(".c-obj"), v => c.objetivo = v); bind($(".c-rec"), v => c.recorrido = v);
    bind($(".desc > .ie"), v => c.description = v); bind($(".aud"), v => c.audience = v); bind($(".ver"), v => c.version_note = v);
    $("#seqC").onchange = e => { c.secuencial = e.target.checked; mark(); };
    $$(".ed-arc[data-ai]").forEach(box => { const a = c.arcs[+box.dataset.ai]; bind($(".arc-t", box), v => a.title = v); bind($(".why", box), v => a.why = v); });
    $$(".lrow.ed").forEach(row => { const x = c.lessons.find(y => lid(y) === row.dataset.l); bind($(".l-h", row), v => x.handle = v); });
    const where = id => c.arcs.findIndex(a => a.lessons.includes(id));
    $$("[data-up],[data-dn]").forEach(btn => btn.onclick = () => { const id = btn.dataset.up || btn.dataset.dn, ai = where(id); if (ai < 0) return; const ls = c.arcs[ai].lessons, i = ls.indexOf(id), j = i + (btn.dataset.up ? -1 : 1); [ls[i], ls[j]] = [ls[j], ls[i]]; redraw(); });
    $$("[data-mv]").forEach(sel => sel.onchange = () => { const id = sel.dataset.mv; c.arcs.forEach(a => { a.lessons = a.lessons.filter(z => z !== id); }); if (+sel.value >= 0) c.arcs[+sel.value].lessons.push(id); redraw(); });
    $$("[data-aup],[data-adn]").forEach(btn => btn.onclick = () => { const i = +(btn.dataset.aup ?? btn.dataset.adn), j = i + (btn.dataset.aup !== undefined ? -1 : 1); [c.arcs[i], c.arcs[j]] = [c.arcs[j], c.arcs[i]]; redraw(); });
    $$("[data-adel]").forEach(btn => btn.onclick = () => { c.arcs.splice(+btn.dataset.adel, 1); redraw(); });
    $("#addArc").onclick = () => { c.arcs.push({title: `Módulo ${c.arcs.length + 1}`, why: "", lessons: [], objetivos: []}); redraw(); setTimeout(() => { const t = $$(".arc-t").pop(); t?.scrollIntoView({block: "center"}); t?.focus(); }, 50); };
    $("#addL").onclick = () => { const id = Math.random().toString(36).slice(2, 10); c.lessons.push({id, n: c.lessons.length + 1, handle: "Lección nueva", summary: "", idea_md: ["", "", ""], idea: [], impact_md: "", who_md: "", lab: {energy: "Rápido", minutes: 10, md: ""}, rule: "", quiz: [], sources: [], script: []}); if (!c.arcs.length) c.arcs.push({title: "Módulo 1", why: "", lessons: [], objetivos: []}); c.arcs[c.arcs.length - 1].lessons.push(id); order(); d.dirty = true; location.hash = `#/curso/${slug}/${c.lessons.length}/editar`; };
    $$(".aobj").forEach(ul => { const a = c.arcs[+ul.dataset.ai]; const paint = () => { ul.innerHTML = a.objetivos.map((o, i) => `<li>${ie(o, "Al terminar el módulo vas a poder…", "", "span")}<button class="mini del" type="button" data-i="${i}" aria-label="Quitar">×</button></li>`).join(""); $$(".ie", ul).forEach((el, i) => bind(el, v => a.objetivos[i] = v)); $$("[data-i]", ul).forEach(b => b.onclick = () => { a.objetivos.splice(+b.dataset.i, 1); mark(); paint(); }); }; paint(); });
    $$("[data-addobj]").forEach(btn => btn.onclick = () => { const a = c.arcs[+btn.dataset.addobj]; a.objetivos.push(""); mark(); viewCourseEdit(slug); });
    const list = (sel, arr, ph, btn) => {
      const paint = () => { $(sel).innerHTML = arr.map((x, i) => `<li>${sel === "#outs" ? icon("check") : ""}${ie(x, ph, "", "span")}<button class="mini del" type="button" data-i="${i}" aria-label="Quitar">×</button></li>`).join("");
        $$(`${sel} .ie`).forEach((el, i) => bind(el, v => arr[i] = v)); $$(`${sel} [data-i]`).forEach(b => b.onclick = () => { arr.splice(+b.dataset.i, 1); mark(); paint(); }); };
      paint(); $(btn).onclick = () => { arr.push(""); paint(); $$(`${sel} .ie`).pop().focus(); };
    };
    list("#outs", c.outcomes, "Algo concreto que el técnico va a saber hacer", "#addO");
    list("#reqs", c.prerequisites, "Un requisito", "#addR");
    $("#draftC").onchange = e => { c.draft = e.target.checked; mark(); };
  }


  /* ---------- mi aprendizaje ---------- */
  async function viewLearning() {
    const list = await allCourses();
    const t = store.totals();
    const mine = list.filter(c => store.started(c.slug, c.lessons));
    const rules = list.map(c => ({c, ls: c.lessons.filter(l => store.get(c.slug, lid(l)).rule)})).filter(x => x.ls.length);
    main.innerHTML = `
      <div class="wrap">
        <div class="page-h"><span class="badge"><span class="p"></span>Mi aprendizaje</span><h1>Tu avance</h1><p>${session.user ? "Tu avance queda guardado en tu cuenta: lo ves desde cualquier equipo." : "Lo que llevás hecho en este navegador. Con una cuenta queda guardado y lo ves desde cualquier equipo."}</p>
          ${session.user ? "" : `<div class="row" style="margin-top:16px"><a class="btn" href="#/registro">Crear cuenta</a><a class="btn ghost" href="#/ingresar">Ingresar</a></div>`}
          <div class="ledger"><div><b>${t.done}</b><span>lecciones completas</span></div><div><b>${t.labs}</b><span>laboratorios hechos</span></div><div><b>${t.quizzes}</b><span>quizzes respondidos</span></div><div><b>${t.rules}</b><span>reglas en tu manual</span></div></div>
        </div>
        <section class="sec"><div class="sec-h"><div><span class="k">Cursos</span><h2>Mis cursos</h2></div></div>
          ${mine.length ? `<div class="grid">${mine.map(courseCard).join("")}</div>` : `<div class="card empty"><b>Todavía no empezaste ningún curso.</b>Elegí uno del catálogo; tu avance aparece acá.<br><a class="btn" href="#/">Ver el catálogo</a></div>`}
        </section>
        <section class="sec"><div class="sec-h"><div><span class="k">Manual de bolsillo</span><h2>Mis reglas</h2><p>Una frase por lección. Es lo que queda cuando el curso termina.</p></div>${rules.length && !framed ? `<button class="btn ghost" id="printRules">Imprimir el manual</button>` : ""}</div>
          ${rules.length ? rules.map(({c, ls}) => `<div class="card" style="padding:8px 24px 10px;margin-bottom:16px"><h3 style="font-size:19px;padding:14px 0 6px">${esc(c.title)}</h3><ul class="rules">${ls.map(l => `<li><a href="#/curso/${c.slug}/${l.n}">Lección ${l.n}</a><p>${rich(l.rule)}</p></li>`).join("")}</ul></div>`).join("")
            : `<div class="card empty"><b>Tu manual está vacío.</b>En cada lección, la regla tiene un botón “Guardar en mi manual”.</div>`}
        </section>
        <section class="sec"><button class="btn ghost" id="resetBtn">Borrar mi progreso</button></section>
      </div>`;
    $("#printRules")?.addEventListener("click", () => print());
    $("#resetBtn").addEventListener("click", e => {
      const b = e.currentTarget;
      if (b.dataset.armed) { store.reset(); viewLearning(); toast("Progreso borrado"); return; }
      b.dataset.armed = "1"; b.textContent = "Tocá de nuevo para borrar todo"; b.classList.remove("ghost");
      setTimeout(() => { if (b.isConnected) { delete b.dataset.armed; b.textContent = "Borrar mi progreso"; b.classList.add("ghost"); } }, 4000);
    });
    document.title = "Mi aprendizaje · IES Training";
  }

  /* ---------- constancia ---------- */
  async function viewCert(slug) {
    if (!session.user) { main.innerHTML = lockedPage("La constancia es para técnicos registrados", "Creá tu cuenta gratis o ingresá: tu avance queda guardado y la constancia sale con tu nombre."); return; }
    const c = await getCourse(slug);
    const done = store.courseDone(slug, c.lessons);
    if (done < c.lessons.length) {
      main.innerHTML = `<div class="wrap page-h"><div class="card empty"><b>La constancia se habilita al completar las ${c.lessons.length} lecciones.</b>Llevás ${done} de ${c.lessons.length} en ${esc(c.title)}.<br><a class="btn" href="#/curso/${slug}">Volver al curso</a></div></div>`;
      return;
    }
    const date = new Date().toLocaleDateString("es-UY", {day: "numeric", month: "long", year: "numeric"});
    main.innerHTML = `
      <div class="wrap">
        <div class="page-h noprint"><span class="badge"><span class="p"></span>Constancia</span><h1>Completaste el curso</h1><p>Escribí tu nombre como querés que figure. ${framed ? "" : "Después podés imprimirla o guardarla como PDF."}</p></div>
        <div class="cert-wrap">
          <form class="cert-form" id="certForm"><label>Nombre y apellido<input id="certName" value="${esc(store.data.name || session.user?.name || "")}" autocomplete="name" placeholder="Tu nombre"></label>${framed ? "" : `<button class="btn" type="button" id="printCert">Imprimir o guardar PDF</button>`}</form>
          <div class="cert">
            <div class="side-band">${shape("rgba(23,168,212,.6)", 8)}<img src="assets/ies-escudo-oscuro.svg" alt="IES"><p>Sistemas que tienen que funcionar a las tres de la mañana.</p></div>
            <div class="body">
              <span class="k">IES Training · Constancia de finalización</span>
              <h2>Constancia</h2>
              <div class="who" id="certWho">${esc(store.data.name || session.user?.name || "")}</div>
              <p>completó las ${c.lessons.length} lecciones del curso, con su laboratorio y su quiz:</p>
              <div class="course">${esc(c.title)}</div>
              <p>${hours(c)} de formación técnica. Montevideo, ${date}.</p>
              <div class="sig"><div><b>Ingeniería en Seguridad S.R.L.</b>IES · ies.com.uy</div><div><b>Equipo técnico IES</b>Soporte 098 437 437</div></div>
            </div>
          </div>
        </div>
      </div>`;
    $("#certName").addEventListener("input", e => { store.data.name = e.target.value; store.save(); $("#certWho").textContent = e.target.value; });
    $("#certForm").addEventListener("submit", e => e.preventDefault());
    $("#printCert")?.addEventListener("click", () => print());
    document.title = `Constancia · ${c.title} · IES Training`;
  }

  /* ---------- búsqueda ---------- */
  async function viewSearch(q) {
    const list = await allCourses();
    const norm = s => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
    const terms = norm(q).split(/\s+/).filter(Boolean);
    const strip = h => String(h || "").replace(/<[^>]+>/g, " ");
    const match = txt => terms.every(t => norm(txt).includes(t));
    const hl = s => { let out = esc(s); terms.forEach(t => { if (t.length > 1) out = out.replace(new RegExp(`(${t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`, "gi"), "<mark>$1</mark>"); }); return out; };
    const cs = list.filter(c => match([c.title, c.vendor, c.tagline, c.description].join(" ")));
    const ls = [];
    list.forEach(c => c.lessons.forEach(l => { if (match([l.handle, l.summary, (l.idea || []).join(" "), strip(l.lab?.html), l.rule, (l.concepts || []).map(k => k.name + " " + k.para_que).join(" ")].map(strip).join(" "))) ls.push({c, l}); }));
    main.innerHTML = `
      <div class="wrap results">
        <div class="page-h"><span class="k">Búsqueda</span><h1>Resultados para “${esc(q)}”</h1><p>${cs.length} cursos y ${ls.length} lecciones.${session.user ? "" : ` Sin cuenta se busca solo en los títulos: <a href="#/ingresar">ingresá</a> para buscar dentro de las lecciones.`}</p></div>
        ${cs.length ? `<h2>Cursos</h2><div class="grid">${cs.map(courseCard).join("")}</div>` : ""}
        ${ls.length ? `<h2>Lecciones</h2>${ls.slice(0, 60).map(({c, l}) => `<a class="card hit" href="#/curso/${c.slug}/${l.n}"><span><b>${hl(l.handle)}</b><small>${esc(c.title)}, lección ${l.n}${l.summary ? `: ${hl(l.summary)}` : ""}</small></span>${icon("chev", "i")}</a>`).join("")}` : ""}
        ${!cs.length && !ls.length ? `<div class="card empty"><b>No hay coincidencias.</b>Probá con otra palabra: el nombre de un equipo, un protocolo o una tarea, como “VLAN”, “backup” o “DTMF”.<br><a class="btn" href="#/">Ver todos los cursos</a></div>` : ""}
      </div>`;
    $$(".hit svg").forEach(s => { s.style.width = "18px"; s.style.color = "var(--ink-3)"; });
    document.title = `Buscar: ${q} · IES Training`;
  }


  /* ---------- modo editor y capturas ---------- */
  const API = "api/capturas.php";
  const EKEY = "iesTraining.editor";
  const editor = {
    key() { try { return localStorage.getItem(EKEY) || ""; } catch { return ""; } },
    on() { return !!this.key() || ["admin", "editor"].includes(session.user?.role); },
    headers(extra = {}) { const h = {"X-IES": "1", ...extra}; if (this.key()) h["X-Editor-Key"] = this.key(); return h; },
    set(k) { try { k ? localStorage.setItem(EKEY, k) : localStorage.removeItem(EKEY); } catch {} }
  };
  async function shrink(file) {
    if (!file.type.startsWith("image/") || file.type === "image/gif" || file.size < 1.5e6) return file;
    try {
      const bmp = await createImageBitmap(file);
      const k = Math.min(1, 2400 / bmp.width);
      if (k === 1 && file.size < 4e6) return file;
      const cv = document.createElement("canvas"); cv.width = Math.round(bmp.width * k); cv.height = Math.round(bmp.height * k);
      cv.getContext("2d").drawImage(bmp, 0, 0, cv.width, cv.height);
      const blob = await new Promise(r => cv.toBlob(r, "image/webp", 0.9));
      return blob && blob.type === "image/webp" ? new File([blob], "captura.webp", {type: "image/webp"}) : file;
    } catch { return file; }
  }
  const MEDIA_OK = /^(image\/(png|jpeg|webp|gif)|video\/(mp4|webm|quicktime))$/;
  const LIMIT = t => t === "image/gif" ? 30 : t.startsWith("video/") ? 60 : 12;
  const mtype = x => x.tipo || (/\.gif$/i.test(x.archivo || x.url || "") ? "gif" : "imagen");
  const embedSrc = x => x.proveedor === "vimeo" ? `https://player.vimeo.com/video/${encodeURIComponent(x.video)}` : `https://www.youtube-nocookie.com/embed/${encodeURIComponent(x.video)}`;
  const thumbOf = x => mtype(x) === "embed" && x.proveedor === "youtube" ? `https://i.ytimg.com/vi/${encodeURIComponent(x.video)}/hqdefault.jpg` : "";
  /* Sube con progreso; devuelve el JSON de la respuesta. */
  function sendFile(fd, onProgress) {
    return new Promise((res, rej) => {
      const xhr = new XMLHttpRequest();
      xhr.open("POST", API);
      Object.entries(editor.headers()).forEach(([k, v]) => xhr.setRequestHeader(k, v));
      xhr.upload.onprogress = e => { if (e.lengthComputable && onProgress) onProgress(Math.round(e.loaded / e.total * 100)); };
      xhr.onload = () => { let j = {}; try { j = JSON.parse(xhr.responseText); } catch {} xhr.status < 300 ? res(j) : rej(new Error(j.error || (xhr.status === 413 ? "El archivo es demasiado grande." : `Error ${xhr.status}`))); };
      xhr.onerror = () => rej(new Error("Se cortó la conexión durante la subida."));
      xhr.send(fd);
    });
  }
  const capturas = {
    cur: null, items: [],
    async mount(slug, n, pos) {
      this.cur = {slug, n, pos}; this.items = [];
      const box = $("#caps"); if (!box) return;
      try {
        const r = await fetch(`${API}?curso=${slug}&leccion=${encodeURIComponent(n)}`, {cache: "no-store"});
        if (!r.ok) throw new Error(r.status);
        this.items = (await r.json()).capturas || [];
      } catch {
        this.items = [];
        if (editor.on()) $("#capsGrid").innerHTML = `<p class="note">No se pudo leer el servicio de medios. Funciona en entrenamientos.ies.com.uy; en una vista previa sin servidor no se guardan.</p>`;
        return;
      }
      if (this.cur.slug !== slug || this.cur.n !== n) return;
      if (this.items.length) box.hidden = false;
      this.paint();
      if (editor.on()) {
        const drop = $("#drop"), inp = $("#capFile");
        drop.addEventListener("click", e => { if (!e.target.closest("input,button,form")) inp.click(); });
        drop.addEventListener("keydown", e => { if (e.target === drop && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); inp.click(); } });
        inp.addEventListener("change", () => { [...inp.files].forEach(f => this.upload(f)); inp.value = ""; });
        ["dragenter", "dragover"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add("over"); }));
        ["dragleave", "drop"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove("over"); }));
        drop.addEventListener("drop", e => [...(e.dataTransfer?.files || [])].forEach(f => this.upload(f)));
        $("#gifB").addEventListener("click", async ev => { ev.stopPropagation(); const f = await gifMaker(); if (f) this.upload(f); });
        $("#embF").addEventListener("submit", ev => { ev.preventDefault(); const u = $("#embU").value.trim(); if (!u) return; this.post({accion: "embed", url: u}, "Video agregado", true); $("#embU").value = ""; });
      }
    },
    paint() {
      const g = $("#capsGrid"); if (!g) return;
      const ed = editor.on();
      g.innerHTML = this.items.map((x, i) => {
        const t = mtype(x);
        const media = t === "video" ? `<video src="${esc(x.url)}" muted playsinline preload="metadata"></video><span class="badge-t">Video</span>`
          : t === "embed" ? `${thumbOf(x) ? `<img src="${thumbOf(x)}" alt="" loading="lazy">` : `<span class="emb-ph">${x.proveedor === "vimeo" ? "Vimeo" : "YouTube"}</span>`}<span class="badge-t">${x.proveedor === "vimeo" ? "Vimeo" : "YouTube"}</span>`
          : `<img src="${esc(x.url)}" alt="${esc(x.texto || `Captura ${i + 1}`)}" loading="lazy" width="${x.ancho || ""}" height="${x.alto || ""}">${t === "gif" ? '<span class="badge-t">GIF</span>' : ""}`;
        return `<figure class="cap" data-id="${esc(x.id)}">
          <button class="cap-img" data-i="${i}" aria-label="Ampliar ${t === "video" || t === "embed" ? "video" : "captura"} ${i + 1}">${media}${t === "video" || t === "embed" ? '<span class="play" aria-hidden="true">▶</span>' : ""}</button>
          ${ed ? `<figcaption class="cap-ed"><label class="sr" for="ct-${i}">Texto ${i + 1}</label><input id="ct-${i}" value="${esc(x.texto || "")}" placeholder="Agregá una descripción" maxlength="300" data-id="${esc(x.id)}">
            <div class="cap-tools"><button class="mini" data-mv="-1" data-id="${esc(x.id)}" aria-label="Mover antes" ${i === 0 ? "disabled" : ""}>↑</button><button class="mini" data-mv="1" data-id="${esc(x.id)}" aria-label="Mover después" ${i === this.items.length - 1 ? "disabled" : ""}>↓</button><button class="mini del" data-del="${esc(x.id)}">Quitar</button></div></figcaption>`
            : (x.texto ? `<figcaption>${esc(x.texto)}</figcaption>` : "")}
        </figure>`; }).join("") || (ed ? `<p class="note">Todavía no hay medios en esta lección.</p>` : "");
      $$(".cap-img", g).forEach(b => b.addEventListener("click", () => lightbox(this.items, +b.dataset.i)));
      if (!ed) return;
      $$(".cap-ed input", g).forEach(inp => inp.addEventListener("change", () => this.post({accion: "texto", id: inp.dataset.id, texto: inp.value}, "Texto guardado")));
      $$("[data-mv]", g).forEach(b => b.addEventListener("click", () => this.post({accion: "mover", id: b.dataset.id, dir: +b.dataset.mv}, null, true)));
      $$("[data-del]", g).forEach(b => b.addEventListener("click", () => {
        if (!b.dataset.armed) { b.dataset.armed = 1; b.textContent = "¿Quitar?"; setTimeout(() => { if (b.isConnected) { delete b.dataset.armed; b.textContent = "Quitar"; } }, 3500); return; }
        this.post({accion: "borrar", id: b.dataset.del}, "Quitado", true);
      }));
    },
    async post(body, msg, reload) {
      const {slug, n} = this.cur;
      try {
        const r = await fetch(API, {method: "POST", headers: editor.headers({"Content-Type": "application/json"}), body: JSON.stringify({...body, curso: slug, leccion: n})});
        const j = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(j.error || `Error ${r.status}`);
        if (msg) toast(msg);
        if (reload) this.mount(slug, n, this.cur.pos);
      } catch (e) { toast(e.message || "No se pudo guardar"); }
    },
    async upload(file) {
      if (!this.cur || !editor.on()) return;
      if (!MEDIA_OK.test(file.type)) { toast("Formato no admitido: imágenes PNG, JPG, WebP o GIF, y videos MP4 o WebM."); return; }
      const {slug, n} = this.cur;
      const g = $("#capsGrid"); const ph = document.createElement("div"); ph.className = "cap up"; ph.textContent = "Subiendo…"; g?.prepend(ph);
      try {
        const f = await shrink(file);
        if (f.size > LIMIT(f.type) * 1024 * 1024) throw new Error(`El archivo pesa más de ${LIMIT(f.type)} MB.`);
        const fd = new FormData(); fd.append("curso", slug); fd.append("leccion", n); fd.append("imagen", f, f.name || "captura.png");
        const j = await sendFile(fd, p => { ph.textContent = `Subiendo… ${p}%`; });
        toast(f.type.startsWith("video/") ? "Video subido" : f.type === "image/gif" ? "GIF subido" : "Captura subida");
        ph.remove();
        if (this.cur.slug === slug && this.cur.n === n) { this.items.push(j.captura); this.paint(); $("#caps").hidden = false; setTimeout(() => $(`#ct-${this.items.length - 1}`)?.focus(), 50); }
      } catch (e) { toast(e.message || "No se pudo subir"); ph.remove(); }
    }
  };
  document.addEventListener("paste", e => {
    if (!editor.on() || !capturas.cur || !location.hash.startsWith(`#/curso/${capturas.cur.slug}/${capturas.cur.pos}`)) return;
    const items = [...(e.clipboardData?.items || [])];
    const files = items.filter(i => i.kind === "file" && MEDIA_OK.test(i.type)).map(i => i.getAsFile()).filter(Boolean);
    if (!files.length) {
      // Un enlace de YouTube/Vimeo pegado fuera de un campo se agrega como video
      const txt = e.clipboardData?.getData("text") || "";
      if (!/INPUT|TEXTAREA/.test(document.activeElement?.tagName || "") && /(youtube\.com|youtu\.be|vimeo\.com)\//.test(txt)) { e.preventDefault(); capturas.post({accion: "embed", url: txt.trim()}, "Video agregado", true); }
      return;
    }
    e.preventDefault();
    const tab = $("#t-laboratorio"); if (tab && tab.getAttribute("aria-selected") !== "true") tab.click();
    files.forEach(f => capturas.upload(f));
  });
  function lightbox(items, i) {
    const ov = document.createElement("div"); ov.className = "lb"; ov.setAttribute("role", "dialog"); ov.setAttribute("aria-modal", "true"); ov.setAttribute("aria-label", "Medio ampliado");
    const draw = () => {
      const x = items[i], t = mtype(x);
      const body = t === "video" ? `<video src="${esc(x.url)}" controls autoplay playsinline></video>`
        : t === "embed" ? `<div class="lb-emb"><iframe src="${embedSrc(x)}?autoplay=1" title="${esc(x.texto || "Video")}" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>`
        : `<img src="${esc(x.url)}" alt="${esc(x.texto || "")}">`;
      ov.innerHTML = `<button class="lb-x" aria-label="Cerrar">×</button>${items.length > 1 ? `<button class="lb-p" aria-label="Anterior">‹</button><button class="lb-n" aria-label="Siguiente">›</button>` : ""}<figure>${body}${x.texto ? `<figcaption>${esc(x.texto)}</figcaption>` : ""}<span class="lb-c">${i + 1} de ${items.length}</span></figure>`;
      $(".lb-x", ov).onclick = close; if ($(".lb-p", ov)) { $(".lb-p", ov).onclick = () => { i = (i - 1 + items.length) % items.length; draw(); }; $(".lb-n", ov).onclick = () => { i = (i + 1) % items.length; draw(); }; } $(".lb-x", ov).focus(); };
    const key = e => { if (e.key === "Escape") close(); if (e.key === "ArrowRight" && items.length > 1) { i = (i + 1) % items.length; draw(); } if (e.key === "ArrowLeft" && items.length > 1) { i = (i - 1 + items.length) % items.length; draw(); } };
    const close = () => { ov.remove(); document.removeEventListener("keydown", key); };
    ov.addEventListener("click", e => { if (e.target === ov) close(); });
    document.addEventListener("keydown", key); document.body.append(ov); draw();
  }

  async function viewEditor() {
    const on = editor.on();
    main.innerHTML = `
      <div class="wrap">
        <div class="page-h"><span class="badge"><span class="p"></span>Modo editor</span><h1>${on ? "Estás en modo editor" : "Entrar en modo editor"}</h1>
          <p>${on ? "En cada lección, la pestaña Laboratorio tiene una zona para agregar capturas: pegá con Ctrl+V desde el portapapeles, arrastrá la imagen o elegí un archivo. Las capturas quedan visibles para todos." : "Con la clave de editor de IES podés agregar capturas a las lecciones. Las ven todos los que abren el curso."}</p></div>
        <div class="card empty" style="margin-top:24px">
          ${on ? `<b>Clave guardada en este navegador.</b>Para cargar capturas desde otra computadora, entrá con la clave también ahí.<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="#/">Ir a los cursos</a><button class="btn ghost" id="edOff">Salir del modo editor</button></div>`
            : `<form id="edForm" class="cert-form"><label>Clave de editor<input id="edKey" type="password" autocomplete="current-password" required></label><button class="btn">Entrar</button></form><p class="note" id="edMsg"></p>`}
        </div>
      </div>`;
    $("#edOff")?.addEventListener("click", () => { editor.set(""); toast("Saliste del modo editor"); viewEditor(); });
    $("#edForm")?.addEventListener("submit", async e => {
      e.preventDefault(); const k = $("#edKey").value.trim(); const msg = $("#edMsg");
      msg.textContent = "Verificando…";
      try {
        const r = await fetch(`${API}?verificar=1`, {headers: {"X-Editor-Key": k}, cache: "no-store"});
        if (r.status === 403) { msg.textContent = "La clave no es correcta. Revisala y probá de nuevo."; return; }
        if (!r.ok) throw new Error();
        editor.set(k); toast("Modo editor activado"); viewEditor();
      } catch { msg.textContent = "No se pudo contactar el servicio de capturas. Funciona en training.ies.com.uy."; }
    });
    document.title = "Modo editor · IES Training";
  }


  /* ---------- cuentas, sincronización y administración ---------- */
  async function api(path, body, method) {
    const opt = {method: method || (body !== undefined ? "POST" : "GET"), headers: {"X-IES": "1"}, cache: "no-store", credentials: "same-origin"};
    if (body !== undefined) { opt.headers["Content-Type"] = "application/json"; opt.body = JSON.stringify(body); }
    let r;
    try { r = await fetch(path, opt); } catch { throw new Error("No hay conexión con el servidor. Probá de nuevo en un momento."); }
    const j = await r.json().catch(() => ({}));
    if (!r.ok) { const e = new Error(j.error || `Error ${r.status}`); e.status = r.status; throw e; }
    return j;
  }
  const session = {
    user: null, ready: false,
    async load() {
      try { this.user = (await api("api/auth.php?a=me")).user; } catch { this.user = null; }
      this.ready = true; paintHeader();
      if (this.user) await sync.pull();
    },
    set(u) { this.user = u; forgetCourses(); paintHeader(); },
    staff() { return ["admin", "editor"].includes(this.user?.role); }
  };
  const sync = {
    pending: new Set(), t: null,
    queue(k) { if (!session.user) return; this.pending.add(k); clearTimeout(this.t); this.t = setTimeout(() => this.push(), 800); },
    async push() {
      if (!session.user || !this.pending.size) return;
      const l = {}; this.pending.forEach(k => { l[k] = store.data.l[k] || {}; }); this.pending.clear();
      try { await api("api/progress.php", {l, replace: true, name: store.data.name || undefined}); } catch {}
    },
    async pull() {
      try {
        const srv = (await api("api/progress.php")).progress || {l: {}};
        const loc = store.data.l;
        for (const [k, v] of Object.entries(srv.l || {})) {
          const a = loc[k] || {};
          const m = {...a};
          ["seen", "lab", "done", "rule"].forEach(f => { if (v[f] || a[f]) m[f] = true; });
          const qa = a.quiz || {}, qb = v.quiz || {};
          if (qb.done || (qb.a || []).length > (qa.a || []).length) m.quiz = qb;
          loc[k] = m;
        }
        if (!store.data.name && session.user) store.data.name = srv.name || session.user.name;
        store.save();
        await api("api/progress.php", {l: loc, replace: false});
      } catch {}
    }
  };
  const _set = store.set.bind(store);
  store.set = (slug, k, patch) => { _set(slug, k, patch); sync.queue(`${slug}/${k}`); };
  const _reset = store.reset.bind(store);
  store.reset = () => { _reset(); if (session.user) api("api/progress.php", {l: {}, clear: true}).catch(() => {}); };

  function paintHeader() {
    const nav = $(".nav"); if (!nav) return;
    const u = session.user;
    $$(".nav [data-acc]").forEach(x => x.remove());
    const cur = location.hash;
    if (session.staff()) nav.insertAdjacentHTML("beforeend", `<a data-acc href="#/admin" data-nav="admin" ${cur.startsWith("#/admin") ? 'aria-current="page"' : ""}><span class="lg">Administración</span><span class="sh">Admin</span></a>`);
    if (u) nav.insertAdjacentHTML("beforeend", `<a data-acc class="who" href="#/cuenta" title="${esc(u.email)}"><span class="av" aria-hidden="true">${esc(u.name.trim().split(/\s+/).map(x => x[0]).slice(0, 2).join("").toUpperCase())}</span><span class="nm">${esc(u.name.split(" ")[0])}</span></a>`);
    else nav.insertAdjacentHTML("beforeend", `<a data-acc class="btn sm" href="#/ingresar">Ingresar</a>`);
  }
  const back = () => { let to = "#/"; try { to = sessionStorage.getItem("ies.back") || "#/"; sessionStorage.removeItem("ies.back"); } catch {} location.hash = to; };

  function authShell(title, sub, inner) {
    return `<div class="wrap auth"><div class="card auth-card"><img src="assets/ies-escudo-claro.svg" alt="" width="58" height="46"><h1>${title}</h1><p class="sub">${sub}</p>${inner}</div></div>`;
  }
  async function viewLogin() {
    if (session.user) return back();
    main.innerHTML = authShell("Ingresar", "Con tu cuenta, tu avance y tus constancias quedan guardados y los ves desde cualquier equipo.", `
      <form id="lf" class="form" novalidate>
        <label>Correo<input id="le" type="email" autocomplete="email" required></label>
        <label>Contraseña<input id="lp" type="password" autocomplete="current-password" required></label>
        <p class="err" id="lerr" role="alert"></p>
        <button class="btn wide">Ingresar</button>
      </form>
      <p class="alt">¿No tenés cuenta? <a href="#/registro">Registrate</a>. Si olvidaste la contraseña, pedile a IES que la reinicie.</p>`);
    $("#le").focus();
    $("#lf").addEventListener("submit", async e => {
      e.preventDefault(); const b = $("#lf .btn"); b.disabled = true; $("#lerr").textContent = "";
      try {
        const {user} = await api("api/auth.php?a=login", {email: $("#le").value, password: $("#lp").value});
        session.set(user); await sync.pull(); toast(`Hola, ${user.name.split(" ")[0]}`);
        if (user.must_change) location.hash = "#/cuenta"; else back();
      } catch (err) { $("#lerr").textContent = err.message; b.disabled = false; }
    });
    document.title = "Ingresar · IES Training";
  }
  async function viewRegister() {
    if (session.user) return back();
    main.innerHTML = authShell("Crear cuenta", "Para técnicos de IES y de empresas que trabajan con IES. Es gratis.", `
      <form id="rf" class="form" novalidate>
        <label>Nombre y apellido<input id="rn" autocomplete="name" required></label>
        <label>Correo<input id="re" type="email" autocomplete="email" required></label>
        <label>Empresa <span class="opt-l">(opcional)</span><input id="rc" autocomplete="organization"></label>
        <label>Contraseña<input id="rp" type="password" autocomplete="new-password" minlength="8" required><small>Al menos 8 caracteres.</small></label>
        <p class="err" id="rerr" role="alert"></p>
        <button class="btn wide">Crear cuenta</button>
      </form>
      <p class="alt">¿Ya tenés cuenta? <a href="#/ingresar">Ingresá</a>.</p>`);
    $("#rn").focus();
    $("#rf").addEventListener("submit", async e => {
      e.preventDefault(); const b = $("#rf .btn"); b.disabled = true; $("#rerr").textContent = "";
      try {
        const {user} = await api("api/auth.php?a=register", {name: $("#rn").value, email: $("#re").value, company: $("#rc").value, password: $("#rp").value});
        session.set(user); await sync.pull(); toast("Cuenta creada"); back();
      } catch (err) { $("#rerr").textContent = err.message; b.disabled = false; }
    });
    document.title = "Crear cuenta · IES Training";
  }
  async function viewAccount() {
    const u = session.user;
    if (!u) { location.hash = "#/ingresar"; return; }
    main.innerHTML = `<div class="wrap"><div class="page-h"><span class="badge"><span class="p"></span>Mi cuenta</span><h1>${esc(u.name)}</h1><p>${esc(u.email)}${u.company ? `, ${esc(u.company)}` : ""}. Rol: ${({admin: "administrador", editor: "editor", tecnico: "técnico"})[u.role]}.</p></div>
      ${u.must_change ? `<div class="card notice"><b>Elegí una contraseña nueva.</b> Entraste con una contraseña temporal.</div>` : ""}
      <div class="acc-grid">
        <form class="card form pad" id="pf"><h2>Datos</h2>
          <label>Nombre y apellido<input id="pn" value="${esc(u.name)}" required></label>
          <label>Empresa<input id="pc" value="${esc(u.company || "")}"></label>
          <p class="err" id="perr" role="alert"></p><button class="btn">Guardar datos</button></form>
        <form class="card form pad" id="cf"><h2>Contraseña</h2>
          ${u.must_change ? "" : `<label>Contraseña actual<input id="cc" type="password" autocomplete="current-password"></label>`}
          <label>Contraseña nueva<input id="cn" type="password" autocomplete="new-password" minlength="8"><small>Al menos 8 caracteres.</small></label>
          <p class="err" id="cerr" role="alert"></p><button class="btn">Cambiar contraseña</button></form>
      </div>
      <section class="sec"><button class="btn ghost" id="out">Salir de la cuenta</button></section></div>`;
    $("#pf").addEventListener("submit", async e => { e.preventDefault(); try { const {user} = await api("api/auth.php?a=profile", {name: $("#pn").value, company: $("#pc").value}); session.set(user); toast("Datos guardados"); viewAccount(); } catch (err) { $("#perr").textContent = err.message; } });
    $("#cf").addEventListener("submit", async e => { e.preventDefault(); try { await api("api/auth.php?a=password", {current: $("#cc")?.value || "", new: $("#cn").value}); session.user.must_change = false; toast("Contraseña cambiada"); viewAccount(); } catch (err) { $("#cerr").textContent = err.message; } });
    $("#out").addEventListener("click", async () => { await api("api/auth.php?a=logout", {}).catch(() => {}); session.set(null); toast("Saliste de tu cuenta"); location.hash = "#/"; });
    document.title = "Mi cuenta · IES Training";
  }

  /* ---------- administración ---------- */
  const fmtDate = s => s ? new Date(s).toLocaleString("es-UY", {day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit"}) : "nunca";
  const ago = s => { if (!s) return "nunca"; const d = (Date.now() - new Date(s)) / 1000; if (d < 3600) return `hace ${Math.max(1, Math.round(d / 60))} min`; if (d < 86400) return `hace ${Math.round(d / 3600)} h`; if (d < 86400 * 30) return `hace ${Math.round(d / 86400)} días`; return fmtDate(s); };
  const ROLE = {admin: "Administrador", editor: "Editor", tecnico: "Técnico"};
  /* ---------- administración: armazón ---------- */
  const ADM_NAV = [["", "Resumen", "grid"], ["usuarios", "Usuarios", "users"], ["cursos", "Cursos", "book"], ["actividad", "Actividad", "pulse"]];
  const initials = n => String(n || "?").trim().split(/\s+/).map(x => x[0]).slice(0, 2).join("").toUpperCase();
  const AV_TONES = ["#002F58", "#0A63B8", "#0B6E8E", "#3A5675", "#1F4E79", "#00639A"];
  const avatar = (u, cls = "") => { let h = 0; for (const ch of String(u.email || u.name || "")) h = (h * 31 + ch.charCodeAt(0)) >>> 0; return `<span class="adm-av ${cls}" style="background:${AV_TONES[h % AV_TONES.length]}" aria-hidden="true">${esc(initials(u.name))}</span>`; };
  const fmtN = n => Number(n || 0).toLocaleString("es-UY");
  const dayLabel = d => new Date(d + "T12:00:00").toLocaleDateString("es-UY", {day: "numeric", month: "short"});
  const recent = (s, days) => s && (Date.now() - new Date(s)) < days * 86400000;
  function adminShell(tab, inner) {
    const isAdmin = session.user.role === "admin";
    const items = ADM_NAV.filter(t => isAdmin || t[0] === "cursos");
    const u = session.user;
    return `<div class="adm">
      <aside class="adm-side" aria-label="Administración">
        <div class="adm-brand"><span class="k">Administración</span><b>IES Training</b></div>
        <nav class="adm-nav">${items.map(([k, t, ic]) => `<a href="#/admin${k ? "/" + k : ""}" ${tab === k ? 'aria-current="page"' : ""}>${icon(ic)}<span>${t}</span></a>`).join("")}</nav>
        <div class="adm-side-foot">
          <a class="adm-site" href="#/">${icon("eye")}<span>Ver el portal</span></a>
          <a class="adm-me" href="#/cuenta">${avatar(u)}<span><b>${esc(u.name)}</b><small>${ROLE[u.role]}</small></span></a>
        </div>
      </aside>
      <div class="adm-main">${inner}</div></div>`;
  }
  const admHead = (kicker, title, sub = "", actions = "") => `<header class="adm-head"><div>${kicker ? `<span class="k">${kicker}</span>` : ""}<h1>${title}</h1>${sub ? `<p>${sub}</p>` : ""}</div>${actions ? `<div class="adm-actions">${actions}</div>` : ""}</header>`;
  const kpi = (ic, value, label, foot = "", tone = "") => `<div class="kpi ${tone}"><span class="kpi-ic">${icon(ic)}</span><b>${value}</b><span class="kpi-l">${label}</span>${foot ? `<small>${foot}</small>` : ""}</div>`;
  const meter = (v, max = 100, cls = "") => `<span class="meter ${cls}" role="img" aria-label="${pct(v, max)}%"><i style="width:${Math.min(100, pct(v, max))}%"></i></span>`;
  const courseMark = c => c.logo ? `<span class="cmark logo"><img src="${esc(c.logo)}" alt="" loading="lazy"></span>` : `<span class="cmark">${icon((META[c.slug] || {}).glyph || "doc")}</span>`;
  const ACT = {ingreso: ["login", "Ingresó"], registro: ["userplus", "Se registró"], "cambio de contraseña": ["key", "Cambió su contraseña"], "curso guardado": ["edit", "Guardó un curso"], "curso creado": ["plus", "Creó un curso"],
    "curso importado": ["upload", "Importó un curso"], "versión restaurada": ["history", "Restauró una versión"], "orden del catálogo": ["sort", "Reordenó el catálogo"], "usuario modificado": ["users", "Modificó un usuario"],
    "contraseña reiniciada": ["key", "Reinició una contraseña"], "usuario creado": ["userplus", "Creó un usuario"], "logo cargado": ["image", "Cargó un logo"], "logo quitado": ["image", "Quitó un logo"], "admin creado por consola": ["userplus", "Creó un administrador por consola"]};
  const actGroup = a => /ingreso|contraseña$/.test(a) && !/reiniciada/.test(a) ? "ingresos" : /registro|usuario|reiniciada/.test(a) ? "usuarios" : /curso|versión|catálogo|logo/.test(a) ? "cursos" : "otros";
  const actRow = x => { const [ic, t] = ACT[x.action] || ["dot", x.action]; return `<li class="feed-i g-${actGroup(x.action)}"><span class="feed-ic">${icon(ic)}</span><div><p><b>${esc(x.name || "Sistema")}</b> ${esc(t.toLowerCase())}${x.detail ? ` <span class="feed-d">${esc(x.detail)}</span>` : ""}</p><time datetime="${esc(x.at)}" title="${esc(fmtDate(x.at))}">${ago(x.at)}</time></div></li>`; };
  function barChart(days, key, label) {
    const vals = days.map(d => d[key]); const max = Math.max(1, ...vals); const nice = max <= 4 ? 4 : Math.ceil(max / 4) * 4;
    return `<div class="bchart" role="img" aria-label="${esc(label)} por día, últimos 30 días">
      <div class="bchart-y" aria-hidden="true"><span>${nice}</span><span>${nice / 2}</span><span>0</span></div>
      <div class="bchart-plot"><div class="bchart-grid" aria-hidden="true"><i></i><i></i><i></i></div>
        <div class="bchart-bars">${days.map((d, i) => `<button type="button" class="bc" data-i="${i}" aria-label="${dayLabel(d.d)}: ${d[key]} ${esc(label.toLowerCase())}"><i style="height:${d[key] ? Math.max(3, d[key] / nice * 100) : 0}%"></i></button>`).join("")}</div>
        <div class="bchart-x" aria-hidden="true"><span>${dayLabel(days[0].d)}</span><span>${dayLabel(days[14].d)}</span><span>Hoy</span></div>
        <div class="bchart-tip" hidden></div>${vals.some(Boolean) ? "" : `<p class="bchart-empty">Sin datos en estos 30 días.${key === "lecciones" || key === "laboratorios" ? " Las fechas de lecciones y laboratorios se registran desde la actualización del 27 de octubre de 2026." : ""}</p>`}</div></div>`;
  }
  function wireChart(root, days, key, label) {
    const tip = $(".bchart-tip", root);
    const show = b => { const d = days[+b.dataset.i]; tip.innerHTML = `<b>${fmtN(d[key])}</b> ${esc(label.toLowerCase())}<small>${new Date(d.d + "T12:00:00").toLocaleDateString("es-UY", {weekday: "long", day: "numeric", month: "long"})}</small>`; tip.hidden = false;
      const r = b.getBoundingClientRect(), p = b.parentElement.getBoundingClientRect(); tip.style.left = `${Math.min(Math.max(r.left - p.left + r.width / 2, 70), p.width - 70)}px`; $$(".bc", root).forEach(x => x.classList.toggle("on", x === b)); };
    $$(".bc", root).forEach(b => { b.addEventListener("mouseenter", () => show(b)); b.addEventListener("focus", () => show(b)); });
    $(".bchart-bars", root).addEventListener("mouseleave", () => { tip.hidden = true; $$(".bc.on", root).forEach(x => x.classList.remove("on")); });
  }
  const csvCell = v => `"${String(v ?? "").replace(/"/g, '""')}"`;
  function downloadCSV(name, rows) {
    const blob = new Blob(["﻿" + rows.map(r => r.map(csvCell).join(";")).join("\r\n")], {type: "text/csv;charset=utf-8"});
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name; document.body.append(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }
  async function exportUsers() {
    const [{users}, cat] = await Promise.all([api("api/admin.php?a=users"), getCatalog()]);
    const pub = cat.courses.filter(c => !c.draft);
    downloadCSV(`ies-training-usuarios-${new Date().toISOString().slice(0, 10)}.csv`, [
      ["Nombre", "Correo", "Empresa", "Rol", "Estado", "Registro", "Última actividad", "Lecciones completas", "Laboratorios", "Quizzes", "Cursos terminados", ...pub.map(c => c.title)],
      ...users.map(u => [u.name, u.email, u.company || "", ROLE[u.role], u.active ? "Activa" : "Desactivada", (u.created || "").slice(0, 10), (u.last_seen || "").slice(0, 16).replace("T", " "), u.done, u.labs, u.quizzes, u.completed,
        ...pub.map(c => { const x = u.courses[c.slug]; return x ? `${x.done}/${c.lessons.length}` : ""; })])]);
    toast("Planilla descargada");
  }
  let markedP = null;
  const loadMarked = () => markedP || (markedP = new Promise((res, rej) => { const s = document.createElement("script"); s.src = "assets/vendor/marked.min.js"; s.onload = () => res(window.marked); s.onerror = rej; document.head.append(s); }));
  // Igual que build.py: una línea "N. …" pegada a un párrafo empieza una lista nueva (si no, marked la une al párrafo)
  const mdPrep = t => { const out = []; let prev = "", fence = false; for (const ln of String(t || "").split("\n")) { if (/^\s*```/.test(ln)) fence = !fence; if (!fence && /^\d+\.\s/.test(ln) && prev.trim() && !/^\s*(\d+\.|[-*])\s/.test(prev) && !/^\s*```/.test(prev)) out.push(""); out.push(ln); prev = ln; } return out.join("\n"); };
  const mdBlock = (m, t) => m.parse(mdPrep(t), {gfm: true, breaks: false});
  const mdInline = (m, t) => m.parseInline(t || "", {gfm: true});

  async function viewAdmin(parts) {
    if (!session.ready) await session.load();
    if (!session.user) { try { sessionStorage.setItem("ies.back", location.hash); } catch {} location.hash = "#/ingresar"; return; }
    if (!session.staff()) { main.innerHTML = `<div class="wrap page-h"><div class="card empty"><b>Tu cuenta no tiene acceso a la administración.</b>Si lo necesitás, pedíselo a un administrador de IES.</div></div>`; return; }
    const [sec, a, b] = parts;
    if (session.user.role !== "admin" && sec !== "cursos") { location.hash = "#/admin/cursos"; return; }
    document.title = "Administración · IES Training";
    if (!sec) return adminSummary();
    if (sec === "usuarios") return a ? adminUser(+a) : adminUsers();
    if (sec === "cursos") return a ? (b ? adminLesson(a, b) : adminCourse(a)) : adminCourses();
    if (sec === "actividad") return adminAudit();
  }
  async function adminSummary() {
    const s = await api("api/admin.php?a=dashboard");
    const k = s.kpi, first = (session.user.name || "").split(" ")[0];
    const tot = key => s.days.reduce((a, d) => a + d[key], 0);
    const SER = [["lecciones", "Lecciones completadas"], ["activos", "Técnicos activos"], ["registros", "Registros"], ["laboratorios", "Laboratorios hechos"]];
    const hoy = new Date().toLocaleDateString("es-UY", {weekday: "long", day: "numeric", month: "long"});
    main.innerHTML = adminShell("", `
      ${admHead(hoy, `Hola${first ? ", " + esc(first) : ""}`, "Así viene la formación técnica de IES.", `<button class="btn ghost sm" id="csv">${icon("download")}Exportar usuarios</button><a class="btn sm" href="#/admin/cursos">${icon("book")}Editar cursos</a>`)}
      <div class="kpis">
        ${kpi("users", fmtN(k.users), "técnicos registrados", k.new7 ? `<span class="up">+${k.new7}</span> esta semana · ${k.new30} en 30 días` : `${k.new30} nuevos en 30 días`)}
        ${kpi("pulse", fmtN(k.active7), "activos en 7 días", `${pct(k.active7, k.users)}% del total · ${k.active30} en 30 días`)}
        ${kpi("check", fmtN(k.lessons_done), "lecciones completadas", k.done7 ? `<span class="up">+${k.done7}</span> esta semana` : `${fmtN(k.labs)} laboratorios hechos`)}
        ${kpi("award", fmtN(k.certificates), "cursos terminados", `${fmtN(k.labs)} laboratorios en total`)}
      </div>
      <section class="card adm-card" id="chartCard">
        <div class="adm-card-h"><div><h2>Últimos 30 días</h2><p id="chartSum"></p></div>
          <div class="seg" role="tablist" aria-label="Qué mostrar">${SER.map(([key, t], i) => `<button role="tab" aria-selected="${i === 0}" data-k="${key}">${t}</button>`).join("")}</div></div>
        <div id="chartBox"></div>
      </section>
      <div class="adm-cols">
        <section class="card adm-card span-2"><div class="adm-card-h"><div><h2>Cursos</h2><p>Quiénes empezaron, cuántos terminaron y qué tan bien les va en los quizzes.</p></div><a class="lnk" href="#/admin/cursos">Ver todos ${icon("chev")}</a></div>
          <div class="tbl-wrap"><table class="tbl ctbl"><thead><tr><th>Curso</th><th class="num">Empezaron</th><th class="num">Terminaron</th><th>Avance medio</th><th class="num">Quiz</th><th class="num">Medios</th><th>Contenido</th></tr></thead>
          <tbody>${s.courses.map(c => `<tr><td><a class="cname" href="#/admin/cursos/${c.slug}">${courseMark(c)}<span><b>${esc(shortTitle(c.title))}</b><small>${esc(c.vendor)} · ${c.lessons} lecciones${c.draft ? " · borrador" : ""}</small></span></a></td>
            <td class="num">${c.started}</td><td class="num">${c.finished}</td><td><span class="mrow">${meter(c.avg)}<span class="mono">${c.avg}%</span></span></td>
            <td class="num">${c.quiz_ok == null ? "<span class=muted>sin datos</span>" : `${c.quiz_ok}%`}</td><td class="num">${c.media}</td>
            <td>${c.pendientes ? `<span class="pill warn">${c.pendientes} con pendientes</span>` : '<span class="pill ok">Completo</span>'}</td></tr>`).join("")}</tbody></table></div></section>
        <section class="card adm-card"><div class="adm-card-h"><div><h2>Los que más avanzan</h2><p>Por lecciones completadas.</p></div></div>
          ${s.top.length ? `<ol class="rank">${s.top.map((u, i) => `<li><span class="rank-n">${i + 1}</span><a href="#/admin/usuarios/${u.id}">${avatar(u)}<span><b>${esc(u.name)}</b><small>${esc(u.company || ROLE[u.role])}</small></span></a><span class="rank-v"><b>${u.done}</b><small>${u.completed ? `${u.completed} ${u.completed === 1 ? "curso" : "cursos"}` : "lecciones"}</small></span></li>`).join("")}</ol>`
            : `<p class="empty-s">Todavía nadie completó lecciones con su cuenta.</p>`}
        </section>
        <section class="card adm-card"><div class="adm-card-h"><div><h2>Por empresa</h2><p>Cuentas registradas.</p></div></div>
          ${s.companies.length ? `<ul class="bars">${s.companies.map(c => `<li><span>${esc(c.name)}</span>${meter(c.n, s.companies[0].n)}<b class="mono">${c.n}</b></li>`).join("")}</ul>` : `<p class="empty-s">Sin cuentas todavía.</p>`}
        </section>
        <section class="card adm-card"><div class="adm-card-h"><div><h2>Preguntas que más se fallan</h2><p>Con 3 intentos o más. Conviene revisar la lección o la pregunta.</p></div></div>
          ${s.hard.length ? `<ul class="hard">${s.hard.map(q => `<li><a href="#/admin/cursos/${q.slug}/${encodeURIComponent(q.id)}"><span class="hard-p">${Math.round(q.errores / q.intentos * 100)}%</span><span><b>${esc(q.q)}</b><small>${esc(q.slug)} · Lección ${q.n}. ${esc(q.handle)} · ${q.errores} de ${q.intentos} la erraron</small></span></a></li>`).join("")}</ul>`
            : `<p class="empty-s">Hace falta más actividad en los quizzes para ver tendencias.</p>`}
        </section>
        <section class="card adm-card"><div class="adm-card-h"><div><h2>Actividad reciente</h2></div><a class="lnk" href="#/admin/actividad">Ver toda ${icon("chev")}</a></div>
          <ul class="feed">${s.recent.map(actRow).join("") || '<li class="empty-s">Sin actividad.</li>'}</ul>
        </section>
      </div>`);
    const draw = key => {
      const [, t] = SER.find(x => x[0] === key);
      $("#chartBox").innerHTML = barChart(s.days, key, t); wireChart($("#chartBox"), s.days, key, t);
      const total = key === "activos" ? Math.max(...s.days.map(d => d.activos)) : tot(key);
      $("#chartSum").textContent = key === "activos" ? `Pico de ${total} técnicos activos en un día` : `${fmtN(total)} ${t.toLowerCase()} en el período`;
      $$("#chartCard .seg button").forEach(b => b.setAttribute("aria-selected", b.dataset.k === key));
    };
    $$("#chartCard .seg button").forEach(b => b.onclick = () => draw(b.dataset.k));
    draw("lecciones");
    $("#csv").onclick = () => exportUsers().catch(e => toast(e.message));
  }

  async function adminUsers() {
    const [{users}, cat] = await Promise.all([api("api/admin.php?a=users"), getCatalog()]);
    const total = cat.courses.filter(c => !c.draft).reduce((a, c) => a + c.lessons.length, 0);
    const counts = {todos: users.length, tecnico: users.filter(u => u.role === "tecnico").length, editor: users.filter(u => u.role === "editor").length, admin: users.filter(u => u.role === "admin").length, off: users.filter(u => !u.active).length};
    const FIL = [["todos", "Todos"], ["tecnico", "Técnicos"], ["editor", "Editores"], ["admin", "Administradores"], ["off", "Desactivadas"]];
    let fil = "todos", sort = "last", q = "";
    main.innerHTML = adminShell("usuarios", `
      ${admHead("Personas", "Usuarios", `${users.length} cuentas · ${users.filter(u => recent(u.last_seen, 7)).length} activas esta semana`, `<button class="btn ghost sm" id="csv">${icon("download")}Exportar</button><button class="btn sm" id="addU">${icon("userplus")}Agregar usuario</button>`)}
      <form class="card form pad inline-form adm-form" id="uf" hidden><h3 class="span-all">Cuenta nueva</h3><label>Nombre y apellido<input id="un" required></label><label>Correo<input id="ue" type="email" required></label><label>Empresa<input id="uc"></label>
        <label>Rol<select id="ur"><option value="tecnico">Técnico</option><option value="editor">Editor</option><option value="admin">Administrador</option></select></label>
        <div class="row"><button class="btn">Crear cuenta</button><button type="button" class="btn ghost" id="ufx">Cancelar</button></div><p class="err" id="uerr" role="alert"></p><div id="uok"></div></form>
      <div class="toolbar">
        <div class="seg" role="tablist" aria-label="Filtrar por rol">${FIL.map(([key, t]) => `<button role="tab" data-f="${key}" aria-selected="${key === fil}">${t}<span class="cnt">${counts[key]}</span></button>`).join("")}</div>
        <div class="toolbar-r"><label class="search-s">${icon("search")}<span class="sr">Buscar usuario</span><input id="uq" type="search" placeholder="Nombre, correo o empresa"></label>
          <label class="sel-s"><span class="sr">Ordenar</span><select id="us"><option value="last">Última actividad</option><option value="progress">Más avance</option><option value="name">Nombre</option><option value="created">Más nuevos</option></select></label></div>
      </div>
      <div class="card tbl-wrap"><table class="tbl utbl"><thead><tr><th>Usuario</th><th>Empresa</th><th>Rol</th><th>Avance general</th><th class="num">Cursos</th><th>Última actividad</th></tr></thead><tbody id="ub"></tbody></table></div>`);
    const paint = () => {
      let list = users.filter(u => fil === "todos" ? true : fil === "off" ? !u.active : u.role === fil);
      if (q) list = list.filter(u => (u.name + " " + u.email + " " + (u.company || "")).toLowerCase().includes(q));
      const by = {last: (a, b) => String(b.last_seen || "").localeCompare(String(a.last_seen || "")), progress: (a, b) => b.done - a.done, name: (a, b) => a.name.localeCompare(b.name, "es"), created: (a, b) => String(b.created).localeCompare(String(a.created))};
      list.sort(by[sort]);
      $("#ub").innerHTML = list.map(u => `<tr class="${u.active ? "" : "off"}" data-href="#/admin/usuarios/${u.id}">
        <td><a class="uname" href="#/admin/usuarios/${u.id}">${avatar(u)}<span><b>${esc(u.name)}</b><small>${esc(u.email)}</small></span></a></td>
        <td>${esc(u.company || "")}</td>
        <td><span class="role r-${u.role}">${ROLE[u.role]}</span>${u.active ? "" : ' <span class="pill warn">Desactivada</span>'}</td>
        <td><span class="mrow">${meter(u.done, total)}<span class="mono">${u.done}/${total}</span></span></td>
        <td class="num">${u.completed ? `<b>${u.completed}</b> ${icon("award", "i sm")}` : Object.keys(u.courses).length ? `<span class="muted">${Object.keys(u.courses).length} en curso</span>` : '<span class="muted">—</span>'}</td>
        <td><span class="seen ${recent(u.last_seen, 7) ? "on" : ""}">${ago(u.last_seen)}</span></td></tr>`).join("") || `<tr><td colspan="6" class="empty-s">No hay usuarios con ese filtro.</td></tr>`;
      $$("#ub tr[data-href]").forEach(tr => tr.addEventListener("click", e => { if (!e.target.closest("a")) location.hash = tr.dataset.href; }));
    };
    paint();
    $$(".toolbar .seg button").forEach(b => b.onclick = () => { fil = b.dataset.f; $$(".toolbar .seg button").forEach(x => x.setAttribute("aria-selected", x === b)); paint(); });
    $("#uq").addEventListener("input", e => { q = e.target.value.toLowerCase().trim(); paint(); });
    $("#us").addEventListener("change", e => { sort = e.target.value; paint(); });
    $("#csv").onclick = () => exportUsers().catch(e => toast(e.message));
    $("#addU").addEventListener("click", () => { $("#uf").hidden = false; $("#un").focus(); });
    $("#ufx").addEventListener("click", () => { $("#uf").hidden = true; });
    $("#uf").addEventListener("submit", async e => {
      e.preventDefault(); $("#uerr").textContent = "";
      try {
        const r = await api("api/admin.php?a=user_create", {name: $("#un").value, email: $("#ue").value, company: $("#uc").value, role: $("#ur").value});
        $("#uok").innerHTML = `<div class="notice">Cuenta creada. Contraseña temporal: <code class="secret">${esc(r.password)}</code> <button type="button" class="mini" id="cpy">Copiar</button><br>Pasásela a la persona; al entrar le pide elegir una propia. <a href="#/admin/usuarios/${r.id}">Ver la cuenta</a></div>`;
        $("#cpy").onclick = () => navigator.clipboard?.writeText(r.password).then(() => toast("Copiada"), () => {});
      } catch (err) { $("#uerr").textContent = err.message; }
    });
  }

  async function adminUser(id) {
    const [{user: u, log, hechos = []}, cat] = await Promise.all([api(`api/admin.php?a=user&id=${id}`), getCatalog()]);
    const me = session.user.id === u.id;
    const pub = cat.courses.filter(c => !c.draft || u.courses[c.slug]);
    const started = pub.filter(c => u.courses[c.slug]), idle = pub.filter(c => !u.courses[c.slug]);
    const ring = (d, t) => { const p = pct(d, t), r = 26, C = 2 * Math.PI * r; return `<svg class="ring" viewBox="0 0 64 64" role="img" aria-label="${p}%"><circle cx="32" cy="32" r="${r}" class="ring-bg"/><circle cx="32" cy="32" r="${r}" class="ring-fg" stroke-dasharray="${(C * p / 100).toFixed(1)} ${C.toFixed(1)}"/><text x="32" y="36.5" text-anchor="middle">${p}%</text></svg>`; };
    main.innerHTML = adminShell("usuarios", `
      <p class="crumbs2"><a href="#/admin/usuarios">Usuarios</a> / ${esc(u.name)}</p>
      <section class="card prof">
        ${avatar(u, "xl")}
        <div class="prof-b"><h1>${esc(u.name)}</h1>
          <p class="prof-m"><a href="mailto:${esc(u.email)}">${icon("mail", "i sm")}${esc(u.email)}</a>${u.company ? `<span>${icon("building", "i sm")}${esc(u.company)}</span>` : ""}</p>
          <p class="prof-t"><span class="role r-${u.role}">${ROLE[u.role]}</span>${u.active ? '<span class="pill ok">Activa</span>' : '<span class="pill warn">Desactivada</span>'}<span class="muted">Se registró el ${new Date(u.created).toLocaleDateString("es-UY", {day: "numeric", month: "long", year: "numeric"})} · última actividad ${ago(u.last_seen)}</span></p></div>
        <div class="prof-a">
          <label>Rol<select id="role" ${me ? "disabled" : ""}>${Object.entries(ROLE).map(([key, t]) => `<option value="${key}" ${u.role === key ? "selected" : ""}>${t}</option>`).join("")}</select></label>
          <div class="row"><button class="btn ghost sm" id="rst">${icon("key")}Reiniciar contraseña</button><button class="btn ghost sm ${u.active ? "danger" : ""}" id="act" ${me ? "disabled" : ""}>${u.active ? "Desactivar" : "Reactivar"}</button></div>
        </div>
      </section>
      <div id="rstOut"></div>
      <div class="kpis">${kpi("check", u.done, "lecciones completas")}${kpi("flask", u.labs, "laboratorios hechos")}${kpi("quiz", u.quizzes, "quizzes respondidos")}${kpi("award", u.completed, "cursos terminados")}</div>
      <section class="adm-sec"><div class="adm-card-h"><div><h2>Cursos</h2><p>${started.length ? `${started.length} empezados${idle.length ? `, ${idle.length} sin empezar` : ""}.` : "Todavía no empezó ningún curso."}</p></div></div>
        <div class="ucourses">${started.map(c => { const x = u.courses[c.slug]; return `<a class="card ucard" href="#/curso/${c.slug}" target="_blank" rel="noopener">${ring(x.done, c.lessons.length)}<span><b>${esc(shortTitle(c.title))}</b><small>${x.done} de ${c.lessons.length} lecciones${x.done >= c.lessons.length ? " · terminado" : ""}</small></span></a>`; }).join("")}</div>
        ${idle.length ? `<p class="idle">Sin empezar: ${idle.map(c => esc(shortTitle(c.title))).join(" · ")}</p>` : ""}
      </section>
      <div class="adm-cols two">
        <section class="card adm-card"><div class="adm-card-h"><div><h2>Lecciones completadas</h2><p>Las más recientes primero.</p></div></div>
          ${hechos.length ? `<ul class="feed">${hechos.map(h => `<li class="feed-i g-cursos"><span class="feed-ic">${icon("check")}</span><div><p><b>${esc(h.handle)}</b> <span class="feed-d">${esc(shortTitle(h.curso))} · lección ${h.n}</span></p><time>${ago(new Date(h.t * 1000).toISOString())}</time></div></li>`).join("")}</ul>`
            : `<p class="empty-s">Sin fechas registradas todavía (se guardan desde octubre de 2026).</p>`}</section>
        <section class="card adm-card"><div class="adm-card-h"><div><h2>Actividad de la cuenta</h2></div></div>
          <ul class="feed">${log.map(x => actRow({...x, name: u.name})).join("") || '<li class="empty-s">Sin actividad registrada.</li>'}</ul></section>
      </div>`);
    $("#role").addEventListener("change", async e => { try { await api("api/admin.php?a=user_update", {id, role: e.target.value}); toast("Rol actualizado"); adminUser(id); } catch (err) { toast(err.message); } });
    $("#act").addEventListener("click", async e => {
      const b = e.currentTarget;
      if (u.active && !b.dataset.armed) { b.dataset.armed = 1; b.textContent = "¿Desactivar? Tocá de nuevo"; setTimeout(() => { if (b.isConnected) { delete b.dataset.armed; b.textContent = "Desactivar"; } }, 4000); return; }
      try { await api("api/admin.php?a=user_update", {id, active: !u.active}); toast(u.active ? "Cuenta desactivada" : "Cuenta reactivada"); adminUser(id); } catch (err) { toast(err.message); }
    });
    $("#rst").addEventListener("click", async e => {
      const b = e.currentTarget;
      if (!b.dataset.armed) { b.dataset.armed = 1; b.lastChild.textContent = "¿Reiniciar? Tocá de nuevo"; setTimeout(() => { if (b.isConnected) { delete b.dataset.armed; b.lastChild.textContent = "Reiniciar contraseña"; } }, 4000); return; }
      try { const r = await api("api/admin.php?a=user_reset", {id}); $("#rstOut").innerHTML = `<div class="notice">Contraseña temporal: <code class="secret">${esc(r.password)}</code> <button type="button" class="mini" id="cpy">Copiar</button>. Al entrar, le pide elegir una nueva.</div>`; $("#cpy").onclick = () => navigator.clipboard?.writeText(r.password).then(() => toast("Copiada"), () => {}); b.lastChild.textContent = "Reiniciar contraseña"; delete b.dataset.armed; }
      catch (err) { toast(err.message); }
    });
  }

  async function adminAudit() {
    const {log} = await api("api/admin.php?a=audit");
    const G = [["todo", "Todo"], ["ingresos", "Ingresos"], ["usuarios", "Usuarios"], ["cursos", "Cursos"]];
    let g = "todo", q = "";
    main.innerHTML = adminShell("actividad", `
      ${admHead("Registro", "Actividad", "Las últimas 200 acciones: ingresos, registros, cambios de cursos y de usuarios.")}
      <div class="toolbar"><div class="seg" role="tablist" aria-label="Filtrar">${G.map(([key, t]) => `<button role="tab" data-g="${key}" aria-selected="${key === g}">${t}<span class="cnt">${key === "todo" ? log.length : log.filter(x => actGroup(x.action) === key).length}</span></button>`).join("")}</div>
        <div class="toolbar-r"><label class="search-s">${icon("search")}<span class="sr">Buscar</span><input id="aq" type="search" placeholder="Persona, curso o detalle"></label></div></div>
      <div id="alog"></div>`);
    const paint = () => {
      const list = log.filter(x => (g === "todo" || actGroup(x.action) === g) && (!q || `${x.name || ""} ${x.action} ${x.detail || ""}`.toLowerCase().includes(q)));
      const byDay = {}; list.forEach(x => (byDay[x.at.slice(0, 10)] ||= []).push(x));
      const today = new Date().toISOString().slice(0, 10), yest = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
      $("#alog").innerHTML = Object.entries(byDay).map(([d, xs]) => `<section class="card adm-card day"><h3>${d === today ? "Hoy" : d === yest ? "Ayer" : new Date(d + "T12:00:00").toLocaleDateString("es-UY", {weekday: "long", day: "numeric", month: "long"})}<span class="cnt">${xs.length}</span></h3>
        <ul class="feed">${xs.map(x => actRow(x).replace(/<time([^>]*)>[^<]*<\/time>/, `<time$1>${new Date(x.at).toLocaleTimeString("es-UY", {hour: "2-digit", minute: "2-digit", hour12: false})}</time>`)).join("")}</ul></section>`).join("") || `<div class="card adm-card"><p class="empty-s">Nada con ese filtro.</p></div>`;
    };
    paint();
    $$(".toolbar .seg button").forEach(b => b.onclick = () => { g = b.dataset.g; $$(".toolbar .seg button").forEach(x => x.setAttribute("aria-selected", x === b)); paint(); });
    $("#aq").addEventListener("input", e => { q = e.target.value.toLowerCase().trim(); paint(); });
  }

  /* cursos */
  const drafts = {};
  async function loadDraft(slug, fresh) {
    if (!fresh && drafts[slug]) return drafts[slug];
    const {course} = await api(`api/admin.php?a=course&slug=${encodeURIComponent(slug)}`);
    course.lessons.forEach(l => { l.id = lid(l); l.idea_md = l.idea_md && l.idea_md.length ? l.idea_md : (l.idea || []).map(h => h.replace(/<[^>]+>/g, "")); });
    (course.arcs || []).forEach(a => { a.lessons = a.lessons.map(r => lid(course.lessons.find(l => lid(l) === String(r)) || course.lessons.find(l => l.n === +r) || {n: r})); });
    drafts[slug] = {course, base: course.updated || "", dirty: false};
    return drafts[slug];
  }
  async function saveDraft(slug, stay) {
    const d = drafts[slug]; const m = await loadMarked();
    // stay: guardar sin salir del editor; se procesa una copia para no mover lo que está en pantalla
    const c = stay ? structuredClone(d.course) : d.course;
    c.lessons.forEach(l => {
      const keep = (l.idea_md || []).map((x, i) => [x, (l.idea_pics || [])[i] || []]).filter(([x, ps]) => x.trim() || ps.length);
      l.idea_md = keep.map(k => k[0]); l.idea_pics = keep.map(k => k[1]);
      l.idea = l.idea_md.map(x => mdInline(m, x));
      l.theory = (l.theory_md || "").trim() ? mdBlock(m, l.theory_md) : "";
      l.impact = mdInline(m, l.impact_md); l.who = mdInline(m, l.who_md);
      l.lab = l.lab || {}; l.lab.html = mdBlock(m, l.lab.md);
    });
    const {course} = await api("api/admin.php?a=course_save", {course: c, base: d.base});
    delete courses[slug]; catalog = null;
    if (stay) { d.base = course.updated || d.base; d.dirty = false; return course; }
    await loadDraft(slug, true);
    return course;
  }
  let admCourseStats = null;
  async function adminCourses() {
    catalog = null;
    const {courses: list} = await api("api/admin.php?a=courses"); admCourseStats = Object.fromEntries(list.map(c => [c.slug, c]));
    const pend = list.filter(c => c.health.length).length;
    const tl = list.reduce((a, c) => a + c.lessons, 0), tm = list.reduce((a, c) => a + c.media.total, 0);
    let view = "todos";
    main.innerHTML = adminShell("cursos", `
      ${admHead("Contenido", "Cursos", `${list.length} cursos · ${tl} lecciones · ${tm} capturas y videos${pend ? ` · ${pend} con pendientes` : ""}`, `<button class="btn sm" id="newC">${icon("plus")}Curso nuevo</button>`)}
      <form class="card form pad inline-form adm-form" id="ncf" hidden><h3 class="span-all">Curso nuevo</h3><label>Título<input id="nct" required></label><label>Fabricante<input id="ncv"></label><label>Identificador<input id="ncs" pattern="[a-z0-9-]+" placeholder="ej. bosch-incendio" required><small>Minúsculas, números y guiones. Va en la dirección.</small></label>
        <div class="row"><button class="btn">Crear borrador</button><button type="button" class="btn ghost" id="ncx">Cancelar</button></div><p class="err" id="ncerr" role="alert"></p></form>
      <div class="toolbar"><div class="seg" role="tablist" aria-label="Filtrar cursos">${[["todos", "Todos", list.length], ["pend", "Con pendientes", pend], ["draft", "Borradores", list.filter(c => c.draft).length]].map(([key, t, n]) => `<button role="tab" data-v="${key}" aria-selected="${key === view}">${t}<span class="cnt">${n}</span></button>`).join("")}</div>
        <p class="hint">El orden de las tarjetas es el orden del catálogo. Movelas con las flechas.</p></div>
      <div class="cgrid" id="cgrid"></div>`);
    const paint = () => {
      const shown = list.map((c, i) => [c, i]).filter(([c]) => view === "todos" || (view === "pend" ? c.health.length : c.draft));
      $("#cgrid").innerHTML = shown.map(([c, i]) => `<article class="card ccard-a" data-slug="${c.slug}">
        <div class="ccard-top">${courseMark(c)}<div><h3><a href="#/admin/cursos/${c.slug}">${esc(c.title)}</a></h3><p>${esc(c.vendor)} · ${c.arcs} ${c.arcs === 1 ? "parte" : "partes"}${c.draft ? ' · <span class="pill warn">Borrador</span>' : ""}</p></div>
          <div class="ord"><button class="mini" data-up="${i}" ${i === 0 ? "disabled" : ""} aria-label="Subir en el catálogo">↑</button><button class="mini" data-dn="${i}" ${i === list.length - 1 ? "disabled" : ""} aria-label="Bajar en el catálogo">↓</button></div></div>
        <dl class="cstats"><div><dt>lecciones</dt><dd>${c.lessons}</dd></div><div><dt>quiz</dt><dd>${c.quiz}</dd></div><div><dt>lab</dt><dd>${(Math.round(c.lab_minutes / 30) / 2).toLocaleString("es-UY")} h</dd></div>
          <div title="${c.media.gif} GIF, ${c.media.video} videos"><dt>medios</dt><dd>${c.media.total}</dd></div><div><dt>alumnos</dt><dd>${c.learners}</dd></div></dl>
        ${c.health.length ? `<details class="health"><summary><span class="pill warn">${c.health.length} ${c.health.length === 1 ? "lección" : "lecciones"} con pendientes</span></summary><ul>${c.health.map(h => `<li><a href="#/admin/cursos/${c.slug}/${encodeURIComponent(h.id)}">${h.n}. ${esc(h.handle)}</a><span>falta ${h.falta.join(", ")}</span></li>`).join("")}</ul></details>` : '<p class="health"><span class="pill ok">Contenido completo</span></p>'}
        <div class="ccard-f"><small>${c.updated ? `Actualizado ${ago(c.updated)}` : ""}${c.versions ? ` · ${c.versions} ${c.versions === 1 ? "versión guardada" : "versiones guardadas"}` : ""}</small>
          <span class="row"><a class="btn ghost sm" href="#/curso/${c.slug}" target="_blank" rel="noopener">Ver</a><a class="btn sm" href="#/admin/cursos/${c.slug}">Editar</a></span></div></article>`).join("") || `<div class="card adm-card"><p class="empty-s">Nada con ese filtro.</p></div>`;
      const move = async (i, d) => { const o = list.map(c => c.slug); [o[i], o[i + d]] = [o[i + d], o[i]]; try { await api("api/admin.php?a=catalog_order", {order: o}); catalog = null; adminCourses(); } catch (e) { toast(e.message); } };
      $$("#cgrid [data-up]").forEach(b => b.onclick = () => move(+b.dataset.up, -1));
      $$("#cgrid [data-dn]").forEach(b => b.onclick = () => move(+b.dataset.dn, 1));
    };
    paint();
    $$(".toolbar .seg button").forEach(b => b.onclick = () => { view = b.dataset.v; $$(".toolbar .seg button").forEach(x => x.setAttribute("aria-selected", x === b)); paint(); });
    $("#newC").onclick = () => { $("#ncf").hidden = false; $("#nct").focus(); };
    $("#ncx").onclick = () => { $("#ncf").hidden = true; };
    $("#nct").addEventListener("input", e => { if (!$("#ncs").dataset.touched) $("#ncs").value = e.target.value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40); });
    $("#ncs").addEventListener("input", e => { e.target.dataset.touched = 1; });
    $("#ncf").addEventListener("submit", async e => { e.preventDefault(); try { const {course} = await api("api/admin.php?a=course_new", {title: $("#nct").value, vendor: $("#ncv").value, slug: $("#ncs").value}); catalog = null; location.hash = `#/admin/cursos/${course.slug}`; } catch (err) { $("#ncerr").textContent = err.message; } });
  }
  const linesOf = v => String(v || "").split("\n").map(x => x.trim()).filter(Boolean);
  async function adminCourse(slug) {
    const d = await loadDraft(slug);
    if (!admCourseStats) { try { const {courses: list} = await api("api/admin.php?a=courses"); admCourseStats = Object.fromEntries(list.map(x => [x.slug, x])); } catch {} }
    const c = d.course;
    const arcOf = l => (c.arcs || []).findIndex(a => a.lessons.includes(lid(l)));
    main.innerHTML = adminShell("cursos", `
      <div class="savebar"><p class="crumbs2"><a href="#/admin/cursos">Cursos</a> / ${esc(c.title)}</p><span class="dirty" id="dirty" ${d.dirty ? "" : "hidden"}>Cambios sin guardar</span>
        <div class="row"><button class="btn ghost sm" id="hist">Historial</button><a class="btn ghost sm" href="#/curso/${slug}" target="_blank" rel="noopener">Ver en el sitio</a><button class="btn sm" id="save">Guardar cambios</button></div></div>
      <div id="histBox"></div>
      ${(() => { const st = admCourseStats?.[slug]; return `<section class="card ced-h">${courseMark(c)}<div><span class="k">${esc(c.vendor || "Curso")}</span><h1>${esc(c.title)}</h1>
        <p class="ced-s"><span>${c.lessons.length} lecciones</span><span>${(c.arcs || []).length} partes</span><span>${c.lessons.reduce((a, l) => a + (l.quiz || []).length, 0)} preguntas</span>${st ? `<span>${st.learners} alumnos</span><span>${st.media.total} medios</span>` : ""}${c.draft ? '<span class="pill warn">Borrador</span>' : '<span class="pill ok">Publicado</span>'}${st?.health.length ? `<span class="pill warn">${st.health.length} con pendientes</span>` : ""}</p></div></section>`; })()}
      <div class="card pad logo-ed"><div class="logo-prev">${c.logo ? `<img src="${esc(c.logo)}" alt="Logo actual">` : '<span class="note">Sin logo</span>'}</div>
        <div><h3>Logo del curso</h3><p class="note">PNG con fondo transparente, JPG o WebP, hasta 3 MB. Aparece en la tarjeta del catálogo y en la página del curso. Se guarda al subirlo.</p>
        <div class="row"><label class="btn ghost sm">${icon("upload")}${c.logo ? "Cambiar logo" : "Subir logo"}<input type="file" id="logoF" accept="image/png,image/jpeg,image/webp" hidden></label>${c.logo ? '<button type="button" class="mini del" id="logoX">Quitar logo</button>' : ""}</div></div></div>
      <form class="card form pad grid2" id="cf">
        <label class="span2">Título<input name="title" value="${esc(c.title)}" required></label>
        <label>Fabricante<input name="vendor" value="${esc(c.vendor || "")}"></label>
        <label>Nivel<input name="level" value="${esc(c.level || "")}"></label>
        <label class="span2">Frase corta<input name="tagline" value="${esc(c.tagline || "")}"></label>
        <label class="span2">Descripción<textarea name="description" rows="3">${esc(c.description || "")}</textarea></label>
        <label class="span2">Para quién es<input name="audience" value="${esc(c.audience || "")}"></label>
        <label>Qué vas a aprender <small>Uno por línea.</small><textarea name="outcomes" rows="6">${esc((c.outcomes || []).join("\n"))}</textarea></label>
        <label>Requisitos <small>Uno por línea.</small><textarea name="prerequisites" rows="6">${esc((c.prerequisites || []).join("\n"))}</textarea></label>
        <label class="span2">Versiones<textarea name="version_note" rows="2">${esc(c.version_note || "")}</textarea></label>
        <label class="check span2"><input type="checkbox" name="draft" ${c.draft ? "checked" : ""}> Borrador: el curso no aparece en el catálogo público</label>
      </form>
      <section class="sec"><div class="sec-h"><div><h2>Partes y lecciones</h2><p>Arrastrá las lecciones para cambiarlas de lugar o de parte (también con las flechas o el selector). La numeración se actualiza sola al guardar.</p></div><div class="row"><button class="btn ghost" id="addArc">Agregar parte</button><button class="btn" id="addL">Agregar lección</button></div></div>
        <div id="arcs">${(c.arcs || []).map((a, ai) => `<div class="card pad arc-ed" data-ai="${ai}"><div class="grid2"><label>Módulo ${ai + 1}<input data-arc="title" value="${esc(a.title)}"></label><label>Por qué esta parte<input data-arc="why" value="${esc(a.why || "")}"></label></div>
          <ol class="les-ed" data-ai="${ai}">${a.lessons.map(id => c.lessons.find(l => lid(l) === id)).filter(Boolean).map(l => lessonRow(c, l)).join("") || '<li class="note">Arrastrá lecciones a esta parte.</li>'}</ol>
          ${!a.lessons.length ? `<button type="button" class="mini del" data-delarc="${ai}">Quitar parte</button>` : ""}</div>`).join("")}
          ${c.lessons.filter(l => arcOf(l) < 0).length ? `<div class="card pad arc-ed"><b>Sin módulo asignado</b><ol class="les-ed" data-ai="none">${c.lessons.filter(l => arcOf(l) < 0).map(l => lessonRow(c, l)).join("")}</ol></div>` : ""}</div>
      </section>
      <section class="sec"><div class="sec-h"><div><h2>Donde las fuentes no coinciden</h2><p>Tema, posturas y cómo decidir.</p></div><button class="btn ghost" id="addS">Agregar</button></div>
        <div id="splits">${(c.splits || []).map((s, i) => `<div class="card pad grid2 split-ed" data-si="${i}"><label class="span2">Tema<input data-sp="topic" value="${esc(s.topic.replace(/<[^>]+>/g, ""))}"></label><label>Posturas<textarea data-sp="sides" rows="3">${esc(s.sides.replace(/<[^>]+>/g, ""))}</textarea></label><label>Cómo decidir<textarea data-sp="decide" rows="3">${esc((s.decide || "").replace(/<[^>]+>/g, ""))}</textarea></label><button type="button" class="mini del" data-dels="${i}">Quitar</button></div>`).join("")}</div>
      </section>`);
    const mark = () => { d.dirty = true; $("#dirty").hidden = false; };
    $("#cf").addEventListener("input", e => {
      const f = e.target; if (!f.name) return;
      if (f.name === "draft") c.draft = f.checked;
      else if (f.name === "outcomes" || f.name === "prerequisites") c[f.name] = linesOf(f.value);
      else c[f.name] = f.value;
      mark();
    });
    $$("[data-arc]").forEach(inp => inp.addEventListener("input", () => { c.arcs[+inp.closest("[data-ai]").dataset.ai][inp.dataset.arc] = inp.value; mark(); }));
    $$("[data-sp]").forEach(inp => inp.addEventListener("input", () => { c.splits[+inp.closest("[data-si]").dataset.si][inp.dataset.sp] = esc(inp.value); mark(); }));
    $$("[data-dels]").forEach(b => b.onclick = () => { c.splits.splice(+b.dataset.dels, 1); mark(); adminCourse(slug); });
    $$("[data-delarc]").forEach(b => b.onclick = () => { c.arcs.splice(+b.dataset.delarc, 1); mark(); adminCourse(slug); });
    $("#addS").onclick = () => { (c.splits = c.splits || []).push({topic: "Tema nuevo", sides: "", decide: ""}); mark(); adminCourse(slug); };
    $("#addArc").onclick = () => { (c.arcs = c.arcs || []).push({title: `Módulo ${c.arcs.length + 1}`, why: "", lessons: []}); mark(); adminCourse(slug); };
    $("#addL").onclick = () => {
      const id = Math.random().toString(36).slice(2, 10);
      c.lessons.push({id, n: c.lessons.length + 1, handle: "Lección nueva", summary: "", idea_md: ["", "", ""], idea: [], impact_md: "", who_md: "", lab: {energy: "Rápido", minutes: 10, md: ""}, rule: "", quiz: [], sources: [], script: []});
      if (!c.arcs || !c.arcs.length) c.arcs = [{title: "Parte 1", why: "", lessons: []}];
      c.arcs[c.arcs.length - 1].lessons.push(id); mark();
      location.hash = `#/admin/cursos/${slug}/${id}`;
    };
    // mover, cambiar de parte, quitar
    const order = () => { const ids = []; (c.arcs || []).forEach(a => ids.push(...a.lessons)); c.lessons.forEach(l => { if (!ids.includes(lid(l))) ids.push(lid(l)); }); return ids; };
    $$("[data-mv]").forEach(b => b.onclick = () => {
      const id = b.dataset.id, dir = +b.dataset.mv;
      const a = (c.arcs || []).find(x => x.lessons.includes(id)); if (!a) return;
      const i = a.lessons.indexOf(id), j = i + dir; if (j < 0 || j >= a.lessons.length) return;
      [a.lessons[i], a.lessons[j]] = [a.lessons[j], a.lessons[i]];
      const ids = order(); c.lessons.sort((x, y) => ids.indexOf(lid(x)) - ids.indexOf(lid(y))); mark(); adminCourse(slug);
    });
    $$("[data-arcsel]").forEach(sel => sel.onchange = () => {
      const id = sel.dataset.arcsel; (c.arcs || []).forEach(a => { a.lessons = a.lessons.filter(x => x !== id); });
      if (sel.value !== "") c.arcs[+sel.value].lessons.push(id);
      const ids = order(); c.lessons.sort((x, y) => ids.indexOf(lid(x)) - ids.indexOf(lid(y))); mark(); adminCourse(slug);
    });
    $$("[data-dell]").forEach(b => b.onclick = () => {
      if (!b.dataset.armed) { b.dataset.armed = 1; b.textContent = "¿Quitar?"; setTimeout(() => { if (b.isConnected) { delete b.dataset.armed; b.textContent = "Quitar"; } }, 3500); return; }
      const id = b.dataset.dell; c.lessons = c.lessons.filter(l => lid(l) !== id); (c.arcs || []).forEach(a => { a.lessons = a.lessons.filter(x => x !== id); }); mark(); adminCourse(slug);
    });
    // arrastrar y soltar lecciones entre partes
    let dragId = null;
    const clearMarks = () => $$(".drop-before,.drop-after,.drop-end").forEach(x => x.classList.remove("drop-before", "drop-after", "drop-end"));
    $$(".les-ed li[data-lid]").forEach(li => {
      li.addEventListener("dragstart", e => { dragId = li.dataset.lid; li.classList.add("dragging"); e.dataTransfer.effectAllowed = "move"; e.dataTransfer.setData("text/plain", dragId); });
      li.addEventListener("dragend", () => { li.classList.remove("dragging"); clearMarks(); dragId = null; });
    });
    $$(".les-ed").forEach(ol => {
      ol.addEventListener("dragover", e => {
        if (!dragId) return; e.preventDefault(); clearMarks();
        const li = e.target.closest("li[data-lid]");
        if (li && li.dataset.lid !== dragId) { const r = li.getBoundingClientRect(); li.classList.add(e.clientY < r.top + r.height / 2 ? "drop-before" : "drop-after"); }
        else if (!li) ol.classList.add("drop-end");
      });
      ol.addEventListener("drop", e => {
        e.preventDefault(); if (!dragId) return;
        const li = e.target.closest("li[data-lid]");
        if (li && li.dataset.lid === dragId) { clearMarks(); return; }
        const after = li?.classList.contains("drop-after");
        const ref = li && li.dataset.lid !== dragId ? li.dataset.lid : null;
        (c.arcs || []).forEach(a => { a.lessons = a.lessons.filter(x => x !== dragId); });
        if (ol.dataset.ai !== "none") {
          const arc = c.arcs[+ol.dataset.ai];
          const idx = ref ? arc.lessons.indexOf(ref) + (after ? 1 : 0) : arc.lessons.length;
          arc.lessons.splice(Math.max(0, idx), 0, dragId);
        }
        const ids = order(); c.lessons.sort((x, y) => ids.indexOf(lid(x)) - ids.indexOf(lid(y)));
        dragId = null; mark(); adminCourse(slug);
      });
    });
    // logo
    const logoUp = async fd => {
      fd.append("slug", slug);
      try {
        const r = await fetch("api/admin.php?a=logo", {method: "POST", headers: {"X-IES": "1"}, body: fd, credentials: "same-origin"});
        const j = await r.json().catch(() => ({})); if (!r.ok) throw new Error(j.error || `Error ${r.status}`);
        if (j.logo) c.logo = j.logo; else delete c.logo;
        d.base = j.updated; delete courses[slug]; catalog = null;
        toast(j.logo ? "Logo guardado" : "Logo quitado"); adminCourse(slug);
      } catch (err) { toast(err.message); }
    };
    $("#logoF").addEventListener("change", e => { const f = e.target.files[0]; if (!f) return; const fd = new FormData(); fd.append("logo", f); logoUp(fd); });
    $("#logoX")?.addEventListener("click", () => { const fd = new FormData(); fd.append("quitar", "1"); logoUp(fd); });
    $("#save").onclick = async () => { const b = $("#save"); b.disabled = true; b.textContent = "Guardando…"; try { await saveDraft(slug); toast("Curso guardado"); adminCourse(slug); } catch (e) { toast(e.message); b.disabled = false; b.textContent = "Guardar cambios"; } };
    $("#hist").onclick = async () => {
      const box = $("#histBox"); if (box.innerHTML) { box.innerHTML = ""; return; }
      const {versions} = await api(`api/admin.php?a=history&slug=${slug}`);
      box.innerHTML = `<div class="card pad"><h3 style="font-size:17px;margin-bottom:8px">Versiones anteriores</h3>${versions.length ? `<ul class="hist">${versions.map(v => { const m = v.file.match(/^(\d{4})(\d\d)(\d\d)-(\d\d)(\d\d)(\d\d)-?(.*)\.json$/); return `<li><span>${m ? `${m[3]}/${m[2]}/${m[1]} ${m[4]}:${m[5]}` : v.file}${m && m[7] ? `, antes de un cambio de ${esc(m[7])}` : ""}</span><button class="mini" data-rest="${esc(v.file)}">Restaurar</button></li>`; }).join("")}</ul>` : '<p class="note">Todavía no hay versiones guardadas: se crean cada vez que guardás.</p>'}</div>`;
      $$("[data-rest]").forEach(b => b.onclick = async () => {
        if (!b.dataset.armed) { b.dataset.armed = 1; b.textContent = "¿Restaurar esta? Tocá de nuevo"; return; }
        try { await api("api/admin.php?a=restore", {slug, file: b.dataset.rest}); delete courses[slug]; catalog = null; await loadDraft(slug, true); toast("Versión restaurada"); adminCourse(slug); } catch (e) { toast(e.message); }
      });
    };
  }
  function lessonChips(c, l) {
    const lab = (l.lab?.md || "").trim(), q = (l.quiz || []).length, src = (l.sources || []).length, med = admCourseStats?.[c.slug]?.media?.por_leccion?.[lid(l)] || 0;
    const chip = (ok, ic, t) => `<span class="lchip ${ok ? "" : "miss"}" title="${esc(t)}">${icon(ic, "i xs")}${esc(t)}</span>`;
    return chip(lab, "flask", lab ? `${l.lab.minutes || "?"} min` : "sin lab") + chip(q >= 3, "quiz", `${q} preg.`) + chip(src, "link", `${src} fuentes`) + (med ? chip(true, "image", `${med} medios`) : "");
  }
  function lessonRow(c, l) {
    const ai = (c.arcs || []).findIndex(a => a.lessons.includes(lid(l)));
    return `<li draggable="true" data-lid="${esc(lid(l))}"><span class="grip" title="Arrastrar" aria-hidden="true">${icon("grip")}</span><span class="mono">${String(c.lessons.indexOf(l) + 1).padStart(2, "0")}</span><a href="#/admin/cursos/${c.slug}/${esc(lid(l))}"><b>${esc(l.handle)}</b><small>${esc(l.summary || "")}</small><span class="lchips">${lessonChips(c, l)}</span></a>
      <select data-arcsel="${esc(lid(l))}" aria-label="Parte de la lección">${(c.arcs || []).map((a, i) => `<option value="${i}" ${i === ai ? "selected" : ""}>Módulo ${i + 1}</option>`).join("")}<option value="" ${ai < 0 ? "selected" : ""}>Sin módulo</option></select>
      <span class="row"><button class="mini" data-mv="-1" data-id="${esc(lid(l))}" aria-label="Subir">↑</button><button class="mini" data-mv="1" data-id="${esc(lid(l))}" aria-label="Bajar">↓</button><button class="mini del" data-dell="${esc(lid(l))}">Quitar</button></span></li>`;
  }
  async function adminLesson(slug, id) {
    const d = await loadDraft(slug); const c = d.course;
    const l = c.lessons.find(x => lid(x) === id);
    if (!l) { location.hash = `#/admin/cursos/${slug}`; return; }
    const m = await loadMarked();
    l.quiz = l.quiz || []; l.sources = l.sources || []; l.script = l.script || []; l.lab = l.lab || {};
    const pos = c.lessons.indexOf(l) + 1;
    const quizEd = () => l.quiz.map((q, qi) => `<div class="card pad q-ed" data-qi="${qi}"><label>Pregunta ${qi + 1}<input data-q="q" value="${esc(q.q)}"></label>
      ${[0, 1, 2, 3].map(j => `<div class="opt-ed"><input type="radio" name="ans${qi}" value="${j}" ${q.answer === j ? "checked" : ""} aria-label="Respuesta correcta ${"ABCD"[j]}"><span class="mono">${"ABCD"[j]}</span><input data-opt="${j}" value="${esc(q.options[j] || "")}" placeholder="Opción ${"ABCD"[j]}"></div>`).join("")}
      <label>Por qué la correcta es correcta<textarea data-q="why" rows="2">${esc(q.why || "")}</textarea></label><button type="button" class="mini del" data-delq="${qi}">Quitar pregunta</button></div>`).join("");
    main.innerHTML = adminShell("cursos", `
      <div class="savebar"><p class="crumbs2"><a href="#/admin/cursos">Cursos</a> / <a href="#/admin/cursos/${slug}">${esc(c.title)}</a> / Lección ${pos}</p><span class="dirty" id="dirty" ${d.dirty ? "" : "hidden"}>Cambios sin guardar</span>
        <div class="row"><a class="btn ghost sm" href="#/curso/${slug}/${pos}" target="_blank" rel="noopener">Ver en el sitio</a><button class="btn sm" id="save">Guardar cambios</button></div></div>
      ${(() => { const prev = c.lessons[pos - 2], next = c.lessons[pos]; const ai = (c.arcs || []).findIndex(a => a.lessons.includes(lid(l)));
        return `<section class="card ced-h led-h"><span class="led-n">${String(pos).padStart(2, "0")}</span><div><span class="k">${ai >= 0 ? `Módulo ${ai + 1} · ${esc(c.arcs[ai].title)}` : "Sin módulo"}</span><h1>${esc(l.handle)}</h1><p class="lchips">${lessonChips(c, l)}</p></div>
          <nav class="led-nav" aria-label="Otras lecciones">${prev ? `<a class="btn ghost sm" href="#/admin/cursos/${slug}/${encodeURIComponent(lid(prev))}" title="${esc(prev.handle)}">${icon("back")}Anterior</a>` : ""}${next ? `<a class="btn ghost sm" href="#/admin/cursos/${slug}/${encodeURIComponent(lid(next))}" title="${esc(next.handle)}">Siguiente${icon("chev")}</a>` : ""}</nav></section>`; })()}
      <form class="form" id="lf2">
        <div class="card pad grid2">
          <label>Nombre de la lección <small>2 a 4 palabras.</small><input data-f="handle" value="${esc(l.handle)}" required></label>
          <label>Resumen <small>Una línea, aparece en el índice.</small><input data-f="summary" value="${esc(l.summary || "")}"></label>
        </div>
        <div class="card pad"><h3>La idea, en tres líneas <small>Admite \`código\` y **negrita**.</small></h3>
          ${[0, 1, 2].map(i => `<label class="sr" for="id${i}">Idea ${i + 1}</label><textarea id="id${i}" data-idea="${i}" rows="2">${esc((l.idea_md || [])[i] || "")}</textarea>`).join("")}
          <div class="grid2"><label>Qué mejora en la obra<textarea data-f="impact_md" rows="3">${esc(l.impact_md || "")}</textarea></label><label>Quién lo dice<textarea data-f="who_md" rows="3">${esc(l.who_md || "")}</textarea></label></div>
          <label>Regla para el manual<input data-f="rule" value="${esc(l.rule || "")}"></label></div>
        <div class="card pad"><h3>Laboratorio</h3>
          <div class="grid3"><label>Tipo<select data-lab="energy">${["Rápido", "Foco", "Campo", "Admin"].map(x => `<option ${l.lab.energy === x ? "selected" : ""}>${x}</option>`).join("")}</select></label><label>Minutos<input type="number" min="0" max="240" data-lab="minutes" value="${l.lab.minutes ?? ""}"></label></div>
          <div class="row ins"><label class="btn ghost sm">${icon("upload")}Insertar imagen, GIF o video<input type="file" id="insF" accept="image/png,image/jpeg,image/webp,image/gif,video/mp4,video/webm" hidden></label>
            <input id="insU" placeholder="Enlace de YouTube o Vimeo" autocomplete="off"><button type="button" class="btn ghost sm" id="insY">Insertar video</button><span class="note" id="insS" role="status"></span></div>
          <div class="md-ed"><label>Pasos en Markdown <small>Listas numeradas, \`código\`, bloques con \`\`\`routeros … \`\`\`. Los medios se insertan donde está el cursor.</small><textarea data-lab="md" rows="22" class="code" id="labMd">${esc(l.lab.md || "")}</textarea></label>
          <div><span class="k">Vista previa</span><div class="lab-body md-prev" id="prev">${mdBlock(m, l.lab.md)}</div></div></div></div>
        <div class="card pad"><div class="sec-h" style="margin:0 0 6px"><h3>Quiz</h3><button type="button" class="btn ghost sm" id="addQ">Agregar pregunta</button></div><p class="note" style="margin:0 0 10px">Marcá con el círculo la opción correcta.</p><div id="qz">${quizEd()}</div></div>
        <div class="card pad"><div class="sec-h" style="margin:0 0 6px"><h3>Fuentes</h3><button type="button" class="btn ghost sm" id="addSrc">Agregar fuente</button></div>
          <div id="srcs">${l.sources.map((s, i) => `<div class="src-ed" data-si="${i}"><input data-s="label" value="${esc(s.label)}" placeholder="Descripción"><input data-s="url" value="${esc(s.url)}" placeholder="https://…"><button type="button" class="mini del" data-dels="${i}">Quitar</button></div>`).join("")}</div></div>
        <div class="card pad"><h3>La charla <small>Opcional. Una línea por intervención: <code>A:</code> Lucía, <code>B:</code> Martín.</small></h3>
          <textarea id="chat" rows="10">${esc(l.script.map(x => `${x.s}: ${x.t}`).join("\n"))}</textarea></div>
      </form>`);
    const mark = () => { d.dirty = true; $("#dirty").hidden = false; };
    const f = $("#lf2");
    f.addEventListener("input", e => {
      const t = e.target;
      if (t.dataset.f) l[t.dataset.f] = t.value;
      else if (t.dataset.idea) { l.idea_md = l.idea_md || []; l.idea_md[+t.dataset.idea] = t.value; }
      else if (t.dataset.lab) { l.lab[t.dataset.lab] = t.dataset.lab === "minutes" ? (t.value === "" ? null : +t.value) : t.value; if (t.dataset.lab === "md") $("#prev").innerHTML = mdBlock(m, t.value); }
      else if (t.dataset.q) l.quiz[+t.closest("[data-qi]").dataset.qi][t.dataset.q] = t.value;
      else if (t.dataset.opt) { const q = l.quiz[+t.closest("[data-qi]").dataset.qi]; q.options[+t.dataset.opt] = t.value; }
      else if (t.type === "radio") l.quiz[+t.closest("[data-qi]").dataset.qi].answer = +t.value;
      else if (t.dataset.s) l.sources[+t.closest("[data-si]").dataset.si][t.dataset.s] = t.value;
      else if (t.id === "chat") l.script = t.value.split("\n").map(x => x.match(/^\s*([AB])\s*:\s*(.+)$/)).filter(Boolean).map(x => ({s: x[1], t: x[2].trim()}));
      mark();
    });
    f.addEventListener("change", e => { if (e.target.type === "radio") { l.quiz[+e.target.closest("[data-qi]").dataset.qi].answer = +e.target.value; mark(); } });
    // posición del cursor: si nunca se tocó el texto, se agrega al final
    let caret = null;
    ["click", "keyup", "select"].forEach(ev => $("#labMd").addEventListener(ev, e => { caret = [e.target.selectionStart, e.target.selectionEnd]; }));
    const insertAt = txt => {
      const ta = $("#labMd"); const [a, b] = caret || [ta.value.length, ta.value.length];
      caret = [a + txt.length, a + txt.length];
      ta.value = ta.value.slice(0, a) + txt + ta.value.slice(b); ta.selectionStart = ta.selectionEnd = a + txt.length;
      ta.dispatchEvent(new Event("input", {bubbles: true})); ta.focus();
    };
    $("#insF").addEventListener("change", async e => {
      const f0 = e.target.files[0]; e.target.value = ""; if (!f0) return;
      if (!MEDIA_OK.test(f0.type)) { toast("Formato no admitido."); return; }
      const st = $("#insS");
      try {
        const f = await shrink(f0);
        if (f.size > LIMIT(f.type) * 1024 * 1024) throw new Error(`El archivo pesa más de ${LIMIT(f.type)} MB.`);
        const fd = new FormData(); fd.append("curso", slug); fd.append("leccion", lid(l)); fd.append("inline", "1"); fd.append("imagen", f, f.name || "medio");
        const j = await sendFile(fd, p => { st.textContent = `Subiendo… ${p}%`; });
        const u = j.captura.url; st.textContent = "";
        insertAt(f.type.startsWith("video/") ? `\n\n<video src="${u}" controls muted playsinline preload="metadata"></video>\n\n` : `\n\n![Descripción de la imagen](${u})\n\n`);
        toast("Medio insertado");
      } catch (err) { st.textContent = ""; toast(err.message); }
    });
    $("#insY").onclick = () => {
      const u = $("#insU").value.trim();
      const yt = u.match(/(?:youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/)|youtu\.be\/)([A-Za-z0-9_-]{11})/), vm = u.match(/vimeo\.com\/(?:video\/)?(\d{5,12})/);
      if (!yt && !vm) { toast("Pegá un enlace de YouTube o de Vimeo."); return; }
      const src = yt ? `https://www.youtube-nocookie.com/embed/${yt[1]}` : `https://player.vimeo.com/video/${vm[1]}`;
      insertAt(`\n\n<div class="embed"><iframe src="${src}" title="Video" allow="fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>\n\n`);
      $("#insU").value = "";
    };
    $("#addQ").onclick = () => { l.quiz.push({q: "", options: ["", "", "", ""], answer: 0, why: ""}); mark(); adminLesson(slug, id); };
    $$("[data-delq]").forEach(b => b.onclick = () => { l.quiz.splice(+b.dataset.delq, 1); mark(); adminLesson(slug, id); });
    $("#addSrc").onclick = () => { l.sources.push({label: "", url: ""}); mark(); adminLesson(slug, id); };
    $$("[data-dels]").forEach(b => b.onclick = () => { l.sources.splice(+b.dataset.dels, 1); mark(); adminLesson(slug, id); });
    $("#save").onclick = async () => {
      const b = $("#save"); b.disabled = true; b.textContent = "Guardando…";
      try { await saveDraft(slug); toast("Lección guardada"); adminLesson(slug, id); }
      catch (e) { toast(e.message); b.disabled = false; b.textContent = "Guardar cambios"; }
    };
  }
  window.addEventListener("beforeunload", e => { if (Object.values(drafts).some(d => d.dirty)) { e.preventDefault(); e.returnValue = ""; } });

  /* ---------- router ---------- */
  async function route() {
    const h = decodeURIComponent(location.hash || "#/");
    let m;
    $$(".nav a").forEach(a => a.removeAttribute("aria-current"));
    main.innerHTML = `<div class="wrap loading">Cargando…</div>`;
    capturas.cur = null;
    try {
      if ((m = h.match(/^#\/glosario\/?([\w-]*)/))) await viewGlossary(m[1]);
      else if ((m = h.match(/^#\/curso\/([\w-]+)\/(\d+)\/pdf/))) await viewPrint(m[1], +m[2]);
      else if ((m = h.match(/^#\/curso\/([\w-]+)\/pdf/))) await viewPrint(m[1], 0);
      else if ((m = h.match(/^#\/curso\/([\w-]+)\/(\d+)\/editar/))) await viewLessonEdit(m[1], +m[2]);
      else if ((m = h.match(/^#\/curso\/([\w-]+)\/editar/))) await viewCourseEdit(m[1]);
      else if ((m = h.match(/^#\/curso\/([\w-]+)\/(\d+)/))) await viewLesson(m[1], +m[2]);
      else if ((m = h.match(/^#\/curso\/([\w-]+)/))) await viewCourse(m[1]);
      else if ((m = h.match(/^#\/constancia\/([\w-]+)/))) await viewCert(m[1]);
      else if ((m = h.match(/^#\/buscar\/(.+)/))) { $("#q").value = m[1]; await viewSearch(m[1]); }
      else if (h.startsWith("#/editor")) await viewEditor();
      else if (h.startsWith("#/ingresar")) await viewLogin();
      else if (h.startsWith("#/registro")) await viewRegister();
      else if (h.startsWith("#/cuenta")) await viewAccount();
      else if (h.startsWith("#/admin")) await viewAdmin(h.replace(/^#\/admin\/?/, "").split("/").filter(Boolean).map(decodeURIComponent));
      else if (h.startsWith("#/aprendizaje")) { $('[data-nav="aprendizaje"]').setAttribute("aria-current", "page"); await viewLearning(); }
      else {
        $('[data-nav="home"]').setAttribute("aria-current", "page"); await viewHome();
        if (h.includes("catalogo")) { $("#catalogo")?.scrollIntoView(); return; }
      }
    } catch (err) {
      console.error(err);
      if (err.status === 404) { main.innerHTML = `<div class="wrap page-h"><div class="card empty"><b>Ese curso no existe o todavía no está publicado.</b><a class="btn" href="#/">Ver el catálogo</a></div></div>`; return; }
      main.innerHTML = `<div class="wrap page-h"><div class="card empty"><b>No se pudo cargar esta página.</b>Revisá la conexión y recargá.<br><a class="btn" href="#/">Volver al inicio</a></div></div>`;
    }
    window.scrollTo(0, 0);
    main.focus({preventScroll: true});
  }
  $("#search").addEventListener("submit", e => { e.preventDefault(); const v = $("#q").value.trim(); if (v) location.hash = `#/buscar/${encodeURIComponent(v)}`; });
  window.addEventListener("hashchange", () => { paintHeader(); route(); });
  document.addEventListener("click", e => { const a = e.target.closest('a[href="#/ingresar"],a[href="#/registro"]'); if (a && !/^#\/(ingresar|registro)/.test(location.hash)) { try { sessionStorage.setItem("ies.back", location.hash || "#/"); } catch {} } });
  main.innerHTML = `<div class="wrap loading">Cargando…</div>`;
  session.load().then(route);
})();
