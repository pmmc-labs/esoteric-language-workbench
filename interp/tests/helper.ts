import { read } from "../src/reader.ts";
import { check } from "../src/checker.ts";
import { evaluate, show } from "../src/evaluator.ts";
import { CheckError, Fault } from "../src/errors.ts";

// A program's outcome as the driver would report it: its printed value,
// `fault: NAME`, or `error L:C message`. Host exceptions pass through.
export function run(src: string): string {
  try {
    return show(evaluate(check(read(src))));
  } catch (e) {
    if (e instanceof Fault) return `fault: ${e.message}`;
    if (e instanceof CheckError) return `error ${e.line}:${e.col} ${e.message}`;
    throw e;
  }
}
