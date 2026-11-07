import { readFileSync, writeFileSync } from "node:fs";
import { codegen } from "./codegen.ts";
import { formatError, isCompileError } from "./errors.ts";
import { lex } from "./lexer.ts";
import { parse } from "./parser.ts";
import { resolve } from "./resolve.ts";

// usage: main.ts FILE.strata OUT.c   (bin/strata drives this)
// Exit 0 on success, 2 on a compile error; anything else is a compiler bug.
const [file, out] = process.argv.slice(2);
try {
  // latin1: one char per byte, so columns are byte columns (D24).
  const src = readFileSync(file, "latin1");
  writeFileSync(out, codegen(resolve(parse(lex(src)))));
} catch (e) {
  if (!isCompileError(e)) throw e;
  process.stderr.write(formatError(e) + "\n");
  process.exit(2);
}
