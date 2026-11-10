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
V3 = "4"
REC = json.load(open(os.path.join(ROOT, "data", "founder-record.json"), encoding="utf-8"))
SRC = REC["sources"]
HUB = REC["person"]["hub"]
PERSON_ID = REC["person"]["id"]
ORG_ID = "https://livethedreamathletics.com/#org"
UNY_ID = "https://unykorn.ai/#org"
V3_PHOTOS = {"kb1-bat", "panama-stadium", "troy-hof-2007",  # Tier A
             # Tier B, adults in baseball settings: published on Kevan's instruction 2026-11-08 (.forge/founder-flags.md)
             "aces-1996", "at-bat", "on-the-field", "clubhouse", "spring-training", "glove-drive", "shoe-day",
             "camp-talk", "camp-coaching", "teammates"}

NAV = [("index", "Home"), ("story", "The road"), ("youth", "Young athletes"), ("athletes", "Athletes · NIL"),
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


from PIL import Image as _Im
_MEDIA = os.path.join(ROOT, "public", "media", "v3")
PHOTO_SIZE = {os.path.splitext(f)[0]: _Im.open(os.path.join(_MEDIA, f)).size for f in os.listdir(_MEDIA) if f.endswith(".jpg")}
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
<script src="/v3/site.js?v={V3}" defer></script>
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


VIDEOS = [
    ("HeO5W1-Q0uI", "24-Hour for Africa Baseball in Tucson", "Cathy Kreyche, SABR Women in Baseball Conference, 2024. The Live the Dream camp comes up around the ten-minute mark."),
    ("fimBAgZY2W0", "We Care Panhandle", "After Hurricane Michael, Florida Panhandle, 2018."),
    ("JoyGZkk4cpE", "Power Punch baseball", "The original Power Punch series."),
    ("uefRdrX_nFg", "Live The Dream Athletics", "From the early Live the Dream channel."),
]

CHAPTERS = [
    # (where, title, text [sourced], quote, source keys, words [Kevan's own account], photos [(stem, caption)])
    ("Beloit, Wisconsin", "Where it starts",
     "A left-handed outfielder at Beloit Memorial High School. The summer after, playing in the Wisconsin State League against grown men, he was named Rookie of the Year with the Janesville Aces.",
     None, ["bdn_2007", "wsl"],
     "That Aces team was a family: Klawitter and Queeny on the mound, Hawk at third, Campy catching, Hallada at short, Darrel Purdue, Schmitty in right, Coolie. And Houck, who threw me extra BP whenever I asked.",
     [("aces-1996", "Janesville, 1996. The print is dated 9/6/96.")]),
    ("Centerville, Iowa", "Indian Hills",
     "Two years of junior college ball at Indian Hills. In 1998 he hit 19 home runs, still tied for the school's single-season top five, and was named an NJCAA Second Team All-American.",
     None, ["ihcc_aa", "ihcc_rb"],
     "Cam Walker ran the program, Kevin Benzing taught me to hit, Whit ran the bench. In 1998 the whole team went to the JUCO World Series in Grand Junction and finished third. We lost the tiebreak on a flip.",
     [("teammates", "Teammates, behind the cage.")]),
    ("Winchester, Virginia", "Summer ball, 1998",
     "", None, [],
     "Summer of 1998 I played for the Winchester Royals in the Valley League. They called me the fastest man in the Valley.",
     []),
    ("Troy, Alabama", "One season, a long memory",
     "One season in center field for Troy State, a Division I program, for coach John Mayotte. He scored 71 runs, fifth-most in a season in the school's history. In 2007, Troy put him in its Baseball Hall of Fame, in the same class as Coach Mayotte.",
     None, ["uf_box", "troy_notes", "troy_hof"], "",
     [("troy-hof-2007", "Troy Baseball Hall of Fame, Class of 2007. The podium sign lists Kevan Burns, OF, 1999.")]),
    ("Missoula to Winnipeg", "Pro ball, 1999 to 2005",
     "Drafted by the Arizona Diamondbacks in the 26th round. He hit .330 his first pro summer, .361 at High-A Lancaster in 2001, then reached Double-A with El Paso and, with the Cardinals, Tennessee. Independent ball followed at Nashua and Winnipeg. Seven seasons, 528 games, a .306 average.",
     None, ["bref"],
     "Mac Seibert scouted me. Mike Rizzo came to my grandmother's house and signed me. Rick Schu was the best hitting coach I ever had. In 2005 I came out of retirement to play for Winnipeg, with P.J. Connelly, another Beloit kid, on the staff.",
     [("at-bat", "At the plate."), ("on-the-field", "On the field, before a game."), ("clubhouse", "In the clubhouse.")]),
    ("A cheap motel and an idea", "The Power Punch",
     "In 2001, still a minor leaguer, he filed a patent on a batting aid. It was granted in 2003. Years later it reached the shelf at Dick's Sporting Goods under the Markwort label.",
     ("while in the minors, while broke and eating pb&j", "Kevan Burns, in Octagon's employee newsletter"), ["patent", "dicks", "octagon"],
     "", [("kb1-bat", "KB1, the Rideau Crusher.")]),
    ("2001", "Live the Dream Athletics",
     "The same year, he started Live the Dream: gloves for kids who didn't have one, clinics from Beloit to Panama, phone calls to college coaches for players nobody was calling about.",
     None, ["ltda"],
     "When I moved back to Beloit, Eric Olsen, Wyatt's dad, brought me back to the game.",
     [("glove-drive", "Donated gloves, laid out for a clinic."), ("shoe-day", "Shoe day.")]),
    ("Tucson, 2003", "Twenty-four hours for Africa",
     "Seventy-two women came to Tucson Electric Park to play one game for twenty-four straight hours, raising money for US Doctors for Africa. Live the Dream ran the two-day pro camp before it, and its coaches worked the game through the night. SABR lists the 127-110 final as the record for a planned marathon game.",
     ("Kevan Burns was coaching first at that point.", "Cecilia Tan, player's diary, 4 a.m."), ["tan2", "tan7", "tan8", "sabr", "kreyche"],
     "", [("camp-talk", "Camp, the talk before drills."), ("camp-coaching", "Camp, one on one.")]),
    ("Beloit, 2007", "A swing turned around",
     "A local player had hit .153 and nearly walked away from the game. Home in Beloit, he worked on his swing with Kevan. The next spring he raised his average 178 points, and the Texas Rangers drafted him.",
     ("He was vital to my turning it around.", "Kyle Murphy, to the Beloit Daily News"), ["bdn_2007"], "", []),
    ("Inside the game", "Agent, director, mentor",
     "", None, ["octagon"],
     "Alan Nero was my mentor. He hired me at Octagon, and I worked for him in the baseball division as an MLB agent. Later, as director of baseball at Montverde Academy, I hired Coach Mayotte as our head coach, and Cam Walker came down for Scout Day. Both of my college coaches, on one field.",
     [("spring-training", "Spring training, visiting an old coach.")]),
    ("Panama and Cuba", "Bridges",
     "Gear carried to fields that didn't have enough of it. Clinics at Rod Carew Stadium and the fields around it. Players helped toward a shot most people never hear about.",
     None, ["ltda"],
     "Tom Justice, the Gringo, coached with us in Panama. Jesus Hernandez and Noro Padron came to us from Cuba.",
     [("panama-stadium", "Rod Carew Stadium, Panama.")]),
    ("Florida Panhandle, 2018", "After the storm",
     "When Hurricane Michael hit the Florida Panhandle, he went to help the families there. The video is on the channel.",
     None, ["youtube"], "", []),
    ("Now", "The new era",
     "The road ends where it began, with players who need someone in their corner. Today that means NIL33, fair deals at a flat fee with no cut of a player's money, and records anyone can check. UnyKorn LLC, which he founded in 2026, runs both.",
     None, ["wyobiz"], "", []),
]


def story(t):
    chapters = []
    for i, (where, title, text, quote, keys, words, photos) in enumerate(CHAPTERS, 1):
        q = (f'<blockquote class="rq"><p>&ldquo;{e(quote[0])}&rdquo;</p><footer class="mono">{e(quote[1])}</footer></blockquote>' if quote else "")
        w = (f'<div class="words"><span class="mono">As Kevan tells it</span><p>{e(words)}</p></div>' if words else "")
        ph = ""
        if photos:
            figs = "".join(f'<div class="cfig">{img(t, s_, c_)}<p class="cap">{e(c_)}</p></div>' for s_, c_ in photos)
            ph = f'<div class="cph n{len(photos)}">{figs}</div>'
        body = f"<p>{e(text)}</p>" if text else ""
        chapters.append(f'<article class="chap"><div class="cnum mono">{i:02d}</div><div class="cbody">'
                        f'<div class="kicker mono">{e(where)}</div><h2 class="ct">{e(title)}</h2>{body}{q}{w}{ph}'
                        f'<div class="srcs">{src_links(keys)}</div></div></article>')
    vids = "".join(f'<button class="vid3" data-yt="{v}" type="button"><span class="play" aria-hidden="true"></span>'
                   f'<span class="vt">{e(ti)}</span><span class="vm">{e(m)}</span></button>' for v, ti, m in VIDEOS)

    def row(x):
        return (f'<li class="srow"><span class="yr">{e(x["year"])}</span><p>{e(x["text"])}</p>'
                f'<span class="srcs">{src_links(x["sources"]) or "<span class=muted>Our own record</span>"}</span></li>')
    builder = "".join(row(x) for x in entries("builder"))
    player = "".join(row(x) for x in entries("player"))
    page(t, "story", "The road · Live the Dream Athletics",
         "The road from Beloit to Indian Hills, Troy, pro ball, Tucson and Panama, and why Live the Dream exists. Every chapter linked to its source.", f"""
<section class="pagehead"><div class="wrap">
  <div class="kicker mono">The road</div>
  <h1 class="as-h2">The road <em>we travelled.</em></h1>
  <p class="big narrow">Live the Dream wasn't planned in an office. It came out of a road: small towns, bus rides, a few good coaches, a lot of nights when the dream looked done. Here it is, stop by stop, with the people who wrote it down at the time.</p>
</div></section>
<section class="tight"><div class="wrap"><div class="road">{"".join(chapters)}</div></div></section>
<section class="tight"><div class="wrap">
  <div class="kicker">Watch</div><h2>On <em>film.</em></h2>
  <p class="muted small">Videos load from youtube-nocookie.com only when you press play.</p>
  <div class="vids3">{vids}</div>
</div></section>
<section class="tight"><div class="wrap"><div class="kicker">The record</div><h2>Every line, <em>sourced.</em></h2></div></section>
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


LEGACY = ["history", "today", "families", "fund", "systems", "proof", "international", "nil33"]


def legacy_pages(t):
    """Regenerate the build.py pages, then re-emit each one inside the v3 shell so the whole site is one design."""
    import re, subprocess
    subprocess.run([sys.executable, "-I", os.path.join(ROOT, "build.py")], cwd=ROOT, check=True)
    for name in LEGACY:
        path = os.path.join(ROOT, "public", name, "index.html")
        old = open(path, encoding="utf-8").read()
        title = html.unescape(re.search(r"<title>(.*?)</title>", old, re.S).group(1))
        desc = html.unescape(re.search(r'<meta name="description" content="(.*?)"', old, re.S).group(1))
        inner = re.search(r'<main class="wrap">(.*)</main>', old, re.S).group(1)
        page(t, name, title, desc, f'<div class="legacy"><div class="wrap">{inner}</div></div>')


def notfound(t):
    page(t, "404", "Page not found · Live the Dream Athletics", "That page isn't here.", f"""
<section class="pagehead"><div class="wrap">
  <div class="kicker mono">404</div>
  <h1 class="as-h2">That page isn't <em>here.</em></h1>
  <p class="big narrow">It may have moved when we rebuilt the site. Start with the road, or go home.</p>
  <div class="btns"><a class="btn solid" href="/story/">The road</a><a class="btn" href="/">Home</a></div>
</div></section>""")
    src = os.path.join(ROOT, "public", "404", "index.html")
    os.replace(src, os.path.join(ROOT, "public", "404.html"))
    os.rmdir(os.path.dirname(src))


def build(t):
    if not t.preview:
        legacy_pages(t)     # runs build.py first; v2/v3 then overwrite the pages they own
    v2.page = page          # v2 page bodies, v3 shell
    v2.NAV = NAV
    # Players are held in data/people.json but kept off the public people page for now (Kevan, 2026-11-08).
    v2.PEOPLE[:] = [p for p in v2.PEOPLE if p.get("group") != "Players"]
    v2.build(t)
    home(t); story(t); athletes(t); sponsors(t)
    if not t.preview:
        notfound(t)
    if not t.preview:
        open(os.path.join(ROOT, "public", "llms.txt"), "w", encoding="utf-8", newline="\n").write(LLMS)


if __name__ == "__main__":
    build(v2.Target(sys.argv[1] if len(sys.argv) > 1 else "preview"))
