# Ship receipt: LTDA v2 to production (WAITING FOR KEVAN'S GO)

FORGE Phase 6. Nothing below has been sent to production.

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
