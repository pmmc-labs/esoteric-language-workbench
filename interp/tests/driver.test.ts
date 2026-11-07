import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";

mkdirSync("build/unit", { recursive: true });
let n = 0;
// Runs a program through the driver under this test's own Node.
export function run(src: string) {
  const path = `build/unit/drv${n++}.lang`;
  writeFileSync(path, src);
  const r = spawnSync(process.execPath, ["bin/lang.ts", path], { encoding: "utf8" });
  return { path, out: r.stdout, err: r.stderr, status: r.status };
}

test("a value prints, exit 0", () => {
  const r = run("42");
  assert.deepEqual([r.out, r.err, r.status], ["42\n", "", 0]);
});

test("an error before running is FILE:LINE:COL: message, exit 2", () => {
  const r = run("\n 99999999999999999999");
  assert.equal(r.out, "");
  assert.equal(r.err, `${r.path}:2:2: integer 99999999999999999999 is out of range (63 bits)\n`);
  assert.equal(r.status, 2);
});

test("a usage error is exit 2", () => {
  const r = spawnSync(process.execPath, ["bin/lang.ts"], { encoding: "utf8" });
  assert.equal(r.status, 2);
  assert.match(r.stderr, /^usage/);
  const m = spawnSync(process.execPath, ["bin/lang.ts", "build/no-such-file"], { encoding: "utf8" });
  assert.equal(m.status, 2);
});
