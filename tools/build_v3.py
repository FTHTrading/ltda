"""Live the Dream Athletics, v3: "the new era with the old".

    python tools/build_v3.py site      -> public/  (every v2 page in the v3 look, plus a new home,
                                                    /story/, /athletes/ and /sponsors/)
    python tools/build_v3.py preview   -> preview/ (local only, noindex)

v3 reuses build_v2's page bodies and data, and replaces the shared page template, the nav and the
look (public/v3/site.css layered on public/v2/preview.css). Every page carries the same JSON-LD:
Live the Dream Athletics (2001), founded by Kevan Burns (https://kevan.unykorn.ai/#kevan-burns),
operated by UnyKorn LLC (https://unykorn.ai/#org).

Facts on /story/ and the founder panel come only from data/founder-record.json (a copy of the
canonical record kept in reputation-tools/record.json): VERIFIED and SELF entries render, PENDING
never does. Photos: only stems in V3_PHOTOS publish (see data/intake/2026-11-08-baseball-ltda).
"""
import html, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_v2 as v2  # noqa: E402

ROOT = v2.ROOT
e = html.escape
V3 = "1"
REC = json.load(open(os.path.join(ROOT, "data", "founder-record.json"), encoding="utf-8"))
SRC = REC["sources"]
HUB = REC["person"]["hub"]
PERSON_ID = REC["person"]["id"]
ORG_ID = "https://livethedreamathletics.com/#org"
UNY_ID = "https://unykorn.ai/#org"
V3_PHOTOS = {"kb1-bat", "panama-stadium", "troy-hof-2007"}  # Tier A only

NAV = [("index", "Home"), ("story", "Our story"), ("youth", "Young athletes"), ("athletes", "Athletes · NIL"),
       ("sponsors", "Sponsors"), ("collection", "The collection"), ("people", "The people")]
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800'
         '&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">')

JSONLD = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "SportsOrganization", "@id": ORG_ID, "name": "Live the Dream Athletics",
         "url": "https://livethedreamathletics.com", "foundingDate": "2001", "sport": "Baseball",
         "founder": {"@id": PERSON_ID}, "parentOrganization": {"@id": UNY_ID},
         "sameAs": ["https://nil33.com", "https://www.youtube.com/@kevanburns3675"]},
        {"@type": "Person", "@id": PERSON_ID, "name": "Kevan Burns", "url": HUB,
         "sameAs": [REC["person"]["linkedin"], SRC["bref"]["url"], SRC["patent"]["url"]]},
        {"@type": "Organization", "@id": UNY_ID, "name": "UnyKorn LLC", "url": "https://unykorn.ai",
         "foundingDate": "2026-07-01", "founder": {"@id": PERSON_ID}},
    ],
}


def img(t, stem, alt, cls=""):
    """v3 photo: published only when cleared (Tier A)."""
    if not t.preview and stem not in V3_PHOTOS:
        return f'<div class="ph pending {cls}"><span class="mono">Photo coming once everyone in it says yes</span></div>'
    w, h = PHOTO_SIZE.get(stem, (1600, 1200))
    return f'<figure class="ph {cls}"><img src="/media/v3/{e(stem)}.jpg" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy"></figure>'


PHOTO_SIZE = {"kb1-bat": (960, 485), "panama-stadium": (1600, 1200), "troy-hof-2007": (604, 267)}
LABEL = {"tan2": "Player diary, pt 2", "tan7": "Player diary, pt 7", "tan8": "Player diary, pt 8", "sabr": "SABR journal",
         "kreyche": "SABR talk (video)", "bdn_2007": "Beloit Daily News", "troy_hof": "Troy media guide, p. 74",
         "troy_notes": "Troy game notes", "ihcc_aa": "IHCC All-Americans", "ihcc_rb": "IHCC record book",
         "bref": "Baseball-Reference", "patent": "Google Patents", "uf_box": "Box score", "wsl": "Wisconsin State League",
         "ltda": "Our archive", "dicks": "Dick's", "markwort": "Markwort", "wyobiz": "Wyoming SOS", "fldfs": "Florida DFS",
         "youtube": "YouTube", "octagon": "Octagon newsletter"}


