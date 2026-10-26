# Research: what makes top athletic / athlete-story sites stand out

- **For:** livethedreamathletics.com redesign (LTDA): static HTML/CSS, light JS, Cloudflare Worker static assets
- **Date:** 2026-10-26
- **Method:** Read-only. Live pages loaded in a browser pane with screenshots, plus computed-style reads (font-family, size, colour, blend modes) through page JS. Pages that blocked the browser were read as text with WebFetch, and those entries are marked **text-only**: visual claims about them are inferred, not seen. Cookie banners were declined. Nothing was submitted.
- **Quote rule:** no quotation from any site is longer than 15 words.
- **Label:** this is research and contains no implementation. Every pattern below is a recommendation, and nothing in it has been built or tested yet.

---

## 1. Site-by-site findings (18 sites)

### A. Athlete-story and media

**1. The Players' Tribune: https://www.theplayerstribune.com/** (seen live)
- **First person is the product.** The athlete is the byline, and many pieces are letters ("Letter to My Younger Self", "Dear UT", "To Chicago"). The excerpt on each card is in the athlete's voice, not an editor's.
- **Editorial type pairing.** Headlines and body use a serif (computed `PublicoHeadline`), and UI and captions use a sans (`Graphik`, 12px/600, white on the image). Long reads sit in a ~680px column with centred bold-italic pull quotes and a small attribution line.
- **Credits on every photo, including family snapshots.** On the Derek Jeter "Letter to My Younger Self" page, a pro shot credited to a Getty or Imagn photographer sits next to one credited "Courtesy of Derek Jeter". The credit makes an amateur photo read as a primary source. The home hero was an illustration rather than a photo, which avoids the photo-quality problem altogether.
- **Low-res and candid fit:** strong. Their format already mixes pro and personal photos.

