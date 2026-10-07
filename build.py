import os, json
B="https://basescan.org"
C=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','base.json')))
UNIT,AFF,ROOT=C['unit'],C['affiliate'],C['historyRoot']
TX=C['txs']; TX2=C['finish']['anchorHistory2']
NAV=[("/history/","History"),("/international/","International"),("/today/","The game today"),("/families/","Families"),("/nil33/","NIL33"),("/systems/","Systems"),("/proof/","On chain")]
FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">'
def short(h): return h[:8]+"…"+h[-6:]
def tx(h,label=None): return f'<a class="chip" href="{B}/tx/{h}" target="_blank" rel="noopener">{label or "tx "+short(h)}</a>'
def addr(a,label=None): return f'<a class="chip" href="{B}/address/{a}" target="_blank" rel="noopener">{label or short(a)}</a>'
def page(path,title,desc,body):
    AC=' aria-current="page"'
    nav="".join(f'<a href="{h}"{AC if h==path else ""}>{t}</a>' for h,t in NAV)+'<a class="give" href="/fund/"'+(' aria-current="page"' if path=="/fund/" else "")+'>Fund a dream</a>'
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://livethedreamathletics.com/media/rod-carew-hillside.jpg">
<link rel="icon" href="/media/ltd-logo.png">{FONTS}<link rel="stylesheet" href="/site.css"></head><body>
<div class="fx" aria-hidden="true"><i></i><i></i><i></i></div>
<header class="top"><div class="wrap"><a class="brand" href="/"><img src="/media/ltd-logo.png" alt=""><span>Live the Dream Athletics<small>ON THE RECORD SINCE 2001</small></span></a>
<button class="menu" id="menu" aria-expanded="false" aria-controls="nav">Menu</button><nav class="main" id="nav">{nav}</nav></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap"><span>Live the Dream Athletics · since 2001 · We love the game. We're here to help.</span><span><a href="https://powerpunchathletics.com">Power Punch</a> · <a href="https://nil33.com">NIL33</a> · <a href="/proof/">On chain</a> · <a href="mailto:kevan@unykorn.org">kevan@unykorn.org</a></span><span>Technology by UnyKorn LLC. Donations are not investments; supporter badges have no cash value.</span></div></footer>
<script>document.getElementById("menu").onclick=function(){{var n=document.getElementById("nav");n.classList.toggle("open");this.setAttribute("aria-expanded",n.classList.contains("open"))}}</script>
</body></html>'''
    d="public"+path; os.makedirs(d,exist_ok=True); open(d+"index.html","w",encoding="utf-8",newline="\n").write(html)

# HOME
page("/","Live the Dream Athletics","Since 2001: gear, coaching and bridges for young athletes. Now every gift, grant and record is on chain.",f'''
<section class="hero" style="background-image:url(/media/rod-carew-hillside.jpg)"><div class="in"><div class="eyebrow">Live the Dream Athletics · since 2001</div>
<h1>Help a kid<br><em>live the dream.</em></h1><p>Twenty-five years of gear drives, coaching and bridges between countries. Now every gift, grant and record is written on chain, so families and donors can see exactly where help goes.</p>
<div class="actions"><a class="btn orange" href="/fund/">Fund a dream</a><a class="btn" href="/history/">See our history</a><a class="btn" href="/proof/">Check it on chain</a></div></div></section>
<section><div class="grid g4">
<div class="panel stat"><div class="v">2001</div><div class="l">Founded. Orlando, Beloit, Panama, Cuba.</div></div>
<div class="panel stat"><div class="v">609</div><div class="l">public posts of our work, 2013–2020</div></div>
<div class="panel stat"><div class="v">33</div><div class="l">history records hashed and anchored on Base</div></div>
<div class="panel stat"><div class="v">$1,016</div><div class="l">what a family now spends a year on one child's sport<sup>1</sup></div></div>
</div></section>
<section><div class="grid g3">
<a class="panel card" href="/history/"><div class="eyebrow">Where we've been</div><h3>Our history, on the record</h3><p>Gear to Cuba, lessons in Beloit, clinics in Panama, prospects to college and pro ball. Every photo and record fingerprinted and anchored.</p><span class="more">Walk the timeline →</span></a>
<a class="panel card" href="/today/"><div class="eyebrow">Where the game is</div><h3>The game today</h3><p>Costs up 46% in five years. Kids from low-income homes quit over cost six times as often. College athletes can now be paid.</p><span class="more">See what changed →</span></a>
<a class="panel card" href="/fund/"><div class="eyebrow">What you can do</div><h3>Fund a dream</h3><p>Grants for gear, travel and fees, paid straight to the program. Every grant recorded in public. Never a loan.</p><span class="more">How the fund works →</span></a>
</div></section>
<section><div class="grid g2">
<a class="panel card" href="/international/"><div class="split" style="gap:18px"><div><div class="eyebrow">International</div><h3>The dream doesn't need a passport</h3><p>Cuba, Panama, the Dominican Republic and beyond. More than a quarter of big-league players were born outside the U.S. We make sure the kids behind them are protected.</p><span class="more">Go international →</span></div><div class="photo"><img src="/media/rod-carew-hillside.jpg" alt="Rod Carew stadium in Panama"></div></div></a>
<a class="panel card" href="/nil33/"><div class="eyebrow">NIL33</div><h3>NIL, in the open</h3><p>For college and pro athletes: endorsements with flat fees, signed terms and a public ledger. Every deal disclosed, no tokens, no games.</p><div class="ev" style="margin-top:12px;display:flex;gap:6px;flex-wrap:wrap"><span class="pill live">Programs live</span><span class="pill live">Public ledger</span><span class="pill soon">On-chain attestation gated</span></div><span class="more">See NIL33 →</span></a>
</div></section>
<section><div class="split"><div class="panel band"><div class="eyebrow">Why on chain</div><h2>Trust you can <em>check.</em></h2>
<p style="margin-top:12px">Youth sports runs on promises: a scholarship, a showcase, a donation. We write ours down where nobody can change them later. You don't have to take our word for it; open the record yourself.</p>
<ul class="list"><li>Every gift gets a receipt on chain.</li><li>Every grant shows its purpose and amount. Never a child's name.</li><li>Every athlete's record belongs to the athlete.</li></ul>
<div class="actions"><a class="btn primary" href="/proof/">See the contracts</a></div></div>
<div><div class="photo"><img src="/media/panama-rod-carew-rail.jpg" alt="Players at the rail above the field in Panama"></div><p class="cap">Panama, 2018. Our players at the Rod Carew stadium rail.</p></div></div></section>
<section><div class="panel band"><div class="split"><div><div class="eyebrow">The system behind it</div><h2>Built for us. <em>Ready for you.</em></h2><p style="margin-top:12px">The same on-chain tools that run Live the Dream can run any academy, league or foundation: athlete passports, a transparent grant fund, gear registries and a permanent history.</p><div class="actions"><a class="btn" href="/systems/">See the systems</a><a class="btn" href="/families/">For players &amp; families</a></div></div>
<div class="photo"><img src="/media/coach-cage.jpg" alt="Coach wearing the Power Punch strap in the cage"></div></div></div></section>
<p class="note">1. Aspen Institute Project Play, 2024 parent survey: average spend on a child's primary sport.</p>''')

