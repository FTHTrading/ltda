"""Live the Dream Athletics, v2 design: a short home hub plus the letter, the collection (RWA),
NIL, the people and the photos.

    python tools/build_v2.py preview   -> preview/*.html   local only, every intake photo, noindex
    python tools/build_v2.py site      -> public/ (/, /letter/, /collection/, /nil/, /people/, /photos/)

Everything (people cards, collection records, film strip, contact sheet) is rendered here as static HTML
with every data string escaped; preview.js only runs the phone menu and the film-strip captions.

The site target publishes ONLY photos in SITE_PHOTOS (already public, or Kevan's own portrait and logos).
Any other photo renders as a "photo coming" panel until the people in it have said yes; adding a stem to
SITE_PHOTOS is the one-line change that publishes it. People appear on the site only when Kevan has given
how he knows them (relationship not "to come").
"""
import html, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = "18"
SITE_PHOTOS = {
    "rod-carew-hillside", "panama-rod-carew-rail", "coach-cage", "dugout",   # already on the live site
    "b01",                                                                   # Kevan's own portrait
}
PENDING_YES = "b12 b15 b03 b02 b26 b22".split()  # collection photos: Kevan's family; waiting on his yes
LOGOS = ["b31", "b29", "b28", "b30"]
COLL = json.load(open(os.path.join(ROOT, "data", "collection", "v2", "manifest.json"), encoding="utf-8"))
SRC = json.load(open(os.path.join(ROOT, "data", "collection", "records.src.json"), encoding="utf-8"))
PEOPLE = json.load(open(os.path.join(ROOT, "data", "people.json"), encoding="utf-8"))["people"]
# photo fingerprints come from the committed record files, so a clean checkout builds the same pages
_REC_DIR = os.path.join(ROOT, "data", "collection", COLL["version"], "records")
HASHES = {}
for _it in COLL["items"]:
    _rec = json.load(open(os.path.join(_REC_DIR, os.path.basename(_it["path"])), encoding="utf-8"))
    HASHES[os.path.splitext(_rec["photo"]["intake"])[0]] = {"sha256": _rec["photo"]["sha256"]}
BASE = json.load(open(os.path.join(ROOT, "data", "base.json"), encoding="utf-8"))
BASESCAN = "https://basescan.org"
e = html.escape

FRAMES = [
    ("b03", "Little League", "the scrapbook"), ("b14", "College", "team day"), ("b21", "Pride", "on the field"),
    ("k16", "Spring training", "March 2016"), ("b07", "Pro ball", "mountain ballpark"),
    ("rod-carew-hillside", "Panama", "Rod Carew Stadium"), ("k01", "Night practice", "team talk"),
]
SITE_FRAMES = [("rod-carew-hillside", "Panama", "Rod Carew Stadium"), ("panama-rod-carew-rail", "Panama", "2018"),
               ("coach-cage", "The cage", "training"), ("dugout", "Dugout", "game day"), ("b01", "The founder", "today")]
SHEET = [
    ("b04", "Scrapbook · team"), ("b13", "College days"), ("b14", "College · team day"), ("b07", "Pro ball"),
    ("b17", "Teammates"), ("b18", "Minor league blues"), ("b20", "Pride"), ("b21", "Pride · a young fan"),
    ("b19", "Old friends"), ("b06", "Ballpark lineup"), ("b23", "Gear day"), ("b24", "The poster wall"),
    ("b16", "Locker room"), ("b05", "Hotel lobby"), ("b08", "Night out"), ("b25", "The crew"), ("b09", "The office"),
    ("coach-cage", "The cage"), ("dugout", "Dugout"), ("rod-carew-hillside", "Panama · Rod Carew"),
    ("panama-rod-carew-rail", "Panama · 2018"), ("k12", "Summer ball · on film"), ("k16", "Spring training · 2016"),
    ("k17", "Spring training · 2016"), ("k02", "Clinic"), ("k03", "Clinic · the group"), ("k01", "Night practice"),
    ("k06", "Atlanta ballpark"), ("k05", "Tropicana Field"), ("k04", "Warning track"), ("k07", "Under the lights"),
    ("k15", "Shoe day"), ("k13", "Octagon · baseball"), ("k11", "The arena wall"), ("k10", "Signing day"),
    ("k18", "Studio"), ("k09", "Night out"), ("k08", "Teammates"), ("k14", "The track"),
]


