"""Generate the local redesign preview: a short home hub plus one page each for the letter,
the collection (RWA), NIL, the people and the photos.

    python tools/build_preview.py          writes preview/*.html

Shared header/footer live here so the six pages stay in step. Dynamic parts (people cards,
collection records, film strip, contact sheet) are filled by preview/preview.js from our own
data files. Local preview only: noindex, and the intake photos it shows are not cleared to publish.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "preview")
V = "16"  # cache-buster for preview.css / preview.js
COLL = json.load(open(os.path.join(ROOT, "data", "collection", "v2", "manifest.json"), encoding="utf-8"))
BASE = json.load(open(os.path.join(ROOT, "data", "base.json"), encoding="utf-8"))
BASESCAN = "https://basescan.org"

NAV = [("index.html", "Home"), ("letter.html", "The letter"), ("collection.html", "The collection"),
       ("nil.html", "NIL"), ("people.html", "The people"), ("photos.html", "Photos")]
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" '
         'href="https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,500&display=swap">')


def page(name, title, body, data_page):
    nav = "".join(f'<a href="/preview/{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in NAV)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="/preview/media/mark.png">
{FONTS}
<link rel="stylesheet" href="/preview/preview.css?v={V}">
</head>
<body data-page="{data_page}">
<div class="grain" aria-hidden="true"></div>
<div class="flag">Local preview · not published · photos and names wait on each person's yes</div>
<header class="top"><div class="wrap">
  <a class="brand" href="/preview/index.html"><img class="mark" src="/preview/media/mark-light.png" alt=""><span>Live the Dream</span></a>
  <button class="menu" id="menu" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav" aria-label="Main">{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
  <b>Live the Dream Athletics</b>
  <span>We love the game. We're here to help.</span>
  <span>Live the Dream Athletics and NIL33 are programs of UnyKorn LLC (Wyoming). Records are history, not investments: nothing here is for sale, and no record carries a share of anything.</span>
</div></footer>
<script src="/preview/preview.js?v={V}"></script>
</body>
</html>
"""
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


def short(h):
    return h[:10] + "…" + h[-6:]


# ---------------------------------------------------------------- HOME (hub)
page("index.html", "Live the Dream Athletics", f"""
<section class="hero photo" aria-label="Live the Dream Athletics" style="background-image:linear-gradient(90deg,rgba(19,33,58,.96) 0%,rgba(19,33,58,.82) 48%,rgba(19,33,58,.35) 100%),url(/preview/media/rod-carew-hillside.duo.jpg)">
  <div class="wrap">
    <div class="kicker mono">Live the Dream Athletics · since 2001</div>
    <h1>For the love<br>of the <em>game.</em></h1>
    <p class="lede">Twenty-five years of gloves for kids, clinics from Beloit to Panama, and players into college and pro ball. Now we build two things the game never had: a permanent record of its history, and fair deals for the players who make it.</p>
    <div class="btns"><a class="btn solid" href="/preview/collection.html">The collection</a><a class="btn" href="/preview/nil.html">NIL</a></div>
    <p class="mono herocap">Rod Carew Stadium · Panama</p>
  </div>
</section>

<section><div class="wrap">
  <div class="kicker">What we build</div>
  <h2>Two things. <em>Done right.</em></h2>
  <div class="tiles two">
    <a class="tile big" href="/preview/collection.html">
      <span class="mono tag">RWA · real-world records</span>
      <h3>The collection</h3>
      <p>Bats, jerseys, scrapbooks and photos from the game, each with a record: its story, where the original is kept, and a fingerprint written to a public blockchain so nobody can quietly change it. A record is history, never a share of anything.</p>
      <span class="state live">33 records anchored</span> <span class="state build">6 pieces being finished</span>
    </a>
    <a class="tile big" href="/preview/nil.html">
      <span class="mono tag">NIL · name, image, likeness</span>
      <h3>Fair deals for players</h3>
      <p>For college and pro players: endorsement deals at a flat fee, in writing, on a public ledger. No percentage of a player's money. Under 18, nothing happens without a parent's signature.</p>
      <span class="state live">Ledger live</span> <span class="state build">ID check in build</span>
    </a>
  </div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="kicker">Start here</div>
  <div class="tiles three">
    <a class="tile" href="/preview/letter.html"><span class="mono tag">The letter</span><h3>Five dollars and a bus ticket</h3><p>Why the founder is still in the game.</p></a>
    <a class="tile" href="/preview/people.html"><span class="mono tag">The people</span><h3>Who shaped it</h3><p>Coaches, mentors and players, in our own words.</p></a>
    <a class="tile" href="/preview/photos.html"><span class="mono tag">Photos</span><h3>Every frame kept</h3><p>Twenty-five years, frame by frame.</p></a>
  </div>
</div></section>
""", "home")

# ---------------------------------------------------------------- LETTER
page("letter.html", "The letter · Live the Dream Athletics", """
<section id="letter"><div class="wrap letter">
  <figure>
    <div class="pic"><img src="/preview/media/b01.orig.jpg" alt="Kevan Burns, black and white portrait"></div>
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
""", "letter")

