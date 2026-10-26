# Brief: the Youth Shield (young-athlete protection layer)

```
FORGE-CLASS: entity=UnyKorn LLC  sec=HIGH (minors' personal data)  claims=REGULATED
             custody=NONE  hearth=NONE  chain=ISSUE (fingerprints only, later)
             surface=PUBLIC
Routing: COUNSEL/FOUNDER GATE FIRST (COPPA, FERPA, state rules) before any real child's data is collected.
Status: DESIGN. No code, no data collected. The public page says "in design".
```

## What / why
Kevan, 2026-10-26: young players' information should only reach the right people. Showcase, scouting and recruiting
pages put a minor's height, weight, school, hometown, grad year and stats in public, and that can be dangerous. The Shield
is a record the family controls: verified facts about the player, shared one answer at a time with people the parent
approves, never published to everyone. It plugs into LTDA (youth) and carries into NIL33 when the player is older.

## The design (v1: buildable now with standard parts)
1. **Parent opens it.** Under 18 nothing exists without a parent's signature; under 13 only with verifiable parental
   consent (COPPA). The player takes control at 18.
2. **Data stays private.** Facts are stored encrypted (envelope encryption, KMS-held key per ANVIL §5), never on chain.
   Only a fingerprint (SHA-256) of each signed fact goes into a Merkle root that may be anchored, same method as the
   collection.
3. **Facts are signed by whoever measured them.** An event signs "60-yard dash 6.8 s", a coach signs a milestone, a
   school (with FERPA consent) signs a grade band. ES256 signatures, as NIL33's KYA assertions already use.
4. **Share answers, not files.** A recruiter asks a question ("16 or older?", "GPA 3.0+?", "60 under 7.0?") and gets a
   signed yes/no for that one predicate. Birth date, transcript, address are never handed over.
5. **The parent approves every viewer.** Access is a grant to a named, verified person or program, for a set time, for
   a set list of questions. Grants expire and can be revoked.
6. **Every look is logged.** The family sees who asked what and when. Logs are append-only.
7. **Default: nothing public.** No public profile page for anyone under 18. Ever.

## v2 (only after v1 has users and an external audit)
Real zero-knowledge selective disclosure (BBS+ signatures or a range-proof circuit) so even the yes/no can be checked
without our server in the middle. The words "zero-knowledge" appear on a public surface only after v2 ships and is
audited (global ADR-0002; LTDA ADR-0002).

## Out of scope (now)
Collecting any real child's data; a public player directory; selling or licensing any youth data (never).

## Acceptance (for the first build task, later)
- A grant-less request for any predicate is refused (exercised as the role, not read from policy).
- A revoked or expired grant is refused.
- Every successful answer writes a log row the parent can read; the requester cannot read the log.
- No field other than the predicate result leaves the server for a grant-holder.
- Nothing about a minor is retrievable without a grant; no endpoint lists minors.

## Claims allowed on the page (now)
"In design" · "the family decides who sees it" · "a recruiter gets the yes or no they asked for, not the file" ·
"every look is logged and the family can see it" · "nothing about a player under 18 is public" ·
"nothing happens without a parent's signature".
Not allowed: "zero-knowledge", "fully private", "guaranteed", "secure" as an absolute, any partner's name as if
they use it.

## Counsel questions (before any real data)
COPPA verifiable consent method for under-13; FERPA consent flow for school-signed facts; state HS association rules
on recruiting contact and NIL; data retention and deletion at the family's request; breach notice duties.

## Partner angle (non-confrontational)
Offered to showcase, scouting and recruiting platforms as a privacy layer they can add for their under-18 players,
not as a rival service. See `.forge/nil-landscape-partners-2026-10-26.md` once written.
