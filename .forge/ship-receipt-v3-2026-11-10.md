# Ship receipt: v3 "the new era with the old", 2026-11-10

Status: DEPLOYED 2026-11-10 on Kevan's go in chat ("Yes, deploy it"). Version `ffe9e32f-3518-44aa-999c-46837dac53b1`.

## What goes where
- **What:** branch `feat/v3-new-era` at commit `2f2c28a` (5 commits on top of the live `2cf898f`). Static `public/` plus the unchanged Worker `src/worker.js`.
- **Where:** Cloudflare Worker `ltda-site` on the UnyKorn Cloudflare account, custom domains `livethedreamathletics.com` and `www.livethedreamathletics.com` (from `wrangler.jsonc`).
- **Surface:** PUBLIC.
- **Command:** `npx wrangler@4 deploy` from `dev/platforms/ltda-v3`.

## Rollback
- Live now: version `03c8d909-a68f-4ce1-bbd6-ab0f7ad0791d` (deployed 2026-10-26, v2).
- Roll back with `npx wrangler@4 rollback 03c8d909-a68f-4ce1-bbd6-ab0f7ad0791d`, or redeploy `main` (`2cf898f`).

## What changes for visitors
- New home (then and now), The road (13 chapters, Kevan's own accounts, sourced quotes, 13 photos, 4 click-to-play videos), For athletes (why NIL33), Sponsors.
- All 19 pages in one design, one nav, one footer, one JSON-LD graph tying Live the Dream (2001) to Kevan Burns (`https://kevan.unykorn.ai/#kevan-burns`) and UnyKorn LLC (`https://unykorn.ai/#org`). New `llms.txt`, new 404.
- People: Tarik El-Abour removed; players held off the page for now.
- On chain (`/proof/`): unchanged content (Base contracts and anchors), new look. No new anchor; new pages say they are not yet in the anchored archive.

## Checks before deploy (local, 2026-11-10)
| Check | Result |
|---|---|
| Copy gate (`node tools/copy-gate.js`) | clean |
| Reputation fact checks, all 19 pages (forbidden strings, fact conflicts, JSON-LD, LinkedIn) | 0 problems |
| 375px overflow, all 19 pages | 0 |
| Lighthouse mobile, home | perf 78 · a11y 100 · best practices 100 · SEO 100 |
| Lighthouse mobile, /story/ | perf 81 · a11y 100 · best practices 100 · SEO 100 |
| Lighthouse mobile, /history/ | perf 87 · a11y 98 (heading order inside legacy content) · 100 · 100 |
Performance was measured on a local Python server with no compression; re-measure on the served site.

## Known gaps shipped knowingly
- The other session's Tucson 2003 page patch is not merged (the road covers Tucson with sources).
- People on `/people/` have no recorded yes (site template shows anyone with a relationship; existing behavior).
- Minors' photos and the two Cuba photos held.
- Cloudflare writes normally go through the Operator session (offline); Kevan's go here stands in for that.

## After deploy (verify served, not repo)
1. curl every page for 200 and `class="v3"`; `/api/health` ok; www redirects 301.
2. Confirm served HTML matches the build (hash of `index.html`).
3. Lighthouse on the live home and /story/.
4. Append the result and the new version id here.

## Result (served check, 2026-11-10)
| Check | Result |
|---|---|
| `wrangler deploy` | ltda-site version `ffe9e32f-3518-44aa-999c-46837dac53b1`, custom domains livethedreamathletics.com and www |
| 18 pages live | 200, all serve `class="v3"` |
| /llms.txt, /v3/site.css, cleared photo | 200 |
| Unknown page | 404 |
| /api/health | `{"ok":true}` |
| Tarik on /people/ | 0 |
| Removed photo /media/v3/handshake.jpg | 404 |
| Served HTML vs build | identical except a Cloudflare bot-protection script injected before `</body>` at the edge |
| Lighthouse live, home | perf 81 · a11y 100 · best practices 82 · SEO 100 (LCP 3.9 s) |
| Lighthouse live, /story/ | perf 81 · a11y 100 · best practices 82 · SEO 100 (LCP 3.9 s) |

## Open after deploy
- ~~www does not redirect on file paths~~ FIXED 2026-11-10 on Kevan's go: `"run_worker_first": true` in wrangler.jsonc, deployed as version `8ae1cc73-e5d8-4fc3-adf9-ace66b9e30d7`. Served check: www `/`, `/story/`, `/people/`, `/proof/` and a photo all 301 to the apex with the path kept; apex pages, assets, `/api/health`, 404 and the `/powerpunch` and `/nil33` short links unchanged.
- Best practices 82 on live (not 100 locally): likely the injected Cloudflare challenge script. Check Bot Fight Mode / JS detections on the zone.
- Rollback: to v3 without the www fix `npx wrangler@4 rollback ffe9e32f-3518-44aa-999c-46837dac53b1`; to v2 `npx wrangler@4 rollback 03c8d909-a68f-4ce1-bbd6-ab0f7ad0791d`.
