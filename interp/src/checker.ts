// The checker: every error D28 says comes before running. Forms in, a
// tree the evaluator walks out; errors are found in reading order.
import { CompileError } from "./errors.ts";
import type { Form } from "./reader.ts";

export type Value = bigint | boolean;
export type Node = { kind: "lit"; value: Value };

export function check(forms: Form[]): Node {
  if (forms.length === 0) throw new CompileError("empty program", 1, 1);
  if (forms.length > 1) throw new CompileError("a program is one expression", forms[1].line, forms[1].col);
  return expr(forms[0]);
}

function expr(f: Form): Node {
  switch (f.kind) {
    case "int": return { kind: "lit", value: f.value };
    case "sym": throw new CompileError(`unknown name: ${f.name}`, f.line, f.col);
    case "list": throw new CompileError("can't evaluate a list yet", f.line, f.col);
  }
}