# HISTORY
items=[("2001","Live the Dream Athletics starts","Kevan Burns, former player and MLB agent, starts training and placing young players. The Power Punch batting aid follows and later reaches Dick's Sporting Goods.",[("media/kevan-original-power-punch.png","original Power Punch photo · anchored")]),
("2013","Beloit, Wisconsin","An old grocery store becomes a baseball facility: turf, nets, tractor tires. Lessons for local kids.",[]),
("2014","Bridges to Cuba","Equipment drives for Cuban youth: gloves, bats, balls and shoes. Free trips, a documentary shot in Havana, and the line we still use: “We build too many walls and not enough bridges.”",[]),
("2015","Montverde Academy","Kevan runs the baseball program; varsity goes 11–1 in the fall.",[]),
("2017","Beloit summer lessons","Summer lessons from June 10 and the Beloit Baseball community.",[]),
("2018","Panama and showcases","LTD Panama at MVP Sport City and the Rod Carew stadium. Coaching at the Power Showcase. Players on to a Yankees draft, TCU and Niagara, and a 12U team to Cooperstown.",[]),
("2019","Remembering Randy Jaco","Oakleys made in his honor; alumni ties to Indian Hills CC.",[]),
("2020","Dick's, then the pause","After 19 years the Power Punch reaches Dick's shelves. Then COVID stops the fields.",[]),
("2026","The record goes on chain","The history archive is fingerprinted and anchored on Base. Unit #0001 of the Power Punch founder's run is minted. Live the Dream becomes the fund and the system.",[("anchor","history anchor"),("mint","unit #0001 minted")]),]
tl=""
for y,h,p,ev in items:
    chips=""
    for e,l in ev:
        if e=="anchor": chips+=tx(TX['anchorHistory'],"history anchored "+short(ROOT))
        elif e=="mint": chips+=tx(TX['mint0001'],"unit #0001 minted")
        else: chips+=f'<a class="chip" href="/archive/manifest.json">{l}</a>'
    evh=('<div class="ev">'+chips+'</div>') if chips else ""
    tl+=f'<div class="panel item"><div class="yr">{y}</div><div><h3>{h}</h3><p>{p}</p>{evh}</div></div>'
