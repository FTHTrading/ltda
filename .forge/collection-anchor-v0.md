# Collection: v0 and v1 SUPERSEDED by v2 (none sent)

> 2026-10-26, later still: Kevan reframed LTDA-001 ("that's my son ... the legacy of playing ball and passing it on to your kids"). Built **v2**, root `0xe6b59b85226808846b979fbc46e7596e3781772d6badece06f60c58fa6c6afb5` (`data/collection/v2/manifest.json`). v1 kept unchanged and must not be anchored. Same pre-anchor list applies to v2.

# Collection v0: SUPERSEDED by v1 (never sent)

> 2026-10-26, later the same day: Kevan gave the stories (his son below the bat; Troy Hall of Fame induction jerseys; Falcons uniform with his grandmother; himself at the plate and as a kid). Built as **v1**, root `0xd68fa09151d9126cc3743805ffee8f28161c20300a93b433ce225e9dbecd67f7` (`data/collection/v1/manifest.json`). v0 is kept unchanged for the record and must not be anchored. Before anchoring v1: era/induction year, where each original is kept, a source for the Troy Hall of Fame line on any public page, and a yes for the photo of Kevan's son and of his grandmother.

# Collection v0 (original note below, unchanged)

Built 2026-10-26. No transaction was sent. Anchoring is Kevan's go, from the owner keystore, per the record protocol.

| | |
|---|---|
| Manifest | `data/collection/v0/manifest.json` (6 records, proofs per record) |
| Records | `data/collection/v0/records/LTDA-001..006.json` (canonical JSON, sorted keys, LF) |
| Leaf / tree | keccak256(sha256(record file)), sorted-pair keccak256: same method as the anchored history archive |
| **Merkle root** | `0xa5c4fdc18f77234ce912ade4fd0c6acb9c29db909a72d6fade4e732e3d91ad40` |
| Contract | PowerPunchUnit `0xCf1660AD2f6D0DD2E14924Fe96cDFC5199D6f052` (Base, chainId 8453) |
| Call | `anchorHistory(root, "https://livethedreamathletics.com/collection/v0/manifest.json")` |

## Checks run
- `node --test tools/collection-manifest.test.mjs`: 8/8 pass (reproducible root, every proof verifies, wrong leaf fails, one-word edit changes root, record file hash matches, unknown photo refused).
- The same Merkle code re-derives the anchored archive root `0x619420a4…34b08f` from `public/archive/manifest.json`: MATCH.
- Independent Python (pycryptodome keccak) rebuild of the v0 root from the record files: MATCH.

## Before sending (why v0 should probably not be the one anchored)
- Every record still says era "to confirm", original "to record", consent "pending". An anchor is permanent and append-only: anchoring v0 freezes those placeholders on chain forever (a later version can supersede, never erase).
- The anchor URI must serve the manifest before or right after the tx (`/collection/v0/manifest.json` is not deployed; the photos are not cleared to publish).
- Recommended: Kevan fills story, era and where each original is kept; consents land; build **v1** (`node tools/build-collection-manifest.mjs v1`); publish manifest; then anchor v1.

## Rollback
Nothing to roll back: nothing was sent. The builder refuses to overwrite a built version (bump the version instead), so a root handed out can't drift.

## To send (owner only, when Kevan says go)
An owner script for this root does not exist yet. `pp-chain/scripts/anchor-3fs.js` is the template (reads a manifest, skips if already anchored, calls anchorHistory, writes anchor.json). Copying it for the collection is a change in the powerpunch-chain repo, waiting on Kevan's yes.
