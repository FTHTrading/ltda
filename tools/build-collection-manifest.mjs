// node tools/build-collection-manifest.mjs [version]
// Builds the LTDA collection (real-world archive) from data/collection/records.src.json:
//   one canonical JSON file per record, leaf = keccak256(sha256(record file)), sorted-pair keccak256 tree
//   (same method as the Power Punch history archive and 3fs docs manifest), proofs per record.
// Writes data/collection/<version>/records/*.json and data/collection/<version>/manifest.json.
// The root is what the owner anchors with PowerPunchUnit.anchorHistory(root, uri). This script sends nothing.
// A version folder is never rebuilt once its root has been handed out for anchoring: bump the version instead.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { createRequire } from "node:module";

const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1"));
const repo = path.join(here, "..");
const { keccak256, concat } = createRequire(import.meta.url)(
  path.join(repo, "..", "..", "..", "powerpunch-chain", "pp-chain", "node_modules", "ethers"));

export function canonical(v) {
  if (Array.isArray(v)) return "[" + v.map(canonical).join(",") + "]";
  if (v && typeof v === "object") return "{" + Object.keys(v).sort().map((k) => JSON.stringify(k) + ":" + canonical(v[k])).join(",") + "}";
  return JSON.stringify(v);
}

const pair = (a, b) => keccak256(concat(a < b ? [a, b] : [b, a]));

// leaves are record sha256 values; returns root and, per input index, the sibling path to the root
export function merkle(sha256s) {
  let layer = sha256s.map((s, i) => ({ h: keccak256(s), idx: [i] })).sort((a, b) => (a.h < b.h ? -1 : a.h > b.h ? 1 : 0));
  const proofs = sha256s.map(() => []);
  while (layer.length > 1) {
    const next = [];
    for (let i = 0; i < layer.length; i += 2) {
      if (i + 1 < layer.length) {
        const a = layer[i], b = layer[i + 1];
        a.idx.forEach((j) => proofs[j].push(b.h));
        b.idx.forEach((j) => proofs[j].push(a.h));
        next.push({ h: pair(a.h, b.h), idx: a.idx.concat(b.idx) });
      } else next.push(layer[i]);
    }
    layer = next;
  }
  return { root: layer[0].h, proofs };
}

export function verifyProof(sha256, proof, root) {
  return proof.reduce((h, sib) => pair(h, sib), keccak256(sha256)).toLowerCase() === root.toLowerCase();
}

function readHashes(tsv) {
  const out = {};
  for (const line of fs.readFileSync(tsv, "utf8").split(/\r?\n/)) {
    if (!line.trim()) continue;
    const [file, bytes, sha, folder] = line.split("\t");
    out[file.replace(/\.[^.]+$/, "")] = { file, bytes: Number(bytes), sha256: "0x" + sha, folder };
  }
  return out;
}

export function buildCollection(src, hashesTsv, outDir, version, builtAt = new Date().toISOString()) {
  const photos = readHashes(hashesTsv);
  fs.mkdirSync(path.join(outDir, "records"), { recursive: true });
  const items = src.records.map((r) => {
    const p = photos[r.photo];
    if (!p) throw new Error(`record ${r.id}: photo ${r.photo} is not in ${path.basename(hashesTsv)}`);
    const record = {
      schema: "ltda.collection.record/1",
      id: r.id, kind: r.kind, title: r.title, story: r.story, era: r.era,
      original: { held_by: "to record", location: "to record" },
      photo: { intake: p.file, bytes: p.bytes, sha256: p.sha256 },
      consent: "pending",
      publisher: "UnyKorn LLC (Wyoming) for Live the Dream Athletics",
      terms: "A record of history. Not a security, not for sale, carries no share of anything.",
    };
    const text = canonical(record) + "\n";
    const rel = path.posix.join("records", r.id + ".json");
    fs.writeFileSync(path.join(outDir, rel), text);
    return { id: r.id, title: r.title, path: rel, bytes: Buffer.byteLength(text), sha256: "0x" + crypto.createHash("sha256").update(text).digest("hex") };
  });
  const { root, proofs } = merkle(items.map((i) => i.sha256));
  items.forEach((it, i) => (it.proof = proofs[i]));
  const manifest = {
    name: "Live the Dream Athletics collection (real-world archive)",
    version, built: builtAt,
    publisher: "UnyKorn LLC (Wyoming) for Live the Dream Athletics",
    leaf: "keccak256(sha256(record file))",
    tree: "sorted-pair keccak256",
    merkleRoot: root, count: items.length,
    anchor: {
      chain: "base", chainId: 8453,
      contract: "0xCf1660AD2f6D0DD2E14924Fe96cDFC5199D6f052",
      method: "anchorHistory(bytes32 root, string uri)",
      uri: `https://livethedreamathletics.com/collection/${version}/manifest.json`,
      status: "PENDING_OWNER_TX",
    },
    items,
  };
  fs.writeFileSync(path.join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
  return manifest;
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1"))) {
  const version = process.argv[2] || "v0";
  const out = path.join(repo, "data", "collection", version);
  if (fs.existsSync(path.join(out, "manifest.json")) && !process.env.REBUILD) {
    console.error(`${version} already built; its root may have been handed out. Bump the version (or REBUILD=1 if it never was).`);
    process.exit(1);
  }
  const src = JSON.parse(fs.readFileSync(path.join(repo, "data", "collection", "records.src.json"), "utf8"));
  const m = buildCollection(src, path.join(repo, "data", "intake", "2026-10-26-onedrive-batch", "hashes.tsv"), out, version);
  console.log(`${m.count} records\nmerkleRoot ${m.merkleRoot}\nmanifest ${path.join(out, "manifest.json")}`);
}