page("/history/","Our history · Live the Dream Athletics","25 years of Live the Dream Athletics, with every record fingerprinted and anchored on chain.",f'''
<div class="phead"><div class="eyebrow">Our history</div><h1>25 years. <em>On the record.</em></h1><p>From a grocery store turned batting cage to stadiums in Panama. The photos and records behind this timeline are fingerprinted (SHA-256) and their combined root is written on Base, so nobody can quietly rewrite it.</p></div>
<section><div class="tl">{tl}</div></section>
<section><div class="grid g2"><div class="panel card"><h3>What's anchored</h3><p>33 files: photos, training videos, the patent record, playing career and retail history. Root <span class="hash">{short(ROOT)}</span>.</p><div class="actions"><a class="btn" href="/archive/manifest.json">Open the manifest</a><a class="btn" href="/proof/">How to verify</a></div></div>
<div class="panel card"><h3>Add to the record</h3><p>Played for us, coached with us, have a photo or clipping? Send it. With your yes (and a parent's, for anyone under 18) it joins the archive.</p><div class="actions"><a class="btn primary" href="mailto:kevan@unykorn.org?subject=Live%20the%20Dream%20archive">Send a memory</a></div></div></div></section>''')

# TODAY
page("/today/","The game today · Live the Dream Athletics","Youth sports costs, who gets left out, and how college athletes are now paid.",'''
<div class="phead"><div class="eyebrow">The game today</div><h1>The game got <em>expensive.</em></h1><p>More kids play than ever, but the cost of staying in keeps climbing, and the rules at the top have changed. Here's where things stand, with sources.</p></div>
<section><div class="grid g3">
<div class="panel stat"><div class="v">$1,016</div><div class="l">average family spend on a child's main sport in 2024, up 46% since 2019. About $1,500 across all sports.</div></div>
<div class="panel stat"><div class="v">6×</div><div class="l">kids from low-income homes quit over cost six times as often as kids from high-income homes.</div></div>
<div class="panel stat"><div class="v">$20.5M</div><div class="l">per year a college can now share directly with athletes, under the 2025 House v. NCAA settlement.</div></div>
</div></section>
<section><div class="grid g2">
<div class="panel card"><h3>What it means for families</h3><ul class="list"><li>Travel ball, gear and fees now decide who stays in the game.</li><li>Talent in small towns and other countries gets missed.</li><li>Money now flows at the top (NIL since 2021, revenue sharing since July 2025), so promises to young players are bigger, and easier to break.</li></ul></div>
<div class="panel card"><h3>What we do about it</h3><ul class="list"><li><b>Grants, not loans</b>, paid straight to the program or vendor.</li><li><b>Records the athlete owns</b>, so a scout can trust them.</li><li><b>Every dollar in public</b>, so a family knows who kept their word.</li></ul><div class="actions"><a class="btn orange" href="/fund/">Fund a dream</a><a class="btn" href="/families/">For families</a></div></div>
</div></section>
<p class="note">Sources: Aspen Institute Project Play, <a href="https://projectplay.org/news/2025/2/24/project-play-survey-family-spending-on-youth-sports-rises-46-over-five-years">2024 parent survey</a> (Nov–Dec 2024, 1,848 parents) and <a href="https://projectplay.org/news/low-income-kids-are-6-times-more-likely-to-quit-sports-due-to-costs">2020 survey</a>; <a href="https://www.cbssports.com/college-football/news/how-college-athletes-will-be-paid-after-house-v-ncaa-settlement-nil-changes-enforcement-contracts-and-more/">CBS Sports</a> and <a href="https://www.espn.com/college-sports/story/_/id/45467505/judge-grants-final-approval-house-v-ncaa-settlement">ESPN</a> on the House v. NCAA settlement (approved June 2025).</p>''')

