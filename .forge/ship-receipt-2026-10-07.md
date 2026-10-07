# Ship receipt — FTHTrading/ltda created, livethedreamathletics.com redeployed from it (2026-10-07)

```
FORGE-CLASS: entity=UnyKorn LLC sec=LOW claims=MARKETING custody=NONE hearth=NONE chain=READ surface=PUBLIC
```
Requested by Kevan in chat 2026-10-07 (empty public repo created by him; "add in the NIL ... professional, color coded, table of contents and flow trees").

## What went where

| What | Surface | Rollback |
|---|---|---|
| Repository `FTHTrading/ltda`, branch `main`, first commit `6d218be`: site source copied from `powerpunch-chain/ltda-v2` (served state of 2026-09-19 `fa44203`) + worker + build + copy gate + README | github.com (PUBLIC) | delete or re-point the repo; monorepo copies untouched |
| `build.py`: data path -> `data/base.json`, UTF-8 output; `/fund/` and `/systems/` reworded (501(c)(3) / tax-deductible removed, fails `copy-gate.js`, F-7 open); `/nil33/` links nil33.com/transparency and /chaos | livethedreamathletics.com (PUBLIC) | `wrangler rollback --name ltda-site`, or redeploy from the monorepo `ltda/` folder |
| Worker `ltda-site` deployed from this repo, version `3251ba4f-be41-4c41-92a1-55eb03d6405e` | livethedreamathletics.com, www | same |

Excluded on purpose: `ltda/docs/*` (internal plan, RockFence dossier, raw Facebook timeline naming minors and third parties), v1 site, `pp-chain` contracts, every key or wallet. Secrets scan of the copied tree: no hits (only public SHA-256 digests).

## Served verification

| Surface | Served check | Result |
|---|---|---|
| /api/health | body | `{"ok":true,"site":"livethedreamathletics.com"}` |
| /fund/ | "501(c)" or "tax-deductible" / new wording | 0 / 1 |
| /systems/ | "501(c)" | 0 |
| /nil33/ | `href="https://nil33.com/transparency"` / chaos link | 1 / 1 |
| / | status, title | 200, Live the Dream Athletics |
| /proof/, /archive/manifest.json | status | 200 / 200 |
| /nope | 404 page | 404 |
| www /api/health | redirect | 301 -> apex (worker handles www) |
| www / | **200, CF-Cache-Status: HIT** | a stale edge-cached 200 predating the worker's www redirect; see carry forward |

On-chain facts in the README re-verified 2026-10-07 against `https://mainnet.base.org`: four receipts `status 0x1`, anchor input contains root `0x6194…b08f`, both contracts hold bytecode, unit `name()` = "Power Punch Unit". Blockscout MCP was out of credits (HTTP 402) and the Blockscout web API challenged curl; the public RPC was used instead.

## Carry forward
- **www root cache.** `https://www.livethedreamathletics.com/` returns a cached 200 (CF-Cache-Status HIT) even with a unique query string, while `/api/health` on www correctly 301s. Needs a cache purge for that URL in the Cloudflare zone (dashboard: Caching -> Purge by URL), which is a production zone action I did not take. Not caused by this deploy.
- **Monorepo copies are stale.** `powerpunch-chain/ltda` and `ltda-v2` still hold the pre-reword pages; this repo is now the source of record for the site. A one-line pointer in the monorepo is the next housekeeping step.
- **Spanish edition.** `tools/make-es.js` targets the v1 home page and will not run against v2 without re-pointing.
- **F-7** (fund legal wrapper) remains open; the stronger charitable wording stays out until it is signed.
