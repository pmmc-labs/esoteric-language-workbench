// The checker: every error D28 says comes before running. Forms in, a
// tree the evaluator walks out; errors are found in reading order, a
// form's own shape before its parts.
import { CompileError } from "./errors.ts";
import { ops } from "./ops.ts";
import type { Form } from "./reader.ts";

export type Value = bigint | boolean;
export type Node =
  | { kind: "lit"; value: Value }
  | { kind: "op"; name: string; a: Node; b: Node };

export function check(forms: Form[]): Node {
  if (forms.length === 0) throw new CompileError("empty program", 1, 1);
  if (forms.length > 1) throw new CompileError("a program is one expression", forms[1].line, forms[1].col);
  return expr(forms[0]);
}

function expr(f: Form): Node {
  switch (f.kind) {
    case "int": return { kind: "lit", value: f.value };
    case "sym": throw new CompileError(`unknown name: ${f.name}`, f.line, f.col);
    case "list": return list(f);
  }
}

function list(f: Extract<Form, { kind: "list" }>): Node {
  const [head, ...args] = f.items;
  if (!head) throw new CompileError("empty list", f.line, f.col);
  if (head.kind !== "sym") throw new CompileError("not an operator", head.line, head.col);
  if (ops.has(head.name)) {
    if (args.length !== 2) throw new CompileError(`${head.name} takes 2 arguments, not ${args.length}`, f.line, f.col);
    return { kind: "op", name: head.name, a: expr(args[0]), b: expr(args[1]) };
  }
  throw new CompileError(`unknown name: ${head.name}`, head.line, head.col);
}