# FAMILIES
page("/families/","Players & families · Live the Dream Athletics","What Live the Dream offers players and families: grants, gear, an athlete passport and clinics.",'''
<div class="phead"><div class="eyebrow">Players &amp; families</div><h1>A place for <em>you.</em></h1><p>Whether you're a player chasing a roster spot or a parent trying to cover the next tournament, this is what we can do today, and what's coming.</p></div>
<section><div class="grid g2">
<div class="panel card"><span class="pill soon">Opening</span><h3 style="margin-top:12px">Ask for a grant</h3><p>Equipment, travel, tournament and camp fees. We pay the program or vendor directly and record the grant in public by purpose and amount, never by name.</p></div>
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">Gear and training</h3><p>The Power Punch strap and drills, with a founder's run for families and team packs for programs.</p><a class="more" href="https://powerpunchathletics.com">Power Punch →</a></div>
<div class="panel card"><span class="pill soon">In build</span><h3 style="margin-top:12px">Athlete passport</h3><p>A record that belongs to the player: showcase numbers signed by the event, milestones confirmed by a coach. You choose which scouts see it. Nothing personal goes on chain.</p></div>
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">NIL, done in the open</h3><p>For older athletes: endorsements with flat fees and a public ledger through NIL33.</p><a class="more" href="https://nil33.com">NIL33 →</a></div>
</div></section>
<section><div class="panel band"><h2>Our promise to <em>families</em></h2><ul class="list"><li>No child's name, face or stats go public without a parent's written yes.</li><li>Grants are never loans, and never tied to future earnings.</li><li>We never sell an athlete's data.</li><li>Anything we say we gave, you can check.</li></ul><div class="actions"><a class="btn primary" href="mailto:kevan@unykorn.org?subject=Live%20the%20Dream%20family">Talk to us</a></div></div></section>''')

# FUND
page("/fund/","Fund a dream · Live the Dream Athletics","The Live the Dream Family Fund: grants for gear, travel and fees, paid to programs and recorded on chain.",f'''
<div class="phead"><div class="eyebrow">The Family Fund</div><h1>Fund a <em>dream.</em></h1><p>Your gift pays for a glove, a bus seat or a tournament fee for a kid whose family can't. It goes straight to the program, and the record goes on chain for anyone to see.</p>
<div class="actions"><a class="btn orange" href="mailto:kevan@unykorn.org?subject=Family%20Fund%20-%20I%20want%20to%20give">I want to give</a><a class="btn" href="mailto:kevan@unykorn.org?subject=Family%20Fund%20-%20sponsor">Sponsor a team or event</a></div>
<p class="note" style="margin-top:12px"><span class="pill soon">Opening</span>&nbsp; We're finalizing the fund's legal wrapper. Join the list and you'll get the first receipt.</p></div>
<section><h2 style="margin-bottom:14px">Where the money <em>goes</em></h2><div class="flow">
<div class="panel"><b>You give</b><p>Card, bank or USDC.</p></div>
<div class="panel"><b>Receipt on chain</b><p>A supporter badge in your wallet. No cash value, can't be sold.</p></div>
<div class="panel"><b>Grant approved</b><p>For gear, travel or fees. A family asks; a coach confirms.</p></div>
<div class="panel"><b>Paid to the program</b><p>Straight to the vendor or team, never cash to a family.</p></div>
<div class="panel"><b>Public ledger</b><p>Purpose and amount on chain. Never a name.</p></div>
</div></section>
<section><div class="grid g3">
<div class="panel card"><h3>Bridges gear drive</h3><p>Bats, gloves, cleats. Every box logged from donor to the coach who signs for it, like we did for Cuba in 2014.</p></div>
<div class="panel card"><h3>Sponsor a kid's season</h3><p>Cover one player's fees and travel for a year. You'll see each payment on the ledger.</p></div>
<div class="panel card"><h3>Events</h3><p>Clinics abroad and a 24-hour game where every inning is sponsored and every run goes to the fund.</p></div>
</div></section>
<section><div class="panel band"><div class="grid g2"><div><h3>The ledger</h3><p style="margin-top:8px">Live once the fund opens: total given, total granted, grants by purpose. It will read straight from the chain.</p></div>
<div class="tbl"><table><thead><tr><th>Purpose</th><th>Granted</th><th>Grants</th></tr></thead><tbody><tr><td>Equipment</td><td>—</td><td>—</td></tr><tr><td>Travel</td><td>—</td><td>—</td></tr><tr><td>Tournament &amp; camp fees</td><td>—</td><td>—</td></tr></tbody></table></div></div></div></section>
<p class="note">Donations are gifts, not investments. They carry no return, no token value and no ownership. Supporter badges are non-transferable receipts.</p>''')

