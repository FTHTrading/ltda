// ADR-0002 copy gate. Run before every deploy:  node tools/copy-gate.js   (exit 1 on a hit)
// Flags forbidden phrases in public/**/*.html. A hit inside a plain negation ("not a coin", "never sold") is allowed,
// because saying what the record is NOT is exactly what ADR-0001 asks for.
const fs = require("fs"), path = require("path");
const pub = path.join(__dirname, "..", "public");
const FORBIDDEN = [
  /\bcoin\b/i, /token value/i, /earn crypto/i, /airdrop/i, /floor price/i, /\bto the moon\b/i, /\breturns\b/i, /appreciate/i,
  /\bguaranteed\b/i, /revolutionary/i, /game-changing/i, /best-selling/i, /top rated/i, /as seen on/i, /\b#1\b/,
  /limited time/i, /only \d+ left/i, /act now/i,
  /tax-deductible/i, /\bcharity\b/i, /\bnonprofit\b/i, /501\(c\)/i,
  /pure shooter/i, /patent pending/i, /patent-pending/i,
  /BitGo/i, /UNYKORN 7777/i, /TROPTIONS/i, /2549008J7LUHSQ73SI26/i, /\bUBEC\b/,
];
const NEGATION = /\b(not|never|no|isn['’]t|aren['’]t|nothing)\b[^.;]{0,70}$/i;

function walk(d) { return fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith(".html") ? [path.join(d, e.name)] : []); }
let hits = 0;
for (const f of walk(pub)) {
  const raw = fs.readFileSync(f, "utf8").replace(/data:[a-z/+.-]+;base64,[A-Za-z0-9+/=]+/g, "").replace(/<script[\s\S]*?<\/script>/g, "").replace(/<style[\s\S]*?<\/style>/g, "");
  const text = raw.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
  for (const re of FORBIDDEN) {
    const g = new RegExp(re.source, re.flags.includes("g") ? re.flags : re.flags + "g");
    let m;
    while ((m = g.exec(text))) {
      const before = text.slice(Math.max(0, m.index - 70), m.index);
      if (NEGATION.test(before)) continue;                       // "not an investment, a coin" -> allowed
      hits++;
      console.log(`HIT  ${path.relative(pub, f)}  "${m[0]}"  …${text.slice(Math.max(0, m.index - 50), m.index + 50)}…`);
    }
  }
}
console.log(hits ? `${hits} hit(s): fix the copy or amend ADR-0002` : "copy gate: clean");
process.exit(hits ? 1 : 0);
