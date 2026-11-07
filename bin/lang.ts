// The driver: `node bin/lang.ts FILE` reads, checks, evaluates and prints.
// Exit 0 with the value; 1 for a fault (D6); 2 for an error before
// running or a usage error (D28); 3 for the interpreter's own fault (D30).
// Output is written synchronously and the status set, not exited with,
// so a pipe is never cut off.

import { readFileSync, writeSync } from "node:fs";
import { read } from "../interp/src/reader.ts";
import { check } from "../interp/src/checker.ts";
import { evaluate, show } from "../interp/src/evaluator.ts";
import { CheckError, Fault } from "../interp/src/errors.ts";

const out = (fd: number, s: string) => writeSync(fd, s);

function main(): number {
  const file = process.argv[2];
  if (process.argv.length !== 3 || file === undefined) {
    out(2, "usage: lang FILE\n");
    return 2;
  }
  let src: string;
  try {
    // Bytes, decoded strictly and keeping a byte order mark (D31): the
    // default replaces a bad byte and drops a BOM.
    src = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(readFileSync(file));
  } catch (e) {
    if (e instanceof TypeError) {
      out(2, `${file}:1:1: the file is not valid UTF-8\n`);
      return 2;
    }
    out(2, `lang: cannot read ${file}: ${(e as Error).message}\n`);
    return 2;
  }
  try {
    const form = read(src);
    check(form);
    out(1, show(evaluate(form)) + "\n");
    return 0;
  } catch (e) {
    if (e instanceof CheckError) {
      out(2, `${file}:${e.line}:${e.col}: ${e.message}\n`);
      return 2;
    }
    if (e instanceof Fault) {
      out(2, `fault: ${e.message}\n`);
      return 1;
    }
    out(2, `lang: internal error: ${(e as Error).stack ?? e}\n`);
    return 3;
  }
}

process.exitCode = main();