# SYSTEMS
page("/systems/","Our systems · Live the Dream Athletics","On-chain systems for academies, leagues and foundations: athlete passports, transparent grant funds, gear registries and history archives.",f'''
<div class="phead"><div class="eyebrow">Our systems</div><h1>Run your program <em>on the record.</em></h1><p>We built these for Live the Dream. Academies, travel organizations, leagues and foundations can use the same tools, on their own name.</p></div>
<section><div class="grid g2">
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">History archive</h3><p>Fingerprint every photo, record and clipping, anchor the root on chain, publish a manifest. Your legacy, provable.</p><div class="tl ev" style="margin-top:10px">{tx(TX['anchorHistory'],"our anchor on Base")}</div></div>
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">Gear &amp; unit registry</h3><p>A numbered on-chain record for every unit you sell or donate, with a proof page and resale history.</p><div class="ev" style="margin-top:10px">{addr(UNIT,"PowerPunchUnit contract")}</div></div>
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">Supporter &amp; affiliate badges</h3><p>Non-transferable badges for donors, coaches and introducers. Credit on the record, no speculation.</p><div class="ev" style="margin-top:10px">{addr(AFF,"PowerPunchAffiliate contract")}</div></div>
<div class="panel card"><span class="pill soon">In build</span><h3 style="margin-top:12px">Transparent grant fund</h3><p>Gifts in, grants out to vendors, every payment on a public ledger by purpose. Built to run under the fund's legal wrapper once it is chosen.</p></div>
<div class="panel card"><span class="pill soon">In build</span><h3 style="margin-top:12px">Athlete passport</h3><p>Verified measurables and milestones the athlete owns, with parent consent under 18 and scout access by permission.</p></div>
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">Projections &amp; NIL</h3><p>Player projections at 3fs.app; transparent NIL endorsements at NIL33.</p><div class="ev" style="margin-top:10px"><a class="chip" href="https://3fs.app">3fs.app</a><a class="chip" href="https://nil33.com">nil33.com</a></div></div>
</div></section>
<section><div class="panel band"><div class="split"><div><h2>Want this for your <em>program?</em></h2><p style="margin-top:10px">Tell us who you serve and what you need to prove. We set it up on your accounts and your name.</p></div><div class="actions"><a class="btn primary" href="mailto:kevan@unykorn.org?subject=Live%20the%20Dream%20systems">Get in touch</a></div></div></div></section>''')

# PROOF
rows="".join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a,b in [
 ("PowerPunchUnit (ERC-721)",addr(UNIT,UNIT)),("PowerPunchAffiliate (badges)",addr(AFF,AFF)),("History root (33 files)",f'<span class="hash">{ROOT}</span>'),
 ("History anchored",tx(TX['anchorHistory'],"Sept 17, 2026 · "+short(TX['anchorHistory']))+" "+tx(TX2,"re-anchored Sept 18 · "+short(TX2))),
 ("Founder's run opened (500 units)",tx(TX['openRun'])),("Unit #0001 minted",tx(TX['mint0001']))])