def src_links(keys):
    return " ".join(f'<a class="chip src" href="{e(SRC[k]["url"])}" target="_blank" rel="noopener">{e(LABEL.get(k, SRC[k]["name"].split(",")[0]))} ↗</a>'
                    for k in keys if k in SRC and SRC[k]["url"].startswith("https://"))


def page(t, name, title, desc, body, og_image="rod-carew-hillside"):
    nav = "".join(f'<a href="{t.url(p)}"{" aria-current=\"page\"" if p == name else ""}>{label}</a>' for p, label in NAV)
    robots = '<meta name="robots" content="noindex,nofollow">' if t.preview else ""
    flag = '<div class="flag">Local preview · not published</div>' if t.preview else ""
    canonical = f'<link rel="canonical" href="https://livethedreamathletics.com{"/" if name == "index" else "/" + name + "/"}">'
    t.write(name, f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://livethedreamathletics.com/media/{og_image}.jpg">
{canonical}
{robots}
<link rel="icon" href="/media/ltd-logo.png">
{FONTS}
<link rel="stylesheet" href="/v2/preview.css?v={v2.V}">
<link rel="stylesheet" href="/v3/site.css?v={V3}">
<script type="application/ld+json">{json.dumps(JSONLD, separators=(",", ":"))}</script>
</head>
<body data-page="{name}" class="v3">
{flag}
<header class="top"><div class="wrap">
  <a class="brand" href="{t.url('index')}"><img class="mark" src="/media/ltd-logo.png" alt=""><span>Live the Dream<small>Athletics · since 2001</small></span></a>
  <button class="menu" id="menu" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav" aria-label="Main">{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
  <b>Live the Dream Athletics</b>
  <span>We love the game. We're here to help. Since 2001.</span>
  <span class="more">More: <a href="/letter/">The letter</a> · <a href="/nil/">NIL</a> · <a href="/photos/">Photos</a> · <a href="/history/">History</a> · <a href="/international/">International</a> · <a href="/families/">Families</a> · <a href="/fund/">The fund</a> · <a href="/proof/">On chain</a></span>
  <span>Founded by <a href="{HUB}">Kevan Burns</a>. Live the Dream Athletics and <a href="https://nil33.com">NIL33</a> are programs of <a href="https://unykorn.ai">UnyKorn LLC</a> (Wyoming). Gifts, not investments: nothing here is for sale, and no record carries a share of anything.</span>
</div></footer>
<script src="/v2/preview.js?v={v2.V}"></script>
</body>
</html>
""")


def _year(x):
    import re as _re
    m = _re.match(r"(19|20)\d\d", x["year"])
    return int(m.group(0)) if m else None


def entries(era=None):
    """Publishable entries: VERIFIED or SELF, with a real year (a PENDING year never renders), oldest first."""
    rows = [x for x in REC["entries"] if x["status"] in ("VERIFIED", "SELF") and _year(x) and (era is None or x["era"] == era)]
    return sorted(rows, key=_year)


def founder_panel(t):
    facts = [
        ("Troy Trojans Baseball Hall of Fame", "Class of 2007, outfield", ["troy_hof"]),
        ("NJCAA All-American", "Indian Hills CC, 1998 · 19 home runs", ["ihcc_aa", "ihcc_rb"]),
        ("Pro career, 1999–2005", ".306 over 528 games · Diamondbacks and Cardinals organizations", ["bref"]),
        ("Inventor", "U.S. Patent 6,514,163, the Power Punch (granted 2003)", ["patent"]),
    ]
    lis = "".join(f'<li><b>{e(a)}</b><span>{e(b)}</span><span class="srcs">{src_links(k)}</span></li>' for a, b, k in facts)
    return f"""
<section class="founder"><div class="wrap grid2v3">
  <div>
    <div class="kicker">Who started it</div>
    <h2>Kevan Burns, <em>founder.</em></h2>
    <p class="big">A player who made it through the system, then spent the next twenty-five years helping the next ones through it. Every line below links to a record he doesn't control.</p>
    <ul class="facts3">{lis}</ul>
    <div class="btns"><a class="btn solid" href="{HUB}">The full record ↗</a><a class="btn" href="{t.url('story')}">Our story</a></div>
  </div>
  {img(t, "troy-hof-2007", "Framed jerseys and the podium sign for the Troy Baseball Hall of Fame Class of 2007, which lists Kevan Burns, OF, 1999", "tall")}
</div></section>"""


def home(t):
    U = t.url
    then_cards = [
        ("2003 · Tucson", "The pro camp before a record game",
         "We ran the two-day pro camp for the 24 Hours for Africa women's game at Tucson Electric Park, and our coaches worked the game through the night. SABR lists its 127–110 final as the record for a planned marathon game.",
         ["tan2", "tan7", "sabr"]),
        ("2007 · Beloit", "A swing turned around",
         "A Beloit player who'd nearly quit worked on his swing with us, then got drafted by the Texas Rangers. In the paper, he said the work was vital to his turnaround.",
         ["bdn_2007"]),
        ("Since 2001", "Gloves, clinics, bridges",
         "Gloves for kids, clinics from Beloit to Panama, players into college and pro ball. Our own archive has the posts, dated as they happened.",
         ["ltda"]),
    ]
    cards = "".join(f'<article class="pcard"><span class="mono tag">{e(a)}</span><h3>{e(b)}</h3><p>{e(c)}</p><div class="srcs">{src_links(k)}</div></article>'
                    for a, b, c, k in then_cards)
    page(t, "index", "Live the Dream Athletics · since 2001",
         "Since 2001: gloves, clinics and bridges for young players, and now fair, open NIL deals through NIL33. A program of UnyKorn LLC.", f"""
<section class="hero3">
  <div class="wrap hero3-in">
    <div class="h3text">
      <div class="kicker mono">Live the Dream Athletics · since 2001</div>
      <h1>The game gave us <em>everything.</em><br>We give it back.</h1>
      <p class="lede">For twenty-five years we've put gloves in kids' hands, run clinics from Beloit to Panama, and helped players reach college and pro ball. Now we do it in the open: fair deals for athletes through NIL33, and records anyone can check.</p>
      <div class="btns"><a class="btn solid" href="{U('youth')}">For families</a><a class="btn" href="{U('athletes')}">For athletes</a><a class="btn" href="{U('sponsors')}">Support a player</a></div>
    </div>
    <div class="thennow" aria-label="Then and now">
      <div class="tn then">{img(t, "kb1-bat", "A wooden bat stamped KB1 Kevan Burns Rideau Crusher, over a ball field")}<span class="mono lbl">Then</span></div>
      <div class="tn now">{img(t, "panama-stadium", "Rod Carew Stadium in Panama, seen from above")}<span class="mono lbl">Now</span></div>
    </div>
  </div>
</section>

<section><div class="wrap">
  <div class="kicker">The old era</div>
  <h2>Twenty-five years, <em>on the record.</em></h2>
  <p class="big narrow">Not what we say about ourselves: what other people wrote down at the time.</p>
  <div class="pcards">{cards}</div>
  <p><a class="more-link" href="{U('story')}">The whole story, then and now →</a></p>
</div></section>

<section class="dark nowband"><div class="wrap">
  <div class="kicker">The new era</div>
  <h2>Same promise. <em>New tools.</em></h2>
  <div class="tiles three">
    <a class="tile big" href="{U('athletes')}"><span class="mono tag">NIL33 · college and pro</span><h3>Fair deals, in the open</h3><p>A flat fee for a set term, in writing, then on a public ledger. No percentage of a player's money, ever.</p></a>
    <a class="tile big" href="{U('youth')}"><span class="mono tag">Under 18 · protected</span><h3>Young athletes first</h3><p>A young player's record belongs to the family. Nothing about a player under 18 is public, and nothing happens without a parent's signature.</p></a>
    <a class="tile big" href="/proof/"><span class="mono tag">Records · on chain</span><h3>Check, don't trust</h3><p>Our history archive is fingerprinted and anchored on a public blockchain, so nobody can quietly change it. Records are history, never a share of anything.</p></a>
  </div>
</div></section>

{founder_panel(t)}

<section class="sponsorband"><div class="wrap split3">
  <div><div class="kicker">Sponsors and donors</div><h2>Help a kid <em>live the dream.</em></h2>
  <p class="big">Gloves, bats, clinic fees, travel for a tryout. Every gift is recorded by purpose. Gifts, not investments.</p></div>
  <div class="btns"><a class="btn solid" href="{U('sponsors')}">How support works</a><a class="btn" href="mailto:kevan@unykorn.org">Talk to us</a></div>
</div></section>

<section class="operator"><div class="wrap">
  <p class="mono">Who runs this today</p>
  <p class="big narrow">Live the Dream Athletics was founded in 2001 by <a href="{HUB}">Kevan Burns</a>. Today it and <a href="https://nil33.com">NIL33</a> are programs of <a href="https://unykorn.ai">UnyKorn LLC</a>, a Wyoming company that builds the records and tools behind them.</p>
</div></section>
""", og_image="v3/panama-stadium")


def story(t):
    def row(x):
        return (f'<li class="srow"><span class="yr">{e(x["year"])}</span><p>{e(x["text"])}</p>'
                f'<span class="srcs">{src_links(x["sources"]) or "<span class=muted>Our own record</span>"}</span></li>')
    builder = "".join(row(x) for x in entries("builder"))
    player = "".join(row(x) for x in entries("player"))
    page(t, "story", "Our story · Live the Dream Athletics",
         "Then and now: twenty-five years of Live the Dream Athletics, each line linked to its source.", f"""
<section class="pagehead"><div class="wrap">
  <div class="kicker mono">Our story</div>
  <h1 class="as-h2">Then, <em>and now.</em></h1>
  <p class="big narrow">The old era was gloves, clinics, camps and phone calls to college coaches. The new era keeps all of that and adds two things the game never had: fair, open deals for athletes, and a record nobody can quietly change. Every line here links to its source.</p>
</div></section>
<section class="tight"><div class="wrap two3">
  <div><h2>The program</h2><ol class="stl">{builder}</ol></div>
  <div><h2>The founder, as a player</h2><ol class="stl">{player}</ol>
  <p class="muted small">Full record and proof wall: <a href="{HUB}">kevan.unykorn.ai</a></p></div>
</div></section>
<section class="tight"><div class="wrap"><p class="muted small">This page is not yet in the anchored archive on Base. It joins at the next re-anchor.</p></div></section>
""")


def athletes(t):
    page(t, "athletes", "For athletes: why NIL33 · Live the Dream Athletics",
         "Why we built NIL33: fair, flat-fee NIL deals for college and pro athletes, in writing and on a public ledger.", f"""
<section class="pagehead dark"><div class="wrap">
  <div class="kicker mono">Athletes · NIL</div>
  <h1 class="as-h2">Why we built <em>NIL33.</em></h1>
  <p class="big narrow">Since July 2025, college athletes can be paid by their schools as well as by brands. That's a lot of new money and a lot of new promises. We've watched players get squeezed for twenty-five years. NIL33 is how our players, coaches and creators take deals without the games.</p>
  <div class="btns"><a class="btn solid" href="https://nil33.com">Go to NIL33 ↗</a><a class="btn" href="https://nil33.com/ledger">See the ledger ↗</a></div>
</div></section>
<section><div class="wrap split2">
  <div><div class="kicker">The rules</div><h2>Four rules. <em>No exceptions.</em></h2>
  <p class="big">These are the same rules on every deal, printed before anyone signs.</p></div>
  <ul class="rules">
    <li><b>Flat fee or unpaid</b><span>A set fee for a set term, or unpaid and disclosed.</span></li>
    <li><b>No percentage, ever</b><span>No commissions, no revenue share, no cut of a player's money.</span></li>
    <li><b>Signed, then public</b><span>Every countersigned agreement goes on a ledger anyone can read.</span></li>
    <li><b>A parent's signature</b><span>Under 18, nothing happens without one.</span></li>
  </ul>
</div></section>
<section class="tight"><div class="wrap">
  <blockquote class="pull"><p>Our generation knows what we went through. Now it's our turn to look out for the ones coming up.</p><footer class="mono">Kevan Burns · founder · <a href="{HUB}">his record</a></footer></blockquote>
</div></section>
""")


def sponsors(t):
    page(t, "sponsors", "Sponsors and donors · Live the Dream Athletics",
         "What support pays for at Live the Dream Athletics, and how every gift is recorded. Gifts, not investments.", f"""
<section class="pagehead"><div class="wrap">
  <div class="kicker mono">Sponsors and donors</div>
  <h1 class="as-h2">What your help <em>buys.</em></h1>
  <p class="big narrow">The same things it bought in 2001: a glove that fits, a clinic a family can't afford, a bus ticket to a tryout. What's new is that you can see where it went.</p>
</div></section>
<section class="tight"><div class="wrap">
  <div class="tiles three">
    <div class="tile"><span class="mono tag">Gear</span><h3>Gloves and bats</h3><p>Equipment drives at home and to Panama and Cuba.</p></div>
    <div class="tile"><span class="mono tag">Coaching</span><h3>Clinics and camps</h3><p>Instruction from people who played the game at a high level.</p></div>
    <div class="tile"><span class="mono tag">Bridges</span><h3>A shot at the next level</h3><p>Travel to tryouts and showcases, and calls to college coaches.</p></div>
  </div>
</div></section>
<section class="tight"><div class="wrap split2">
  <div><h2>How it's <em>recorded.</em></h2>
  <p class="big">Gifts go into the Family Fund and come out as grants to vendors, by purpose, on a public ledger. The fund is being set up: its ledger shows no entries yet, and we'll say so until it does.</p></div>
  <ul class="rules">
    <li><b>Gifts, not investments</b><span>Nothing here is for sale, and no gift buys a share of anything.</span></li>
    <li><b>Badges have no cash value</b><span>Supporter badges say thank you. They can't be sold or traded.</span></li>
    <li><b>Talk to a person</b><span><a href="mailto:kevan@unykorn.org">kevan@unykorn.org</a></span></li>
  </ul>
</div></section>
""")


LLMS = f"""# Live the Dream Athletics

> A youth baseball program founded in 2001 by Kevan Burns: gloves for kids, clinics from Beloit to Panama, and players into college and pro ball. Today Live the Dream Athletics and NIL33 (fair, flat-fee NIL deals for athletes) are programs of UnyKorn LLC (Wyoming).

## Who
- Founder: Kevan Burns. Full sourced record: {HUB}
- Operator today: UnyKorn LLC, https://unykorn.ai
- Athlete side: NIL33, https://nil33.com

## Outside records of the program
- 2003 pro camp before the Tucson 24-hour women's game: {SRC['tan2']['url']} and {SRC['sabr']['url']}
- 2007 Beloit Daily News, a drafted player credits his swing work with Kevan: {SRC['bdn_2007']['url']}

## Founder record (outside sources)
- Troy Trojans Baseball Hall of Fame, Class of 2007: {SRC['troy_hof']['url']}
- NJCAA All-American, Indian Hills CC, 1998: {SRC['ihcc_aa']['url']}
- Pro career 1999-2005: {SRC['bref']['url']}

## What this is not
Not a charity, investment or token. Gifts are not investments; supporter badges have no cash value.
"""


def build(t):
    v2.page = page          # v2 page bodies, v3 shell
    v2.NAV = NAV
    v2.build(t)
    home(t); story(t); athletes(t); sponsors(t)
    if not t.preview:
        open(os.path.join(ROOT, "public", "llms.txt"), "w", encoding="utf-8", newline="\n").write(LLMS)


if __name__ == "__main__":
    build(v2.Target(sys.argv[1] if len(sys.argv) > 1 else "preview"))
