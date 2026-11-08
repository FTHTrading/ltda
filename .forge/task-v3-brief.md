# Task v3: Live the Dream Athletics, "the new era with the old"

```
FORGE-CLASS: entity=UnyKorn LLC (operator of LTDA and NIL33)
             sec=MED (minors' images and names; no money, no keys)
             claims=MARKETING
             custody=NONE
             hearth=NONE
             chain=READ (links to the existing Base anchors; no new anchor)
             surface=PUBLIC
```
Routing: FULL FORGE. Branch `feat/v3-new-era` in worktree `dev/platforms/ltda-v3`. Nothing deploys without Kevan's go.

## What
Rebuild livethedreamathletics.com around the program, not the founder. The story: 25 years of helping young players (the old era: gloves, clinics, camps, bridges to Panama and Cuba, players into college and pro ball), carried into a new era (NIL33 for fair, open athlete deals; records anyone can check). One founder panel proves who started it and links to kevan.unykorn.ai for the full record. Every page says plainly that UnyKorn LLC operates LTDA and NIL33 now, in words and in schema, so people and AI tools connect them.

## Why
Diligence readers and AI tools read the sites as unrelated strangers and a new company. The program has 25 years of outside proof (Tucson 2003 / SABR, Beloit Daily News 2007, Indian Hills, Troy Hall of Fame). The site should show it, sourced, and hand athletes to NIL33.

## Audience (Kevan, 2026-11-08)
1. Families of young players. 2. College and pro athletes (NIL). 3. Sponsors and donors. AI readability through JSON-LD and `llms.txt`.

## In scope
- New home: "Then / Now". Old era: proof cards with sources. New era: NIL33, records, the fund. Founder panel. Sponsors band.
- New pages: `/story/` (then and now, sourced timeline from `record.json`), `/athletes/` (why NIL33 exists, how it works, links to nil33.com), `/sponsors/` (what support pays for, gifts not investments).
- New shared look (`public/v3/site.css`) applied to every existing page through the shared `page()` template, so no page looks old.
- JSON-LD on every page: Organization LTDA (`foundingDate` 2001, `founder` = `https://kevan.unykorn.ai/#kevan-burns`, `parentOrganization` = UnyKorn LLC `https://unykorn.ai/#org`). Updated `llms.txt`.
- A photo set from Kevan's folder, in tiers (below).

## Out of scope
- Re-anchoring the archive on Base (needs Kevan's key). New pages say "not yet in the anchored archive."
- The other session's Tucson patch (`0001-History-Tucson-2003...`). Not applied here; v3 links its sources directly, and the patch merges after.
- Deploy.

## Photos: tiers
| Tier | Rule | From the 2026-11-08 set |
|---|---|---|
| A: can publish | No identifiable person, or Kevan alone, or public event with adults | KB1 "Rideau Crusher" bat; row of donated gloves (one adult coach: needs his yes, crop him out otherwise); sepia batter at the plate (if it's Kevan) |
| B: adults, need each person's yes | Named or identifiable adults | Night coaching talk to adults (Tucson 2003 slides); handshake photo; locker-room photo; Cuba street group; Cuba elder with bat; four players behind the cage net; Nationals coach photos |
| C: minors, need a parent's written yes | Anyone under 18 | Kevan's children (walking with a bat bag; hitting at dusk; boy at the Panama ballpark): Kevan's own yes in writing is enough. Teen team at the night practice; Panama youth team: each parent. |
Faces are never identified by the build; names come only from Kevan. Default for any photo not cleared: not published.

## Acceptance criteria
1. Every factual sentence maps to a `record.json` entry or a source link; the reputation crawler reports 0 conflicts and 0 forbidden strings on the built pages.
2. `node tools/copy-gate.js` prints clean.
3. Every page carries the LTDA Organization JSON-LD with the founder and parent IDs above; it parses.
4. No photo of a minor appears without a recorded yes in `data/intake/*/ATTACHMENTS-LOG.md`.
5. Mobile 375px: no horizontal scroll; reduced motion respected; Lighthouse a11y ≥ 95.
6. Screenshots of home, `/story/` and `/athletes/` at 1440 and 375 for Kevan.

## Claims touched (literal)
"since 2001"; "programs of UnyKorn LLC"; "Gifts, not investments"; "No percentage of a player's money"; the record entries' exact text. No "charity", "nonprofit", "tax-deductible", "guaranteed".

## Test plan
`python -I -m unittest` in reputation-tools against the built `public/`; copy gate; JSON-LD parse check; Playwright screenshots.