page("/proof/","On chain · Live the Dream Athletics","Contracts, anchors and how to verify the Live the Dream record on Base.",f'''
<div class="phead"><div class="eyebrow">On chain · Base mainnet</div><h1>Don't trust. <em>Check.</em></h1><p>Everything we say we recorded is here, with a link you can open on a public block explorer.</p></div>
<section><div class="panel tbl"><table><thead><tr><th>Record</th><th>Where to check</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section><div class="grid g3">
<div class="panel card"><h3>1 · Pick a file</h3><p>Download any photo or record listed in the <a href="/archive/manifest.json">manifest</a>.</p></div>
<div class="panel card"><h3>2 · Fingerprint it</h3><p>Run SHA-256 on it. It must match the hash in the manifest. One changed pixel gives a different hash.</p></div>
<div class="panel card"><h3>3 · Match the root</h3><p>The manifest's root must equal the root written on Base in the anchor transaction.</p></div>
</div></section>
<p class="note">Records are receipts and badges, never securities. No personal data about any athlete is written on chain.</p>''')
# INTERNATIONAL
page("/international/","International · Live the Dream Athletics","Live the Dream abroad: Cuba, Panama, the Dominican Republic. Protecting young international players and their families with records and grants on chain.",'''
<section class="hero" style="background-image:url(/media/panama-rod-carew-rail.jpg);min-height:400px"><div class="in"><div class="eyebrow">International</div><h1>The dream doesn't<br><em>need a passport.</em></h1><p>We've taken gear to Cuba, run clinics in Panama and represented Latin American players at the top of the game. Now we're building the protection those kids never had.</p><div class="actions"><a class="btn orange" href="/fund/">Fund a player abroad</a><a class="btn" href="mailto:kevan@unykorn.org?subject=International%20program%20partner">Partner with us</a></div></div></section>
<section><div class="grid g4">
<div class="panel stat"><div class="v">27%</div><div class="l">of 2026 Opening Day big-leaguers were born outside the U.S. (213 of 780)</div></div>
<div class="panel stat"><div class="v">21</div><div class="l">countries on 2026 Opening Day rosters</div></div>
<div class="panel stat"><div class="v">74</div><div class="l">players from the Dominican Republic, 56 from Venezuela, 18 from Cuba</div></div>
<div class="panel stat"><div class="v">35–50%</div><div class="l">of a Dominican prospect's signing bonus that trainers take, per this month's reporting</div></div>
</div></section>
<section><div class="grid g2">
<div class="panel card"><h3>What kids abroad face</h3><ul class="list"><li>Handshake deals with boys as young as 11, years before they can legally sign at 16.</li><li>High-interest loans to families against a bonus the child hasn't received.</li><li>Of $1.04 billion in bonuses paid to Dominican prospects from 2012 to 2026, reporting estimates up to half went to trainers and lenders.</li></ul></div>
<div class="panel card"><h3>What we bring</h3><ul class="list"><li><b>Records the family keeps</b>: every promise, meeting and number logged and time-stamped, so nobody can deny it later.</li><li><b>Grants, never loans</b>: gear, travel and fees paid to the program, so no family borrows against a child.</li><li><b>Every dollar in public</b>: donors and families see exactly where help went.</li><li><b>Spanish and English</b>, for families and coaches.</li></ul></div>
</div></section>
<section><h2 style="margin-bottom:14px">Where we've <em>been</em></h2><div class="grid g3">
<div class="panel card"><div class="eyebrow">Cuba · 2014–2015</div><h3>Bridges</h3><p>Equipment drives, free trips, a documentary shot in Havana, uniforms donated. “We build too many walls and not enough bridges.”</p></div>
<div class="panel card"><div class="eyebrow">Panama · 2017–2018</div><h3>LTD Panama</h3><p>Clinics at MVP Sport City and the Rod Carew stadium, working alongside big-league alumni.</p></div>
<div class="panel card"><div class="eyebrow">Latin America · Octagon</div><h3>Representing players</h3><p>Kevan represented Latin American and U.S. players as an MLB agent. He saw the system from the inside, the good and the bad.</p></div>
</div></section>
<section><div class="panel band"><div class="split"><div><h2>Next: <em>Dominican Republic.</em></h2><p style="margin-top:10px">Our first international grant market, with local partner programs and a Bridges gear shipment. Support for Cuba and Venezuela only after a sanctions review, so help arrives legally.</p></div><div class="actions"><a class="btn primary" href="mailto:kevan@unykorn.org?subject=Dominican%20Republic%20program">Run a program with us</a><a class="btn" href="/fund/">Give to Bridges</a></div></div></div></section>
<p class="note">Sources: <a href="https://www.baseballamerica.com/stories/where-do-mlb-players-come-from-2026-opening-day-edition/">Baseball America, 2026 Opening Day</a>; <a href="https://www.propublica.org/article/dominican-republic-baseball-major-league-takeaways">ProPublica, Sept 15, 2026</a>.</p>''')

