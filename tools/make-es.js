// Build public/es/index.html from public/index.html with a Spanish (Latin American) translation, and cross-link both.
const fs = require("fs"), path = require("path");
const pub = path.join(__dirname, "..", "public");
let h = fs.readFileSync(path.join(pub, "index.html"), "utf8");
const R = [
  ['<html lang="en">', '<html lang="es">'],
  ["<title>Live the Dream Athletics</title>", "<title>Live the Dream Athletics · Español</title>"],
  [`content="Live the Dream Athletics. Player development, the family fund, and the systems behind them. Home of the Power Punch, sold at Dick's Sporting Goods, Amazon and Markwort. We love the game. We're here to help."`,
   `content="Live the Dream Athletics. Desarrollo de peloteros, el fondo familiar y los sistemas detrás. Casa del Power Punch, a la venta en Dick's Sporting Goods, Amazon y Markwort. Amamos el juego. Estamos para ayudar."`],
  [`<meta property="og:description" content="We love the game. We're here to help.">`, `<meta property="og:description" content="Amamos el juego. Estamos para ayudar.">`],
  [`<a href="#push">Power Punch</a><a href="#pillars">What we do</a><a href="https://powerpunchathletics.com/dispatch/">Dispatch</a><a href="/es/">Español</a>`, `<a href="#push">Power Punch</a><a href="#pillars">Qué hacemos</a><a href="/">English</a>`],
  [`<a href="#push">Power Punch</a><a href="#pillars">What we do</a><a href="https://powerpunchathletics.com/dispatch/">Dispatch</a>`, `<a href="#push">Power Punch</a><a href="#pillars">Qué hacemos</a><a href="/">English</a>`],
  [`aria-label="Switch light or dark">Light</button>`, `aria-label="Cambiar claro u oscuro">Claro</button>`],
  [`<span class="eyebrow">Live the Dream Athletics · since 2001</span>`, `<span class="eyebrow">Live the Dream Athletics · desde 2001</span>`],
  [`<h1>We love the game. <span>We're here to help.</span></h1>`, `<h1>Amamos el juego. <span>Estamos para ayudar.</span></h1>`],
  [`Player development, a family fund, and the systems behind them. Built by a pro hitter, for the next generation.`, `Desarrollo de peloteros, un fondo familiar y los sistemas detrás. Construido por un bateador profesional, para la próxima generación.`],
  [`<span class="tag">From grassroots to the next level.</span>`, `<span class="tag">De la base al siguiente nivel.</span>`],
  [`<span class="eyebrow">The flagship · on shelves nationwide</span>`, `<span class="eyebrow">El producto insignia · en tiendas de todo EE. UU.</span>`],
  [`<h2>Power Punch. <span>Sold at Dick's Sporting Goods.</span></h2>`, `<h2>Power Punch. <span>A la venta en Dick's Sporting Goods.</span></h2>`],
  [`One strap that fixes bar arm for hitters, holds the slot for pitchers, keeps fielders low and catchers quiet. Adult and Youth.`, `Una banda que corrige el brazo rígido del bateador, sostiene el ángulo del lanzador, mantiene bajo al infielder y quieto al receptor. Adulto y juvenil.`],
  [`<span class="rline">In stock. Ships, free store pickup, same-day delivery.</span>`, `<span class="rline">En stock. Envío, recogida gratis en tienda, entrega el mismo día.</span>`],
  [`<span class="rline">Adult and Youth.</span>`, `<span class="rline">Adulto y juvenil.</span>`],
  [`<span class="rgo">Buy at Dick's &rarr;</span>`, `<span class="rgo">Comprar en Dick's &rarr;</span>`],
  [`<span class="rline">The manufacturer. Teams and dealers.</span>`, `<span class="rline">El fabricante. Equipos y distribuidores.</span>`],
  [`<span class="rline">Markwort Power Punch, Adult and Youth.</span>`, `<span class="rline">Markwort Power Punch, adulto y juvenil.</span>`],
  [`rel="noopener">Dick's Youth</a>`, `rel="noopener">Dick's juvenil</a>`],
  [`<a class="btn" href="https://powerpunchathletics.com/">The Power Punch site</a>`, `<a class="btn" href="https://powerpunchathletics.com/">Sitio de Power Punch</a>`],
  [`<a class="btn" href="https://powerpunchathletics.com/founder">Who it helps</a>`, `<a class="btn" href="https://powerpunchathletics.com/founder">A quién ayuda</a>`],
  [`Retailer names are theirs. Power Punch is sold there under the Markwort label. The 2026 founder's run pre-orders on powerpunchathletics.com.`, `Los nombres de las tiendas son de ellas. Power Punch se vende allí bajo la marca Markwort. La serie fundadora 2026 se reserva en powerpunchathletics.com.`],
  [`<span class="eyebrow">What we do</span>`, `<span class="eyebrow">Qué hacemos</span>`],
  [`<h2>Three systems. <span>One job.</span></h2>`, `<h2>Tres sistemas. <span>Un solo trabajo.</span></h2>`],
  [`<span class="state live">Live</span><h3>Player development</h3><p>Pro-grade tools and drills for the kid who gets overlooked.</p>`, `<span class="state live">Activo</span><h3>Desarrollo de peloteros</h3><p>Herramientas y ejercicios de nivel profesional para el chico que nadie mira.</p>`],
  [`<li>Power Punch, on shelves since the 2000s</li><li>Pure 3s for basketball, next</li><li>Founder's run: 500 numbered straps with a training record</li>`, `<li>Power Punch, en tiendas desde los 2000</li><li>Pure 3s para baloncesto, lo próximo</li><li>Serie fundadora: 500 bandas numeradas con registro de entrenamiento</li>`],
  [`<span class="state">In build</span><h3>The family fund and passports</h3><p>Money that reaches a family fast and in the open. A record a scout can trust.</p>`, `<span class="state">En construcción</span><h3>El fondo familiar y los pasaportes</h3><p>Dinero que llega a una familia rápido y a la vista. Un registro en el que un scout puede confiar.</p>`],
  [`<li>Equipment and travel grants, settled on-chain the day they're approved</li><li>Verified athlete record: sessions, measurables, milestones</li><li>NIL, in the open, through NIL33</li>`, `<li>Ayudas para equipo y viajes, liquidadas en cadena el día en que se aprueban</li><li>Registro verificado del atleta: sesiones, medidas, hitos</li><li>NIL, a la vista, a través de NIL33</li>`],
  [`<span class="state">In build</span><h3>Events and media</h3><p>Showcases that raise money for kids and facilities, and the archive that remembers them.</p>`, `<span class="state">En construcción</span><h3>Eventos y medios</h3><p>Showcases que recaudan para niños e instalaciones, y el archivo que los recuerda.</p>`],
  [`<li>The Dugout Dispatch, live now</li><li>Community showcases and clinics</li><li>The vault: every event, every clip, preserved</li>`, `<li>The Dugout Dispatch, ya en línea</li><li>Showcases y clínicas comunitarias</li><li>La bóveda: cada evento, cada clip, preservado</li>`],
  [`<span class="eyebrow">The next generation</span>`, `<span class="eyebrow">La próxima generación</span>`],
  [`Wyatt Olsen, Beloit, Wisconsin. First player Kevan coached after he retired. Graduation day, at the plaque.`, `Wyatt Olsen, Beloit, Wisconsin. El primer jugador que Kevan entrenó tras retirarse. Día de graduación, frente a la placa.`],
  [`<p class="lede">Not the plaque. The kid who gets past it.</p>`, `<p class="lede">No la placa. El chico que la deja atrás.</p>`],
  [`<a class="btn" href="https://powerpunchathletics.com/founder">The founder</a>`, `<a class="btn" href="https://powerpunchathletics.com/founder">El fundador</a>`],
  [`<footer class="site"><strong>We love the game. We're here to help.</strong>Live the Dream Athletics, founded 2001 by Kevan Burns. Power Punch and Pure 3s are Live the Dream Athletics products. U.S. Patent No. 6,514,163 (expired). Unit records are proof-of-authenticity entries, not securities, and carry no expectation of profit. Train under adult supervision.</footer>`,
   `<footer class="site"><strong>Amamos el juego. Estamos para ayudar.</strong>Live the Dream Athletics, fundada en 2001 por Kevan Burns. Power Punch y Pure 3s son productos de Live the Dream Athletics. Patente de EE. UU. n.º 6,514,163 (vencida). Los registros de unidad son constancias de autenticidad, no valores, y no prometen ganancia alguna. Entrenar bajo supervisión adulta.</footer>`],
  [`btn.textContent = current()==="dark" ? "Light" : "Dark";`, `btn.textContent = current()==="dark" ? "Claro" : "Oscuro";`],
  [`aria-label="Listen to this page"><span class="dot"></span><span class="lbl">Listen</span></button><small>2 minutes · English narration</small>`, `aria-label="Escuchar esta página"><span class="dot"></span><span class="lbl">Escuchar</span></button><small>2 minutos · narración en español</small>`],
  [`src="/audio/ltda-en.mp3"`, `src="/audio/ltda-es.mp3"`],
  [`txt=lbl.textContent, stop="Stop";`, `txt=lbl.textContent, stop="Detener";`],
];
let miss = 0;
for (const [a, b] of R) { if (!h.includes(a)) { miss++; } h = h.split(a).join(b); }
const HREF = `<link rel="alternate" hreflang="en" href="https://livethedreamathletics.com/"><link rel="alternate" hreflang="es" href="https://livethedreamathletics.com/es/"><link rel="icon"`;
if (!h.includes('hreflang="es"')) h = h.replace('<link rel="icon"', HREF);
fs.mkdirSync(path.join(pub, "es"), { recursive: true });
fs.writeFileSync(path.join(pub, "es", "index.html"), h);
// English page: add the Español link and hreflang once
let e = fs.readFileSync(path.join(pub, "index.html"), "utf8");
if (!e.includes('href="/es/"')) e = e.replace(`<a href="https://powerpunchathletics.com/dispatch/">Dispatch</a>`, `<a href="https://powerpunchathletics.com/dispatch/">Dispatch</a><a href="/es/">Español</a>`);
if (!e.includes('hreflang="es"')) e = e.replace('<link rel="icon"', HREF);
fs.writeFileSync(path.join(pub, "index.html"), e);
console.log("translation misses (expected 1: the nav variant not present):", miss, "| es bytes:", h.length, "| en has es link:", e.includes('href="/es/"'));
