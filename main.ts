import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The cover image lives beside this entrypoint in the repository.
// Resolve it from the module's own URL: the grader runs us from a
// different working directory, so a cwd-relative path would miss it.
const repoDir = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(repoDir, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });

const image = readFileSync(sourcePath);
if (image.length === 0) {
  throw new Error("entry.png is empty");
}
// A PNG must start with its eight-byte signature; refuse anything else
// rather than copying a corrupt or mistyped file into the output.
const pngSignature = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
if (!image.subarray(0, 8).equals(pngSignature)) {
  throw new Error("entry.png is not a PNG file");
}
if (image.length > 1048576) {
  throw new Error(`entry.png is ${image.length} bytes, over the 1 MiB cap`);
}

const digest = createHash("sha256").update(image).digest("hex");
const destPath = join(outDir, "entry.png");
writeFileSync(destPath, image);

// Read the copy back and prove it matches the source byte for byte.
const written = readFileSync(destPath);
const writtenDigest = createHash("sha256").update(written).digest("hex");
if (written.length !== image.length || writtenDigest !== digest) {
  throw new Error("integrity check failed: output differs from entry.png");
}

console.log(`entry.png ${image.length} bytes sha256 ${digest}`);