def short(h):
    return h[:10] + "…" + h[-6:]


class Target:
    def __init__(self, name):
        self.name = name
        self.preview = name == "preview"
        self.out = os.path.join(ROOT, "preview" if self.preview else "public")
        self.media = "/preview/media/" if self.preview else "/media/v2/"
        self.static = "/preview/" if self.preview else "/v2/"

    def url(self, page):  # page: "index", "letter", ...
        if self.preview:
            return f"/preview/{page}.html"
        return "/" if page == "index" else f"/{page}/"

    def ok(self, stem):
        return self.preview or stem in SITE_PHOTOS

    def write(self, page, text):
        path = os.path.join(self.out, "index.html") if (page == "index") else (
            os.path.join(self.out, page + ".html") if self.preview else os.path.join(self.out, page, "index.html"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)


NAV = [("index", "Home"), ("letter", "The letter"), ("collection", "The collection"), ("nil", "NIL"),
       ("youth", "Young athletes"), ("people", "The people"), ("photos", "Photos")]
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" '
         'href="https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,500&display=swap">')


def page(t, name, title, desc, body, og_image="rod-carew-hillside"):
    nav = "".join(f'<a href="{t.url(p)}"{" aria-current=\"page\"" if p == name else ""}>{label}</a>' for p, label in NAV)
    robots = '<meta name="robots" content="noindex,nofollow">' if t.preview else ""
    flag = ('<div class="flag">Local preview · not published · photos and names wait on each person\'s yes</div>'
            if t.preview else "")
    more = "" if t.preview else ('<span class="more">More: <a href="/history/">History</a> · <a href="/international/">International</a> · '
                                 '<a href="/today/">The game today</a> · <a href="/families/">Families</a> · <a href="/fund/">The fund</a> · '
                                 '<a href="/proof/">On chain</a></span>')
    t.write(name, f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://livethedreamathletics.com/media/{og_image}.jpg">
{robots}
<link rel="icon" href="{t.media}mark.png">
{FONTS}
<link rel="stylesheet" href="{t.static}preview.css?v={V}">
</head>
<body data-page="{name}">
<div class="grain" aria-hidden="true"></div>
{flag}
<header class="top"><div class="wrap">
  <a class="brand" href="{t.url('index')}"><img class="mark" src="{t.media}mark-light.png" alt=""><span>Live the Dream</span></a>
  <button class="menu" id="menu" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav" aria-label="Main">{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
  <b>Live the Dream Athletics</b>
  <span>We love the game. We're here to help.</span>
  {more}
  <span>Live the Dream Athletics and NIL33 are programs of UnyKorn LLC (Wyoming). Records are history, not investments: nothing here is for sale, and no record carries a share of anything.</span>
</div></footer>
<script src="{t.static}preview.js?v={V}"></script>
</body>
</html>
""")


def pic(t, stem, alt, cls="pic", single=False):
    if not t.ok(stem):
        return f'<div class="{cls} pending"><span class="mono">Photo coming<br>once everyone in it says yes</span></div>'
    if single:  # one image, original colour, no hover layer
        return f'<div class="{cls}"><img src="{t.media}{e(stem)}.orig.jpg" alt="{e(alt)}"></div>'
    return (f'<div class="{cls}"><img src="{t.media}{e(stem)}.duo.jpg" alt="{e(alt)}" loading="lazy">'
            f'<img class="orig" src="{t.media}{e(stem)}.orig.jpg" alt="" loading="lazy"></div>')


def people_cards(t, limit=None):
    out = []
    for p in PEOPLE:
        if not t.preview and p["relationship"].startswith("How we know him: to come"):
            continue
        srcs = "".join(f'<a class="chip src" href="{e(u)}" target="_blank" rel="noopener">source {i + 1}</a>'
                       for i, u in enumerate(x for x in p.get("fact_sources", []) if x.startswith(("https://", "http://"))))
        chip = '<span class="chip wait">Awaiting yes</span>' if t.preview and not p.get("publish") else ""
        facts = f'<p class="facts">{e(p["public_facts"])}</p>' if p.get("public_facts") else ""
        role = ("In memory · " if p.get("in_memory") else "") + p["group"]
        out.append(f'<article class="person{" memory" if p.get("in_memory") else ""}"><div class="mono role">{e(role)}</div>'
                   f'<h3>{e(p["name"])}</h3><p>{e(p["relationship"])}</p>{facts}<div class="src">{srcs}{chip}</div></article>')
        if limit and len(out) >= limit:
            break
    return "".join(out)


def records(t):
    out = []
    for r in SRC["records"]:
        h = HASHES.get(r["photo"], {}).get("sha256", "")
        fp = (h[:16] + "…" + h[-8:]) if h else "—"
        out.append(f'<article class="rec" tabindex="0">{pic(t, r["photo"], r["title"])[:-6]}<span class="no">{e(r["id"])}</span></div>'
                   f'<div class="body"><h3>{e(r["title"])}</h3><p>{e(r["story"])}</p>'
                   f'<dl><dt>When</dt><dd>{e(r["era"])}</dd><dt>Original</dt><dd>where it\'s kept: to record</dd>'
                   f'<dt>Fingerprint</dt><dd>{fp}</dd></dl>'
                   f'<div class="chips"><span class="chip ok">Fingerprinted</span><span class="chip wait">Being finished</span></div></div></article>')
    return "".join(out)


def frames(t):
    items = FRAMES if t.preview else SITE_FRAMES
    out = []
    for i, (stem, place, when) in enumerate(items):
        out.append(f'<div class="frame{" on" if i == min(3, len(items) - 1) else ""}" tabindex="0" role="listitem" '
                   f'data-cap="{e(place)} · {e(when)} · frame {i + 1:02d}">'
                   f'<div class="pic"><img src="{t.media}{e(stem)}.duo.jpg" alt="{e(place)}, {e(when)}">'
                   f'<img class="orig" src="{t.media}{e(stem)}.orig.jpg" alt=""></div><div class="no">FRAME {i + 1:02d}</div></div>')
    return "".join(out)


def sheet(t):
    out = []
    for stem, cap in SHEET:
        if not t.ok(stem):
            continue
        out.append(f'<figure class="cell" tabindex="0" style="margin:0">{pic(t, stem, cap)}'
                   f'<figcaption class="cap"><span>{e(cap)}</span></figcaption></figure>')
    return "".join(out)


def build(t):
    hist_tx = BASE["txs"]["anchorHistory"]
    U = t.url
    # ------------------------------------------------------------ HOME (hub)
    page(t, "index", "Live the Dream Athletics",
         "For the love of the game, since 2001. A permanent record of the game's history, and fair NIL deals for the players who make it.", f"""
<section class="hero photo" aria-label="Live the Dream Athletics" style="background-image:linear-gradient(90deg,rgba(19,33,58,.96) 0%,rgba(19,33,58,.84) 50%,rgba(19,33,58,.4) 100%),url({t.media}rod-carew-hillside.duo.jpg)">
  <div class="wrap">
    <div class="kicker mono">Live the Dream Athletics · since 2001</div>
    <h1>For the love<br>of the <em>game.</em></h1>
    <p class="lede">Twenty-five years of gloves for kids, clinics from Beloit to Panama, and players into college and pro ball. Now we build two things the game never had: a permanent record of its history, and fair deals for the players who make it.</p>
    <div class="btns"><a class="btn solid" href="{U('collection')}">The collection</a><a class="btn" href="{U('nil')}">NIL</a></div>
    <p class="mono herocap">Rod Carew Stadium · Panama</p>
  </div>
</section>

<section><div class="wrap">
  <div class="kicker">What we build</div>
  <h2>Three things. <em>Done right.</em></h2>
  <div class="tiles three">
    <a class="tile big" href="{U('collection')}">
      <span class="mono tag">RWA · real-world records</span>
      <h3>The collection</h3>
      <p>Bats, jerseys, scrapbooks and photos from the game, each with a record: its story, where the original is kept, and a fingerprint written to a public blockchain so nobody can quietly change it. A record is history, never a share of anything.</p>
      <span><span class="state live">33 records anchored</span> <span class="state build">6 pieces being finished</span></span>
    </a>
    <a class="tile big" href="{U('nil')}">
      <span class="mono tag">NIL · name, image, likeness</span>
      <h3>Fair deals for players</h3>
      <p>For college and pro players: endorsement deals at a flat fee, in writing, on a public ledger. No percentage of a player's money. Under 18, nothing happens without a parent's signature.</p>
      <span><span class="state live">Ledger live</span> <span class="state build">ID check in build</span></span>
    </a>
    <a class="tile big" href="{U('youth')}">
      <span class="mono tag">Under 18 · protected</span>
      <h3>Young athletes</h3>
      <p>A young player's record belongs to the family. Nothing about a player under 18 is public. A recruiter gets the yes or no they asked for, not the file, and only with a parent's okay.</p>
      <span><span class="state build">In design</span></span>
    </a>
  </div>
</div></section>

<section class="nilband dark"><div class="wrap">
  <div class="split2">
    <div>
      <div class="kicker">NIL33</div>
      <h2>Paid in <em>the open.</em></h2>
      <p class="big">Since July 2025, college athletes can be paid by their schools as well as by brands. That's a lot of new money and a lot of new promises. NIL33 is how our players, coaches and creators take deals without the games.</p>
      <div class="btns"><a class="btn solid" href="{U('nil')}">How NIL33 works</a><a class="btn" href="https://nil33.com/ledger">See the ledger</a></div>
    </div>
    <ul class="rules">
      <li><b>Flat fee or unpaid</b><span>A set fee for a set term, or unpaid and disclosed.</span></li>
      <li><b>No percentage, ever</b><span>No commissions, no revenue share, no cut of a player's money.</span></li>
      <li><b>Signed, then public</b><span>Every countersigned agreement goes on a ledger anyone can read.</span></li>
      <li><b>A parent's signature</b><span>Under 18, nothing happens without one.</span></li>
    </ul>
  </div>
  <blockquote class="pull"><p>Our generation knows what we went through. Now it's our turn to look out for the ones coming up.</p><footer class="mono">Kevan Burns · founder</footer></blockquote>
</div></section>

<section><div class="wrap">
  <div class="kicker">Start here</div>
  <div class="tiles three">
    <a class="tile" href="{U('letter')}"><span class="mono tag">The letter</span><h3>Five dollars and a bus ticket</h3><p>Why the founder is still in the game.</p></a>
    <a class="tile" href="{U('people')}"><span class="mono tag">The people</span><h3>Who shaped it</h3><p>Coaches, mentors and players, in our own words.</p></a>
    <a class="tile" href="{U('photos')}"><span class="mono tag">Photos</span><h3>Every frame kept</h3><p>Twenty-five years, frame by frame.</p></a>
  </div>
</div></section>
""")

    # ------------------------------------------------------------ LETTER
    page(t, "letter", "The letter · Live the Dream Athletics",
         "Drafted in the 26th round, signed at his grandmother's house: why Kevan Burns is still in the game.", f"""
<section id="letter"><div class="wrap letter">
  <figure>
    {pic(t, "b01", "Kevan Burns, black and white portrait", single=True)}
    <figcaption class="mono">Kevan Burns · founder</figcaption>
  </figure>
  <div class="body">
    <div class="kicker">A letter from the founder</div>
    <h1 class="as-h2">Why I'm still <em>in the game.</em></h1>
    <p>I was drafted in the 26th round by the Arizona Diamondbacks. Mike Rizzo, years before he ran the Washington Nationals, came to my grandmother's house and signed me right there. Five dollars and a bus ticket. I danced around that kitchen anyway, because I knew exactly what I'd been handed: a shot.</p>
    <p>Baseball has been most of my life ever since. Rick Schu was my hitting coach in the Diamondbacks system, the best I ever had. Later I worked as a player agent at Octagon, hired by Alan Nero, my mentor.</p>
    <p>When I ran the baseball program at Montverde Academy, I hired my college coach from Troy, John Mayotte, as head coach for the season. He and his wife moved onto campus. On Scout Day, Cam Walker, my coach at Indian Hills, came too. For one season, both of my college coaches were on the field with me, running the camp.</p>
    <p>The older you get, the more clearly you see the game you were part of: what it did right, and who it left behind. Most players never make big-league money. Some of the best people in the game are the coaches, the characters and the creators around it, and the game rarely pays them fairly or keeps a straight record of what they were promised.</p>
    <p>That's where this started: making agents and agencies better. Now there's NIL, revenue sharing, and a lot more money moving through the game. So we're building the record for it: the game's history kept where nobody can rewrite it, and players' deals done in the open.</p>
    <p>And above all of it, Jesus. None of this happens without Him.</p>
    <p class="sign">Kevan Burns<small>Founder · Live the Dream Athletics</small></p>
  </div>
</div></section>

<section id="what" class="tight"><div class="wrap">
  <div class="kicker">What we do</div>
  <h2>On the field, <em>since 2001.</em></h2>
  <div class="what">
    <article><span class="state live">Since 2014</span><h3>Gear</h3><p>Gloves, bats, balls and cleats for kids who can't buy them. We shipped equipment to young players in Cuba in 2014 and 2015. Next drive: every box logged from the donor to the coach who signs for it.</p></article>
    <article><span class="state live">Since 2001</span><h3>Coaching</h3><p>Lessons in Beloit, Wisconsin. The baseball program at Montverde Academy. Clinics at MVP Sport City and Rod Carew Stadium in Panama. Showcases where scouts can see kids who'd otherwise be missed.</p></article>
    <article><span class="state build">Opening</span><h3>The family fund</h3><p>Equipment, travel and tournament fees for families who can't cover them. Paid straight to the team or the store, never cash, never a loan. Every grant listed by what it paid for, never by a child's name.</p></article>
  </div>
</div></section>
""", og_image="rod-carew-hillside")

    # ------------------------------------------------------------ COLLECTION (RWA)
    bat = (f"""<div class="bat" role="img" aria-label="A wooden game bat, with Kevan's son on the field below it">
  <img src="{t.media}b12.orig.jpg" alt="">
  <div class="wrap"><p class="mono">LTDA-001 · my bat, my son below it</p><p class="batline">Passed <em>down.</em></p></div>
</div>""" if t.ok("b12") else "")
    page(t, "collection", "The collection · Live the Dream Athletics",
         "Real things, real records: bats, jerseys and scrapbooks from the game, each fingerprinted and anchored on a public blockchain.", f"""
<section class="hero small" aria-label="The collection"><div class="wrap">
  <div class="kicker mono">The collection · RWA</div>
  <h1>Real things. <em>Real records.</em></h1>
  <p class="lede">RWA means real-world assets. For us it means real-world records: a bat, a jersey, a scrapbook page, each with its story, where the original is kept, and a fingerprint written to a public blockchain. A record proves history. It is never a share of anything, and nothing here is for sale.</p>
</div></section>
{bat}
<section id="collection"><div class="wrap">
  <div class="kicker">The pieces</div>
  <h2>Six pieces, <em>being finished.</em></h2>
  <div class="records">{records(t)}</div>
</div></section>

<section class="proof"><div class="wrap">
  <div class="kicker">How a record works</div>
  <h2>Four steps. <em>Check any of them.</em></h2>
  <ol class="steps">
    <li><b>Photograph and story</b><span>The piece is photographed and its story written: what it is, when it's from, who is in it, where the original is kept.</span></li>
    <li><b>Fingerprint</b><span>The record is hashed with SHA-256. Change one letter or one pixel and the fingerprint changes.</span></li>
    <li><b>Bundle</b><span>All the fingerprints combine into one root (a Merkle tree), so one number stands for the whole set.</span></li>
    <li><b>Anchor</b><span>The root is written to Base, a public blockchain. Anyone can rebuild it from the files and match it, without asking us.</span></li>
  </ol>
  <div class="grid2">
    <div class="hash"><span class="mono tag">Already anchored · 33 records</span><br>History archive root {short(BASE["historyRoot"])}<br><a href="{BASESCAN}/tx/{hist_tx}" target="_blank" rel="noopener">anchor tx {short(hist_tx)}</a> · Sept 17, 2026</div>
    <div class="hash"><span class="mono tag">Being finished · 6 pieces</span><br>Collection root {short(COLL["merkleRoot"])} ({e(COLL["version"])})<br>Anchors once every story is complete and everyone pictured has said yes.</div>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="kicker">Add to the collection</div>
  <h2>Have a piece <em>of the game?</em></h2>
  <p style="max-width:680px">A ball, a glove, a scorebook, a photo. Send it with its story. We fingerprint it, record where it's kept, and add it to the next bundle. You keep the piece.</p>
  <div class="btns"><a class="btn solid" href="mailto:kevan@unykorn.org?subject=A%20piece%20for%20the%20collection">Send a piece</a></div>
</div></section>
""")

    # ------------------------------------------------------------ NIL
    page(t, "nil", "NIL · Live the Dream Athletics",
         "NIL33: flat fee or unpaid, no percentage of a player's money, every countersigned deal on a public ledger, a parent's signature under 18.", f"""
<section class="hero small" aria-label="NIL"><div class="wrap">
  <div class="kicker mono">NIL · name, image, likeness</div>
  <h1>Paid in <em>the open.</em></h1>
  <p class="lede">College athletes can be paid for their name, image and likeness, and since July 2025 schools can share revenue with them directly. That's a lot of new money and a lot of new promises. NIL33 is how our players, coaches and creators do it without the games.</p>
  <div class="btns"><a class="btn solid" href="https://nil33.com/apply">Apply to NIL33</a><a class="btn" href="https://nil33.com/ledger">See the ledger</a></div>
</div></section>

<section class="why"><div class="wrap">
  <div class="kicker">Why it matters</div>
  <blockquote>
    <p>Our generation knows what we went through: the handshake deals, the promises nobody wrote down. Now it's our turn to look out for the ones coming up, the way the people before us looked out for us. That's why NIL, and every contract, gets done in the open.</p>
    <footer class="mono">Kevan Burns · founder</footer>
  </blockquote>
</div></section>

<section><div class="wrap">
  <div class="kicker">The rules</div>
  <h2>Five rules. <em>No exceptions.</em></h2>
  <div class="what">
    <article><span class="state live">Live</span><h3>Flat fee or unpaid</h3><p>Every deal is a flat fee for a set term, or unpaid and disclosed. Nothing tied to how much a player earns.</p></article>
    <article><span class="state live">Live</span><h3>No percentage, ever</h3><p>No commissions. No revenue share. No cut of a player's money, and nothing tied to recovered funds.</p></article>
    <article><span class="state live">Live</span><h3>Signed, then public</h3><p>An agreement goes on the public ledger once it's countersigned. Anyone can read the ledger, as a page or as data.</p></article>
    <article><span class="state live">Live</span><h3>A parent's signature</h3><p>Under 18, nothing happens without a parent's signature. <a href="{U('youth')}">How we protect young athletes</a></p></article>
    <article><span class="state build">In build</span><h3>Know who's real</h3><p>Verification for athletes and the people working with them. The ID step waits on a vendor; it is not live yet.</p></article>
  </div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="kicker">Two ways in</div>
  <div class="tiles two">
    <a class="tile" href="https://nil33.com/champions"><span class="mono tag">Paid</span><h3>Champions</h3><p>A flat fee for a set term, approved lines, every placement tagged as paid.</p></a>
    <a class="tile" href="https://nil33.com/ambassadors"><span class="mono tag">Unpaid</span><h3>Ambassadors</h3><p>Coaches, programs, alumni and creators who back the system. No money changes hands, and no exclusivity.</p></a>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="kicker">How it ties together</div>
  <h2>From a kid's first glove <em>to a signed deal.</em></h2>
  <ul class="list">
    <li>The record we build with families when a player is young carries into college and pro.</li>
    <li>Endorsement income stays with the athlete. Nothing is ever borrowed against it.</li>
    <li>The deal and the history sit side by side, both where the player can always find them.</li>
  </ul>
  <p class="mono" style="color:var(--muted);margin-top:18px">Sources: nil33.com rules (read live 2026-10-26); House v. NCAA settlement, approved June 2025.</p>
</div></section>
""")

    # ------------------------------------------------------------ YOUNG ATHLETES
    page(t, "youth", "Young athletes · Live the Dream Athletics",
         "Protection for players under 18: the family controls the record, nothing is public, and recruiters get only the yes or no they asked for.", f"""
<section class="hero small" aria-label="Young athletes"><div class="wrap">
  <div class="kicker mono">Young athletes · under 18</div>
  <h1>Protected until <em>they're ready.</em></h1>
  <p class="lede">Showcases, rankings and recruiting pages can put a kid's height, school, hometown and numbers in front of anyone with a browser. Exposure is good. Exposure to everyone isn't. We're building a record the family controls, so a young player's information reaches the right people and nobody else.</p>
  <div class="btns"><span class="state build">In design: no player data collected yet</span></div>
</div></section>

<section><div class="wrap">
  <div class="kicker">How it works</div>
  <h2>Six promises. <em>Built in, not bolted on.</em></h2>
  <ol class="steps six">
    <li><b>A parent opens it</b><span>Under 18, nothing exists without a parent's signature. At 18, the record passes to the player.</span></li>
    <li><b>Nothing is public</b><span>No public profile for any player under 18. Not a name, not a school, not a hometown.</span></li>
    <li><b>Facts are signed</b><span>The event that timed the sixty signs the time. The coach signs the milestone. Nobody can pad a number.</span></li>
    <li><b>Answers, not files</b><span>A recruiter asks "Is he 16 or older?" or "Under 7.0 in the sixty?" and gets a signed yes or no. Never the birth date, the transcript or the address.</span></li>
    <li><b>The parent approves who asks</b><span>Each coach or program gets access for a set time and a set list of questions. The family can take it back at any time.</span></li>
    <li><b>Every look is logged</b><span>The family sees who asked what, and when. Nobody looks without leaving a mark.</span></li>
  </ol>
</div></section>

<section class="why"><div class="wrap">
  <div class="kicker">Why it matters</div>
  <blockquote>
    <p>We know what we went through. Now we look out for the ones coming up, and the youngest ones first. Their information is for the right people, not for everybody.</p>
    <footer class="mono">Kevan Burns · founder</footer>
  </blockquote>
</div></section>

<section class="dark"><div class="wrap">
  <div class="kicker">Where it fits</div>
  <div class="tiles three">
    <a class="tile" href="{U('index')}"><span class="mono tag">Live the Dream</span><h3>Young players</h3><p>The record starts with families in our programs, clinics and gear drives.</p></a>
    <a class="tile" href="{U('nil')}"><span class="mono tag">NIL33</span><h3>When they're older</h3><p>The same record carries into college and pro NIL, with a parent's signature on anything before 18.</p></a>
    <div class="tile"><span class="mono tag">For programs</span><h3>Showcases and scouts</h3><p>Built to plug into the platforms that already run showcases and recruiting, as a privacy layer for their under-18 players.</p></div>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="kicker">The fine print</div>
  <ul class="list">
    <li>This is in design. No player's information is collected until the parent-consent process has been reviewed by counsel for children's privacy and school-records law.</li>
    <li>Player information stays encrypted and off any blockchain. Only a fingerprint of a signed fact is ever anchored, and it reveals nothing about the player.</li>
    <li>We never sell or license a young player's information. Not to brands, not to scouts, not to anyone.</li>
  </ul>
  <div class="btns" style="margin-top:22px"><a class="btn solid" href="mailto:kevan@unykorn.org?subject=Young%20athletes%20-%20parent%20or%20program">Parents and programs: talk to us</a></div>
</div></section>
""")

    # ------------------------------------------------------------ PEOPLE
    page(t, "people", "The people · Live the Dream Athletics",
         "Coaches, mentors and players who shaped Live the Dream Athletics, in our own words, with public facts and sources.", f"""
<section class="hero small" aria-label="The people"><div class="wrap">
  <div class="kicker mono">In the frame</div>
  <h1>The people who <em>shaped it.</em></h1>
  <p class="lede">Coaches, mentors and players from twenty-five years in the game. Each card says how we know them, in our own words, next to public facts with their sources.</p>
</div></section>
<section id="frame" class="dark"><div class="wrap">
  <div class="people">{people_cards(t)}</div>
  <p class="disclaim" style="opacity:.9">And so many more. Played with us, coached with us, have a photo? <a href="mailto:kevan@unykorn.org?subject=In%20the%20frame">Send it</a>, and with your yes it joins the record.</p>
  <p class="disclaim">Names, teams and organizations appear to tell our history. Nobody listed here endorses Live the Dream Athletics, NIL33 or UnyKorn LLC. Team names belong to their owners.</p>
</div></section>
""")

    # ------------------------------------------------------------ PHOTOS
    logos = "".join(f'<figure{" class=\"wide\"" if s == "b30" else ""}><img src="{t.media}{s}.logo.jpg" alt="Live the Dream logo concept, a batter inside a D">'
                    f'<figcaption class="mono">{n} · made with AI</figcaption></figure>'
                    for s, n in zip(LOGOS, ["Gloss", "Steel", "Pixel", "Est. 2001"]))
    page(t, "photos", "Photos · Live the Dream Athletics",
         "Twenty-five years in the game, frame by frame.", f"""
<section class="hero small" aria-label="Photos"><div class="wrap">
  <div class="kicker mono">Photos</div>
  <h1>Every frame <em>kept.</em></h1>
  <p class="lede">Phone photos and film prints from the fields we've worked. Hover a frame for the original colour. More join as the people in them say yes.</p>
</div>
  <div class="strip">
    <div class="sprockets" aria-hidden="true"></div>
    <div class="frames" id="frames" role="list">{frames(t)}</div>
    <div class="sprockets b" aria-hidden="true"></div>
    <p class="caption" id="caption" aria-live="polite"></p>
  </div>
</section>
<section id="archive"><div class="wrap">
  <div class="kicker">The contact sheet</div>
  <h2>Twenty-five years, <em>frame by frame.</em></h2>
  <div class="sheet">{sheet(t)}</div>
</div></section>
<section id="logos" class="dark logolab"><div class="wrap">
  <div class="kicker">Logo lab</div>
  <h2>The batter <em>in the D.</em></h2>
  <div class="logos">{logos}</div>
</div></section>
""")

    if not t.preview:  # ship the stylesheet, script and only the cleared media
        os.makedirs(os.path.join(t.out, "v2"), exist_ok=True)
        os.makedirs(os.path.join(t.out, "media", "v2"), exist_ok=True)
        for f in ("preview.css", "preview.js"):
            shutil.copyfile(os.path.join(ROOT, "preview", f), os.path.join(t.out, "v2", f))
        src = os.path.join(ROOT, "preview", "media")  # baked locally by tools/preview_media.py (git-ignored)
        keep = [f"{s}.{k}.jpg" for s in SITE_PHOTOS for k in ("duo", "orig")] + \
               [f"{s}.logo.jpg" for s in LOGOS] + ["mark.png", "mark-light.png"]
        dst = os.path.join(t.out, "media", "v2")    # committed: only cleared files ever land here
        for f in os.listdir(dst):  # drop anything no longer cleared
            if f not in keep:
                os.remove(os.path.join(dst, f))
        for f in keep:
            if os.path.exists(os.path.join(src, f)):
                shutil.copyfile(os.path.join(src, f), os.path.join(dst, f))
        missing = [f for f in keep if not os.path.exists(os.path.join(dst, f))]
        if missing:
            sys.exit("missing cleared media (run tools/preview_media.py first): " + ", ".join(missing))
        print("site media:", len(keep), "files")
    print("built", t.name, "->", t.out)


if __name__ == "__main__":
    build(Target(sys.argv[1] if len(sys.argv) > 1 else "preview"))