# NIL33
page("/nil33/","NIL33 · Live the Dream Athletics","NIL33: transparent NIL endorsements for athletes, coaches and creators, with flat fees, signed terms and a public ledger.",'''
<div class="phead"><div class="eyebrow">NIL33 · part of the Live the Dream family</div><h1>NIL, <em>in the open.</em></h1><p>College athletes can now be paid for their name, image and likeness, and schools can share revenue directly. NIL33 is how our athletes, coaches and creators do it without the usual games: flat fees, signed terms, every deal on a public ledger.</p><div class="actions"><a class="btn orange" href="https://nil33.com/apply">Apply to NIL33</a><a class="btn" href="https://nil33.com/ledger">See the ledger</a></div></div>
<section><div class="grid g2">
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">Champions</h3><p>Paid endorsements: a flat fee for a set term, approved lines, a kit and a portal with real results. Every placement is tagged as paid. No commissions, no pay-for-outcome.</p><a class="more" href="https://nil33.com/champions">Champions →</a></div>
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">Ambassadors</h3><p>For coaches, programs, alumni and creators who back a system they believe in. No money changes hands, ever, and no exclusivity.</p><a class="more" href="https://nil33.com/ambassadors">Ambassadors →</a></div>
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">Know Your Athlete</h3><p>Verification for athletes and the organizations working with them, so everyone knows who's real.</p><a class="more" href="https://nil33.com/kya">KYA →</a></div>
<div class="panel card"><span class="pill live">Live</span><h3 style="margin-top:12px">The transparency stack</h3><p>Six layers anyone can check without asking: the public ledger and its JSON, hash-chained signed records, signed athlete assertions, x402 pay-per-call access for software, and the ERC-8004 public identity of the rail that gets paid. Each labelled with what is real.</p><a class="more" href="https://nil33.com/transparency">See the stack →</a></div>
<div class="panel card"><span class="pill soon">Gated</span><h3 style="margin-top:12px">On-chain attestation</h3><p>Signed agreements anchored on chain. Designed and waiting on final sign-off; the public ledger is live today.</p></div>
</div></section>
<section><h2 style="margin-bottom:14px">How to <em>join</em></h2><div class="flow">
<div class="panel"><b>Apply</b><p>Name, audience, program.</p></div>
<div class="panel"><b>Agree</b><p>Approved lines and disclosure text.</p></div>
<div class="panel"><b>Ledger</b><p>Your entry goes public.</p></div>
<div class="panel"><b>Claim</b><p>Sign in with a wallet to own your profile.</p></div>
<div class="panel"><b>Go</b><p>Link, QR, badge, scripts and portal.</p></div>
</div></section>
<section><div class="panel band"><div class="split"><div><h2>How it ties to <em>Live the Dream</em></h2><ul class="list"><li>The athlete record we build with families carries into college and pro NIL.</li><li>Endorsement income stays with the athlete; nothing is borrowed against it.</li><li>Under 18: no deals without a parent's signature.</li></ul></div><div class="actions"><a class="btn primary" href="https://nil33.com">Visit nil33.com</a><a class="btn" href="https://nil33.com/chaos">What happened to college sports</a><a class="btn" href="/families/">For families</a></div></div></div></section>
<p class="note">NIL33 is a program of UnyKorn LLC. No tokens are issued. Every paid endorsement is disclosed.</p>''')

open("public/404.html","w",encoding="utf-8",newline="\n").write(open("public/index.html",encoding="utf-8").read().replace("<title>Live the Dream Athletics</title>","<title>Not found · Live the Dream Athletics</title>"))
print("built")
