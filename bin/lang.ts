// The driver: `node bin/lang.ts FILE` reads, checks, evaluates and prints.
// Exit 0 with the value on stdout; 1 for a fault (D6); 2 for an error
// before running, a usage error or an unreadable file (D28); 3 for a
// fault in the interpreter itself.
import { readFileSync } from "node:fs";
import { read } from "../interp/src/reader.ts";
import { check } from "../interp/src/checker.ts";
import { evaluate, show } from "../interp/src/evaluator.ts";
import { CompileError, Fault } from "../interp/src/errors.ts";

const file = process.argv[2];
if (process.argv.length !== 3) {
  console.error("usage: lang FILE");
  process.exit(2);
}
let text: string;
try {
  text = readFileSync(file, "utf8");
} catch (e) {
  console.error(`lang: can't read ${file}: ${(e as Error).message}`);
  process.exit(2);
}
try {
  const out = show(evaluate(check(read(text))));
  process.stdout.write(out + "\n");
} catch (e) {
  if (e instanceof CompileError) {
    console.error(`${file}:${e.line}:${e.col}: ${e.message}`);
    process.exit(2);
  } else if (e instanceof Fault) {
    console.error(`fault: ${e.message}`);
    process.exit(1);
  }
  console.error(`lang: internal error: ${(e as Error).stack}`);
  process.exit(3);
}
