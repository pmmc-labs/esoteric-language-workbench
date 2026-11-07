import assert from "node:assert/strict";
import { read } from "../src/reader.ts";
import { check } from "../src/checker.ts";
import { evaluate, show } from "../src/evaluator.ts";
import { CompileError, Fault } from "../src/errors.ts";

// A program's output, "LINE:COL: message" for an error before running, or
// "fault: message" for a fault.
export const run = (src: string) => show(evaluate(check(read(src))));
export const fault = (src: string) => {
  try { run(src); } catch (e) { if (e instanceof Fault) return e.message; throw e; }
  assert.fail("no fault");
};
export const err = (src: string) => {
  try { check(read(src)); } catch (e) { if (e instanceof CompileError) return `${e.line}:${e.col}: ${e.message}`; throw e; }
  assert.fail("no error");
};