# ---------------------------------------------------------------- COLLECTION (RWA)
hist_tx = BASE["txs"]["anchorHistory"]
page("collection.html", "The collection · Live the Dream Athletics", f"""
<section class="hero small" aria-label="The collection"><div class="wrap">
  <div class="kicker mono">The collection · RWA</div>
  <h1>Real things. <em>Real records.</em></h1>
  <p class="lede">RWA means real-world assets. For us it means real-world records: a bat, a jersey, a scrapbook page, each with its story, where the original is kept, and a fingerprint written to a public blockchain. A record proves history. It is never a share of anything, and nothing here is for sale.</p>
</div></section>

<div class="bat" role="img" aria-label="A wooden game bat, with Kevan's son on the field below it">
  <img src="/preview/media/b12.orig.jpg" alt="">
  <div class="wrap"><p class="mono">LTDA-001 · my bat, my son below it</p><p class="batline">Passed <em>down.</em></p></div>
</div>

<section id="collection"><div class="wrap">
  <div class="kicker">The pieces</div>
  <h2>Six pieces, <em>being finished.</em></h2>
  <div class="records" id="records"></div>
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
    <div class="hash"><span class="mono tag">Being finished · 6 pieces</span><br>Collection v2 root {short(COLL["merkleRoot"])}<br>Anchors once every story is complete and everyone pictured has said yes.</div>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="kicker">Add to the collection</div>
  <h2>Have a piece <em>of the game?</em></h2>
  <p style="max-width:680px">A ball, a glove, a scorebook, a photo. Send it with its story. We fingerprint it, record where it's kept, and add it to the next bundle. You keep the piece.</p>
  <div class="btns"><a class="btn solid" href="mailto:kevan@unykorn.org?subject=A%20piece%20for%20the%20collection">Send a piece</a></div>
</div></section>
""", "collection")

# ---------------------------------------------------------------- NIL
page("nil.html", "NIL · Live the Dream Athletics", """
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
    <article><span class="state live">Live</span><h3>A parent's signature</h3><p>Under 18, nothing happens without a parent's signature.</p></article>
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
""", "nil")

# ---------------------------------------------------------------- PEOPLE
page("people.html", "The people · Live the Dream Athletics", """
<section class="hero small" aria-label="The people"><div class="wrap">
  <div class="kicker mono">In the frame</div>
  <h1>The people who <em>shaped it.</em></h1>
  <p class="lede">Coaches, mentors and players from twenty-five years in the game. Each card says how we know them, in our own words, next to public facts with their sources.</p>
</div></section>
<section id="frame" class="dark"><div class="wrap">
  <div class="people" id="people"></div>
  <p class="disclaim" style="opacity:.9">And so many more. Played with us, coached with us, have a photo? <a href="mailto:kevan@unykorn.org?subject=In%20the%20frame">Send it</a>, and with your yes it joins the record.</p>
  <p class="disclaim">Names, teams and organizations appear to tell our history. Nobody listed here endorses Live the Dream Athletics, NIL33 or UnyKorn LLC. Team names belong to their owners.</p>
</div></section>
""", "people")

# ---------------------------------------------------------------- PHOTOS
page("photos.html", "Photos · Live the Dream Athletics", """
<section class="hero small" aria-label="Photos"><div class="wrap">
  <div class="kicker mono">Photos</div>
  <h1>Every frame <em>kept.</em></h1>
  <p class="lede">Phone photos and film prints from the fields we've worked. Hover a frame for the original colour.</p>
</div>
  <div class="strip">
    <div class="sprockets" aria-hidden="true"></div>
    <div class="frames" id="frames" role="list"></div>
    <div class="sprockets b" aria-hidden="true"></div>
    <p class="caption" id="caption" aria-live="polite"></p>
  </div>
</section>
<section id="archive"><div class="wrap">
  <div class="kicker">The contact sheet</div>
  <h2>Twenty-five years, <em>frame by frame.</em></h2>
  <div class="sheet" id="sheet"></div>
</div></section>
<section id="logos" class="dark logolab"><div class="wrap">
  <div class="kicker">Logo lab</div>
  <h2>The batter <em>in the D.</em></h2>
  <div class="logos">
    <figure><img src="/preview/media/b31.logo.jpg" alt="Black glossy batter inside a D"><figcaption class="mono">Gloss · made with AI</figcaption></figure>
    <figure><img src="/preview/media/b29.logo.jpg" alt="Silver batter inside a D"><figcaption class="mono">Steel · made with AI</figcaption></figure>
    <figure><img src="/preview/media/b28.logo.jpg" alt="Batter in a D with blue pixels and live the dream text"><figcaption class="mono">Pixel · made with AI</figcaption></figure>
    <figure class="wide"><img src="/preview/media/b30.logo.jpg" alt="Live The Dream athletics, Est. 2001, script logo over a ballpark"><figcaption class="mono">Est. 2001 · made with AI</figcaption></figure>
  </div>
</div></section>
""", "photos")

print("built", len(NAV), "pages into", OUT)
