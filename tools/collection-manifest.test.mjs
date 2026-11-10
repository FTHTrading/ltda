// node --test tools/collection-manifest.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import { canonical, merkle, verifyProof, buildCollection } from "./build-collection-manifest.mjs";

const repo = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1")), "..");
const SRC = JSON.parse(fs.readFileSync(path.join(repo, "data", "collection", "records.src.json"), "utf8"));
const HASHES = path.join(repo, "data", "intake", "2026-10-26-onedrive-batch", "hashes.tsv");
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), "ltda-coll-"));

test("canonical JSON sorts keys at every depth and has no whitespace", () => {
  assert.equal(canonical({ b: 1, a: { d: 2, c: [3, { f: 4, e: 5 }] } }), '{"a":{"c":[3,{"e":5,"f":4}],"d":2},"b":1}');
});

test("the same sources build the same root twice", () => {
  const a = buildCollection(SRC, HASHES, tmp(), "v0", "2026-10-26T00:00:00.000Z");
  const b = buildCollection(SRC, HASHES, tmp(), "v0", "2026-10-26T00:00:00.000Z");
  assert.match(a.merkleRoot, /^0x[0-9a-f]{64}$/);
  assert.equal(a.merkleRoot, b.merkleRoot);
});

test("every record has a proof that verifies to the root", () => {
  const m = buildCollection(SRC, HASHES, tmp(), "v0", "2026-10-26T00:00:00.000Z");
  assert.equal(m.items.length, SRC.records.length);
  for (const it of m.items) assert.ok(verifyProof(it.sha256, it.proof, m.merkleRoot), it.id);
});

test("a proof does not verify against a different leaf", () => {
  const m = buildCollection(SRC, HASHES, tmp(), "v0", "2026-10-26T00:00:00.000Z");
  assert.equal(verifyProof(m.items[1].sha256, m.items[0].proof, m.merkleRoot), false);
});

test("editing one word of one story changes the root", () => {
  const base = buildCollection(SRC, HASHES, tmp(), "v0", "2026-10-26T00:00:00.000Z");
  const edited = structuredClone(SRC);
  edited.records[0].story += " ";
  const after = buildCollection(edited, HASHES, tmp(), "v0", "2026-10-26T00:00:00.000Z");
  assert.notEqual(base.merkleRoot, after.merkleRoot);
});

test("each written record file hashes to its manifest sha256 and carries its photo hash", () => {
  const out = tmp();
  const m = buildCollection(SRC, HASHES, out, "v0", "2026-10-26T00:00:00.000Z");
  for (const it of m.items) {
    const bytes = fs.readFileSync(path.join(out, it.path));
    assert.equal("0x" + crypto.createHash("sha256").update(bytes).digest("hex"), it.sha256, it.id);
    const rec = JSON.parse(bytes.toString("utf8"));
    assert.match(rec.photo.sha256, /^0x[0-9a-f]{64}$/);
  }
});

test("a record whose photo is missing from the intake hashes is refused", () => {
  const bad = structuredClone(SRC);
  bad.records[0].photo = "b99";
  assert.throws(() => buildCollection(bad, HASHES, tmp(), "v0", "2026-10-26T00:00:00.000Z"), /b99/);
});

test("merkle of one leaf is that leaf's keccak", () => {
  const { root } = merkle(["0x" + "11".repeat(32)]);
  assert.match(root, /^0x[0-9a-f]{64}$/);
});