**2. Nike / Jordan Brand: https://www.nike.com/jordan** (seen live)
- **Diptych hero.** An extreme close crop (back and shoulder texture) sits beside the full-body action frame. The crop carries the emotion and the wide frame carries the context.
- Dark ground (#111 to #1a1a1a), `Helvetica Now` / `Neue Haas Grotesk`, a small uppercase eyebrow over a short bold uppercase headline and a pill CTA. One heritage section heading reads "Born from tradition".
- Lifestyle tiles show people mid-moment (crouching, laughing), not posed.
- **Low-res fit:** moderate. The diptych works with phone photos if the close crop comes from a sharp region of the frame.

**3. On Running "OFF Stories": https://www.on.com/en-us/explore/off-stories** (seen live; images lazy-loaded)
- One proprietary grotesk (`On`) everywhere, with negative tracking. The intro paragraph is set very large (~37px), so the voice reads as a statement.
- A row of circular avatar thumbnails acts as category chips (Running, Training, Culture, and so on), so people become the navigation.
- Story cards are gradient-darkened photos with white type and two pill buttons.
- **Low-res fit:** moderate. Circular chips are very forgiving of low resolution.

**4. Under Armour:** not reviewed (time budget). Not cited anywhere below.

### B. Baseball culture and development

**5. Driveline Baseball: https://www.drivelinebaseball.com/** (seen live)
- **Proof through athlete outcomes.** An "Athlete Spotlight" hero pairs a player photo with a card whose headline runs from draft pick to All-Star. The arc is the credential.
- `Montserrat` 700 uppercase headings (60px H1), `Lato` body, a black/white/orange-gold system, rounded pill CTAs. The training-facility photography is gritty: netting, cages, low light.
- **Low-res fit:** moderate. Their gritty facility photos are close to what LTDA has.

**6. Perfect Game: https://www.perfectgame.org/** (text-only)
- **Numbers as the headline credential.** Header stats give MLB players and draft selections as a pipe-separated uppercase line, like a scoreboard. An alumni grid of headshots with names, and a "since" copyright range (1994–2026), signal age.
- **Low-res fit:** the stat line needs no photos at all, which suits LTDA.

**7. Baseball America: https://www.baseballamerica.com/** (seen live)
- `Tungsten` (an ultra-condensed display face) for headlines over `Barlow` body. A red category eyebrow, then a huge condensed headline over a dark full-bleed action photo.
- A "Quick Hits" ticker bar under the nav.
- **Low-res fit:** weak for the hero, which needs a sharp photo. The ticker idea transfers well.

**8. Prep Baseball: https://www.prepbaseballreport.com/** (seen live)
- `komu-a` condensed uppercase, black and red, slanted tabs, dense ad slots.
- **Anti-pattern for LTDA.** It reads busy and promotional. Use it only as a reminder of what "travel-ball template" looks like, and avoid it.

**9. Savannah Bananas: https://bananaball.com/savannah-bananas/** (seen live; thesavannahbananas.com redirects here)
- Two-colour identity, navy with banana yellow, carried by `Anton` uppercase plus a script wordmark. The brand is mostly colour discipline.
- **The schedule is a designed object:** scoreboard rows with a yellow left bar, a date block, an opponent and a venue.
- The origin story is told plainly in a "Who we are" section, with press names (CBS, NBC, SI) as proof. A repeating slogan strip acts as a marquee.
- **Low-res fit:** strong. Crowd and celebration photos tolerate softness, and the brand colour does the work.

**10. Negro Leagues Baseball Museum: https://www.nlbm.com/** (seen live). This is the best heritage reference in the set.
- **Cream paper ground** (computed `rgb(253,253,246)`), headings in deep green `#1E4D47` and maroon, condensed uppercase (`scale-variable`), and a faded script word behind the content.
- **The hero is a row of rounded photo cards with a deliberately mixed treatment:** one black-and-white archival frame, one colour, one green-monochrome duotone. The duotone is baked into the image file (no CSS filter was found). The mix makes the archive feel curated rather than inconsistent.
- **Low-res fit:** excellent. It is built around old photographs.

**11. Nike RBI (MLB's youth programme): https://www.mlb.com/rbi** (seen live; branded "NIKE RBI")
- The page is mainly a feed of short video stories about individual players and coaches (perseverance, playing in honour of a coach). The people are the content.
- A supporters rail on the side shows sponsor and partner logos, separate from the stories, and three primary CTAs sit at the top (affiliate, find a programme, donate).
- **Low-res fit:** good. The stories are handheld or broadcast quality.

### C. Agencies and foundations

**12. Octagon: https://www.octagon.com/** (text-only; the browser was blocked)
- Short stacked headlines with **one italicised accent word** ("Play to your *strengths*"), and work shown as named case-study cards (brand plus athlete).
- **Relevance:** the founder was a former Octagon player agent. Do not use Octagon's marks. State the role in text only (see §3.2).

**13. Wasserman: https://www.teamwass.com/ → redirects to https://the.team/ ("THE·TEAM")** (seen live)
- The redirect is as observed on 2026-10-26. Whether this is a rebrand or a sale is UNVERIFIED; do not describe it on any surface.
- **Black-and-white hero photography** with `Gotham` uppercase, widely tracked (68px, +3.4px).
- **A mixed-style statement line:** a roman serif with italic accent words in green, for example *unifying power*, *Sports*. This is the clearest live example of the serif-plus-italic-accent move.
- A news grid of B&W and colour portraits, then a large wordmark footer.

**14. Roc Nation Sports: https://www.rocnation.com/sports/** (seen live)
- **A roster as an index:** an A–Z letter filter over a uniform grid of headshots on matching dark gradient backdrops. Each card has the name, a hometown line and "Learn more →".
- `Roboto Condensed` throughout with tight negative tracking. The hero is a carousel with the name centred.
- **Lesson:** uniform crops and backdrops make a mixed-quality set of people look like a system.

**15. Jackie Robinson Foundation: https://www.jackierobinson.org/** (seen live)
- **Navy and muted gold** (`#c6b784`), `Graphik Bold` uppercase, and a checkerboard of alternating split blocks (a text panel with an outlined CTA next to a photo).
- The hero photo sits under a heavy dark overlay so the headline reads, and a big "42" appears as a graphic motif.
- **A gap to beat:** on the homepage, the archival Robinson image had no visible caption or credit, and several images had filenames as alt text. LTDA can be better on captions and alt text from day one.

**16. Laureus Sport for Good: https://www.laureus.com/sport-for-good** (seen live)
- The hero photo is washed with a **deep navy overlay**, which works as a near-duotone. An ambassador appears **next to a programme coach in programme kit**, so the star is shown serving the programme rather than endorsing it.
- Lowercase section headings, impact figures written into prose, programme cards with a country flag plus sport and focus tags, partner logos split into "Global" and "Host" tiers.
- **Caution:** the page gives two different programme counts (300+ in the intro, 160+ in "where we work"). That inconsistency is the failure LTDA's proof layer should prevent.

### D. Award-level references (Awwwards)

**17. Justin Jefferson: https://jjettas.com/** (Awwwards Honorable Mention, dated Oct 2, 2026 on its Awwwards page; seen live). This is the most relevant technique reference.
- **It makes broadcast-quality footage look premium through layering, not resolution.** Live DOM inspection found stacked texture layers using `mix-blend-mode` multiply, screen, overlay and soft-light, a dedicated grain layer, and a soft-light tone layer. Video stills had visible scanline and halftone texture with a warm gradient tint toward the edges.
- **The athlete's name is a giant blurred background marquee** (`filter: blur(1px)`, soft-light) behind the content, with ghosted yard-line numbers as wayfinding.
- **"Signature Moments" are trading cards:** a photo in a gold foil frame with the moment's name and a monospaced stat line underneath (in the format "14 REC · 227 YDS · 4 TD"). It also has a handwritten signature over a portrait, `beachwood-variable` ultra-display uppercase (222px), Lenis smooth scroll, and 6 canvases plus 1 video (counted on load).

**18. Montreal Canadiens Children's Foundation: https://fondation.canadiens.com/** (Awwwards Honorable Mention, dated Aug 28, 2026; seen live)
- **Cut-corner (notched) image masks** on candid, natural-light kids' photos, and a **bento grid** that alternates saturated colour text tiles with photos.
- The narrative device is a refrain: each tile is a child gaining something, then "one ___ at a time" (stride, pass, smile).
- **Dated impact numbers**: a money figure and a count of organisations, each tied to a "since 2000" frame. Big display face (`bauhausvole`, 121px uppercase) with `Poppins` body. Illustrated characters fill the gaps where there are no photos.
- **Low-res fit:** strong. The masks and colour tiles reduce how much each photo has to carry.

**19. ZT Baseball: https://ztbaseball.com/** (Awwwards nominee, Nov 18, 2025; seen live)
- **The closest analogue to LTDA's photos.** The hero is a team kneeling on a field holding a trophy, and it is softened with a navy gradient wash from the left that doubles as the text panel.
- `Roboto Slab` plus a display face (`Boston`) on `TT Commons` body.
- **Lesson:** a gradient wash rescues an ordinary team photo, but a slab serif alone does not make it read as premium.

(Under Armour was not reviewed, so 18 sites carry findings.)

---

## 2. The patterns to adopt, ranked

Ranked by how much each one moves "old phone photos" toward "premium" for LTDA, weighed against build cost on a static site.

### 1. One consistent photo treatment applied to every archive image (seen on JJettas, NLBM, Laureus, ZT)
None of the sites showed raw photos at mixed quality side by side. They unify them with a wash, duotone or grain.
**Implementation:**
- Bake a duotone into each image at build time (sharp/ImageMagick: greyscale, then map shadows to `--ink` and highlights to `--paper`) and ship AVIF/WebP plus JPEG. Baked files are cheaper than live CSS filters and look the same everywhere (NLBM bakes theirs).
- Keep the colour original for the lightbox, so the treatment is the stylised view and the colour file is the record.
- If you need it live, use an inline SVG `<filter id="duo">` with `feColorMatrix type="saturate" values="0"` followed by `feComponentTransfer` tables, applied as `filter:url(#duo)`.

### 2. A global grain/texture layer (JJettas)
**Implementation:**
- One `position:fixed; inset:0; pointer-events:none; z-index:50` div whose background is an SVG `feTurbulence` data URI (`baseFrequency≈0.8`, `numOctaves=2`, `stitchTiles`), at `opacity:.06–.10` with `mix-blend-mode:overlay`.
- No animation by default. Optionally add a 2-step `steps(2)` jitter at 8fps, disabled under `prefers-reduced-motion`.
- Grain hides JPEG blocking and makes softness look chosen.

### 3. Credit and caption every photo like an archive (Players' Tribune, the gap at JRF)
**Implementation:**
- Use `<figure>` + `<figcaption>` with a fixed micro-format: `PLACE · YEAR — what is happening. Photo: LTDA archive (phone).`
- The caption is set in a mono or small-caps sans at 11–12px with tracking.
- Real alt text, never filenames.
- This is the single cheapest thing that turns a snapshot into a document.

### 4. Make the archive look deliberate: contact sheet, film frames, trading cards (JJettas cards, NLBM mixed cards)
**Implementation:**
- Use a CSS grid of uniform 4:5 or 3:2 frames with a thin `--paper` border, frame numbers (`counter()` in `::before`), and a sprocket strip made with `repeating-linear-gradient` on the container edges.
- For hero moments, use the trading-card variant: a frame, then a title, then a one-line mono "stat line" with no numbers we can't source (for example `PANAMA · CLINIC · 2016`).
- `object-fit:cover` plus a per-image `object-position` stored in a `data-focus` attribute, so every crop lands on faces.

### 5. A founder voice in the first person (Players' Tribune)
**Implementation:**
- Write the "Story" page as a letter in a ~640–680px serif column, with pull quotes set bold-italic and centred, and an attribution line.
- Write the copy with the founder. Do not ghost-write facts.

### 6. Dated proof numbers, never undated ones (Perfect Game, Montreal Foundation; Laureus as the warning)
**Implementation:**
- A scoreboard strip: big condensed numerals with a small "since / as of" label (for example *since 2001*, only if that year is confirmed).
- Every number needs a source note in a `<details>` or footnote.
- Use one number per concept and keep them consistent across pages (Laureus contradicts itself).
- No count goes live without a source (rules/11).

### 7. An index for the "people who shaped me" section (Roc Nation grid; Laureus "star with the programme")
See §3.2.

### 8. Two-tone colour discipline plus one accent (Savannah Bananas, JRF, NLBM)
See §3.3. Every top site ran on two or three colours. None used gradients or bright rainbows.

### 9. A designed schedule and clinic list (Savannah Bananas)
**Implementation:**
- Clinics, drives and camps as table rows with a coloured left bar, a date block, place and country (flag emoji or a small SVG), and status.
- Plain HTML `<table>` or `<ol>`, so it is readable without JS.

### 10. The proof layer as a design element, not a disclaimer (no site does this; it would set LTDA apart)
**Implementation:**
- Each archive item gets a small "Verify" chip (mono, outlined) that opens a panel with the file's SHA-256, the anchor reference and a link to the public verifier.
- **Gate:** per rules/10 and rules/11, the chip only ships for items whose anchor receipt exists and has passed a served check. Until then the chip reads "Record pending", never "on-chain".

---

## 3. Specific answers

### 3.1 Making 2015–2018 phone photos look intentional
Ranked by effect, for LTDA's actual inventory (night team kneels, dirt-field clinics, ballpark shots, spring training):

| Technique | Use it on | Why | Build note |
|---|---|---|---|
| **Baked duotone** (ink navy → paper cream, or clay → cream) | Grid and story thumbnails | Removes white-balance mismatch between phones and years. NLBM and Laureus both use this. | Build-time script; keep the colour original for the lightbox |
| **Grain overlay** | Site-wide | Hides compression; reads as film | SVG turbulence, opacity ≤ .10, overlay blend |
| **Hard, confident crops** | Hero and diptychs | Phone photos are often wide and centred. A tight crop on faces, hands or a cap reads editorial (Jordan's diptych). | `data-focus` attribute → `object-position` |
| **Contact sheet / film strip** | Archive page, year dividers | Turns "many average photos" into "a body of work". Quantity becomes the asset. | CSS grid plus frame-number counters |
| **Night photos: lean in** | Night team-kneel shots | Push blacks to `--ink`, let the field lights bloom. Don't brighten, which only shows noise. | Levels and duotone at build; no sharpening |
| **Dirt-field clinics: warm clay duotone** | Panama clinics | The terracotta palette matches the subject, so dust reads as atmosphere | A second duotone map (`--clay`) |
| **Scrapbook (tape, rotated polaroids)** | At most one section ("Gear drives") | Charming in one place, cheap-looking everywhere | CSS `rotate(-2deg)`, a tape PNG; limit to 3–5 items |
| **Upscaling (AI)** | Only the 1–3 hero images | Fixes edge pixelation at large sizes | Review each output for invented faces or detail. Never upscale archive items that carry a hash, because the hash must match the original file. |

Rules that stop the look turning cheap: no drop shadows on photos, no rounded corners above 8px except on chips, no Instagram-style filters, and never put a low-res photo full-bleed at 100vw without the duotone and grain.

### 3.2 A "people who shaped me" section without implying endorsement
What the reviewed sites do:
- **Roc Nation:** only shows people it actually represents.
- **Laureus:** shows the star *in programme context*.
- **Players' Tribune:** uses the *athlete's own voice* and credits every photo.
- **Montreal Foundation:** has no celebrity section at all.

Recommended pattern for LTDA, **"In the Frame"**:
1. **Name the relationship, the date and the place.** For example: "Coached alongside at spring training, 2016", or "Former client during my time as a player agent". The caption states a fact that happened. It does not state an opinion the person holds.
2. **Photos only where the founder is in the frame,** taken by LTDA. No headshots pulled from the web, no team or agency logos, no MLB or club marks. Mentioning a ballpark name in a caption is fine; using the team logo is not.
3. **No pull quotes from those people** unless they gave written consent for that exact text, and the consent is filed in the deal tree.
4. **A visible line under the section,** in substance: *Photos document moments; they do not imply endorsement by anyone pictured.* Get the final wording from counsel. It is a REGULATED-adjacent claim, so FORGE `claims=MARKETING` at minimum.
5. **Layout:** a uniform grid (Roc Nation style), the same duotone, the same 4:5 crop. The caption is the content and the name is secondary, so it reads as a timeline, not a roster of endorsers.
6. **"Octagon":** text only, past tense, for example *former player agent (Octagon)*. Do not use the logo. Check with counsel whether naming the employer is acceptable.
7. Before publishing any identifiable minor, keep a parental photo release on file. Default to group and wide shots, and use no surnames for minors.

### 3.3 Typography and colour: heritage baseball meets modern
Observed pattern: the premium sites use **one condensed uppercase display face, one serif or clean sans for reading, and at most one script or italic accent.** Prep Baseball and Savannah Bananas show the ceiling when only condensed type is used.

**Type (Google Fonts, free, works on a static site):**
- **Display:** `Oswald` 500–700 uppercase, or `Anton` for maximum punch. Reference: Baseball America's Tungsten and NLBM's condensed face.
- **Reading / editorial:** `Newsreader` or `Source Serif 4` for the founder letter and story pages (the Players' Tribune move), with `Inter` for UI.
- **Accent:** serif *italic* accent words in the accent colour (The Team, Octagon). Optionally, a baseball script (`Yellowtail`) used **once**, as the wordmark or a single section stamp (Savannah Bananas, NLBM).
- **Proof / captions:** `IBM Plex Mono` 11–12px, uppercase, `letter-spacing:.08em`, for captions, frame numbers, hashes and stat lines (JJettas stat line).

**Colour tokens** (define on `:root`, with a dark variant):
| Token | Value (proposal) | Role | Reference |
|---|---|---|---|
| `--paper` | `#F3EEE2` | Light ground, cream | NLBM `#FDFDF6` |
| `--ink` | `#13213A` | Text, deep navy, night-field duotone shadows | JRF, Savannah Bananas, Laureus |
| `--clay` | `#B4562E` | Infield dirt accent, Panama duotone | |
| `--grass` | `#1F4A3A` | Secondary heritage green | NLBM `#1E4D47` |
| `--chalk` | `#FFFFFF` | Foul lines, rules, frame borders | |
| `--gold` | `#C6B784` | Sparingly; proof chips, record markers only | JRF `#c6b784` |

Use two colours per section (paper + ink, or ink + chalk), with clay as the one accent. Dark mode is ink ground, paper text, clay accent; the night-game photos look best here, so consider making the home page dark by default.

### 3.4 One hero concept: "The Contact Sheet"
**Idea:** the first screen is an archivist's contact sheet of the program's 25 years, at night.
- **Ground:** `--ink`, with the grain layer on.
- **Headline:** left-aligned, stacked condensed uppercase in `--paper`, with one serif-italic accent word in `--clay`. For example: LIVE THE DREAM / ATHLETICS, then *since [year]* once the founding year is sourced. Below it, a single sentence in the founder's voice.
- **The strip:** a horizontal film strip of 7 duotone frames runs across the lower 40% of the viewport: night kneel, Panama dirt clinic, ballpark, spring training, gear drive, and so on. Sprocket holes come from `repeating-linear-gradient`, and frame numbers are in Plex Mono.
- **The active frame:** the centre frame is 1.6× larger. It shows its original colour and drops the duotone on hover or focus, which echoes the NLBM mixed-treatment card row.
- **The caption:** under the active frame, a mono caption line:
  `PANAMA · 2016 · FRAME 07 · RECORD ▸`
  "RECORD" opens the verify panel only when that file has a served anchor receipt; otherwise it reads "RECORD PENDING".
- **Motion:** the strip auto-advances one frame every 5s with a CSS `transform: translateX()` transition. Arrow keys and buttons work, it pauses on hover or focus, and it is static (no auto-advance) under `prefers-reduced-motion`. About 40 lines of vanilla JS.
- **Mobile:** the strip becomes a vertical stack of 3 frames with `scroll-snap`, and the headline sits above it.
- **Why it works:** it makes *quantity and age* the premium signal (a contact sheet is evidence of a life's work). It hides each photo's weaknesses inside a consistent treatment. And it introduces the proof layer in the first screen without crypto jargon.

---

## 4. Gates before any of this goes live

- FORGE-CLASS for the redesign task: `surface=PUBLIC`, `claims=MARKETING` (endorsement and "on-chain" wording), `chain=READ` (verify links only). That means **FULL FORGE**, including the marketing-copy ADR and the Phase 6 verify-served check.
- **The "anchored on-chain" wording** needs a receipt per item (rules/10 §3) and a served check (rules/11) before it appears. Until then, use "record pending".
- **Founding year, "25 years", the agent history and every count:** source each one from Kevan or the client before use. This document does not verify any of them.
- **Minors in photos:** releases are on file before publishing.

## Sources (all accessed 2026-10-26)
- https://www.theplayerstribune.com/ and https://www.theplayerstribune.com/posts/derek-jeter-letter-to-my-younger-self-new-york-yankees-mlb-baseball
- https://www.nike.com/jordan
- https://www.on.com/en-us/explore/off-stories
- https://www.drivelinebaseball.com/
- https://www.perfectgame.org/ (text-only)
- https://www.baseballamerica.com/
- https://www.prepbaseballreport.com/
- https://bananaball.com/savannah-bananas/
- https://www.nlbm.com/
- https://www.mlb.com/rbi
- https://www.octagon.com/ (text-only)
- https://the.team/ (redirected from https://www.teamwass.com/)
- https://www.rocnation.com/sports/
- https://www.jackierobinson.org/
- https://www.laureus.com/sport-for-good
- https://jjettas.com/ and https://www.awwwards.com/sites/justin-jefferson
- https://fondation.canadiens.com/ and https://www.awwwards.com/sites/montreal-canadiens-foundation
- https://ztbaseball.com/ and https://www.awwwards.com/sites/zt-baseball
- https://www.awwwards.com/websites/sports/ (category index)
