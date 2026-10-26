# Ship receipt: LTDA v2 to production (DEPLOYED 2026-10-26)

**Deployed** 2026-10-26 ~17:56Z on Kevan's instruction in chat ("add the Live the Dream to the website that we actually
have up so that when I get to the office, it has everything connected"). `main` fast-forwarded locally to `99db6b9`
(not pushed: the GitHub repo is public and the branch carries internal .forge files). Worker `ltda-site` version
`03c8d909-a68f-4ce1-bbd6-ab0f7ad0791d`; previous live version `10c09850-2cf7-4002-b840-74610de82a60` (2026-09-17)
is the rollback (`npx wrangler@4 rollback 10c09850-2cf7-4002-b840-74610de82a60`).

**Served check (livethedreamathletics.com, 2026-10-26 ~17:57Z):** /, /letter/, /collection/, /nil/, /youth/, /people/,
/photos/, /history/, /proof/, /fund/, /v2/preview.css, /v2/preview.js, two media files and /api/health all 200; home
serves v2 (hero, "Three things", NIL33 band); no preview banner; 0 references to uncleared photos; 0 "zero-knowledge".
Known: www.livethedreamathletics.com serves the site directly (200) instead of 301 to the apex; static assets answer
before the worker's redirect runs. Pre-existing config, not changed here.

FORGE Phase 6. Original pre-deploy receipt below.

| | |
|---|---|
| What | v2 design: home hub, /letter/, /collection/, /nil/, /people/, /photos/; older pages keep their URLs with nav pointing into v2 |
| Commit | `fc8f5cb` on `feat/memories-redesign` (merge to `main` at deploy time) |
| Where | Worker `ltda-site` on livethedreamathletics.com + www (wrangler.jsonc) |
| Surface | PUBLIC |
| Preview | Deployed 2026-10-26 to `ltda-site-preview` (https://ltda-site-preview.kevanbtc.workers.dev), version 903441af-4fb0-4b2f-bc9d-5c1b4235172b. Served check: all 8 pages + css/media/health 200; no preview banner; no uncleared photo referenced |
| Rollback | `npx wrangler@4 rollback` on `ltda-site` (previous version stays available), or redeploy `main` at `fddb823` |
| Copy gate | `node tools/copy-gate.js`: clean |
| Account rule | Cloudflare changes go through the Operator; Operator session was offline at deploy time (2026-10-26) |

## What goes public (decisions for Kevan)
1. **People page:** six text cards (John Mayotte, Cam Walker, Rick Schu, Mike Rizzo, Alan Nero, Tarik El-Abour) with Kevan's relationship lines and sourced public facts. No photos of them. Tarik's card states he is widely reported as the first pro player with autism (public, sourced).
2. **Collection:** six records with stories and photo fingerprints; the six photos show "photo coming" panels. Publishing them needs Kevan's yes as family/parent (his son below the bat; his grandmother; himself as a kid with team photos).
3. **Photos page:** only already-public photos, Kevan's portrait and the AI logo concepts (labelled "made with AI").
4. **Letter:** names Rizzo, Schu, Nero, Mayotte (and "his wife", unnamed), Walker; draft year and Montverde year not stated.

## After deploy
`curl` each page on livethedreamathletics.com, confirm v2 markup and the absence of intake photos (verify served, not repo).
