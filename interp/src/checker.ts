// The checker: every error D28 says comes before running, found before
// anything is evaluated, in every branch whether taken or not (D7, D31).
// It recurses; the reader has already bounded the depth (D30).

import { CheckError } from "./errors.ts";
import type { Form } from "./reader.ts";
import { OPERATORS } from "./evaluator.ts";
import type { Program } from "./evaluator.ts";

const SPECIAL = new Map([["if", 3], ["within", 2]]);
const reserved = (n: string) => OPERATORS.has(n) || SPECIAL.has(n) || n === "def";
const isDef = (f: Form) => f.t === "list" && f.items[0]?.t === "sym" && f.items[0].name === "def";

export function check(forms: Form[]): Program {
  // The definitions come first and the expression last (D31).
  const k = forms.findIndex((f) => !isDef(f));
  if (k < 0) {
    const l = forms[forms.length - 1];
    throw new CheckError("a program needs an expression after its definitions", l.line, l.col);
  }
  if (k < forms.length - 1) {
    const x = forms[k + 1];
    throw new CheckError(isDef(x) ? "a definition must come before the expression" : "unexpected form after the program", x.line, x.col);
  }

  // Pass 1: every function's name and parameters, so each sees every
  // other whatever their order.
  const fns: Program["fns"] = new Map();
  const defs: { params: Set<string>; toks: { name: string; line: number; col: number }[]; body: Form }[] = [];
  for (const d of forms.slice(0, k)) {
    const items = (d as { items: Form[] }).items;
    if (items.length !== 3) throw new CheckError(`def takes a header and a body, not ${items.length - 1} parts`, d.line, d.col);
    const [, head, body] = items;
    if (head.t !== "list" || head.items.length === 0 || head.items.some((x) => x.t !== "sym"))
      throw new CheckError("def needs (name param ...), names only", head.line, head.col);
    const [name, ...params] = head.items as { t: "sym"; name: string; line: number; col: number }[];
    if (reserved(name.name)) throw new CheckError(`${name.name} is reserved`, name.line, name.col);
    if (fns.has(name.name)) throw new CheckError(`${name.name} is already defined`, name.line, name.col);
    const seen = new Set<string>();
    for (const p of params) {
      if (reserved(p.name)) throw new CheckError(`${p.name} is reserved`, p.line, p.col);
      if (seen.has(p.name)) throw new CheckError(`parameter ${p.name} is repeated`, p.line, p.col);
      seen.add(p.name);
    }
    fns.set(name.name, { params: params.map((p) => p.name), body });
    defs.push({ params: seen, toks: params, body });
  }
  // Pass 2: the names a parameter may not take (a function's) and the bodies.
  for (const d of defs)
    for (const p of d.toks)
      if (fns.has(p.name)) throw new CheckError(`parameter ${p.name} is the name of a function`, p.line, p.col);
  const arity = (n: string) => fns.get(n)?.params.length;
  const expr = (f: Form, scope: Set<string>): void => {
    switch (f.t) {
      case "int":
      case "bool":
        return;
      case "sym":
        if (scope.has(f.name)) return;
        throw new CheckError(fns.has(f.name) ? `${f.name} is a function, not a value` : `unknown name ${f.name}`, f.line, f.col);
      case "list": {
        const head = f.items[0];
        if (head === undefined || head.t !== "sym") throw new CheckError("a list must start with an operator", f.line, f.col);
        const n = f.items.length - 1;
        if (scope.has(head.name)) throw new CheckError(`${head.name} is a parameter, not a function`, head.line, head.col);
        if (head.name === "def") throw new CheckError("def only at the top of the program", head.line, head.col);
        const want = OPERATORS.has(head.name) ? 2 : SPECIAL.get(head.name) ?? arity(head.name);
        if (want === undefined) throw new CheckError(`unknown name ${head.name}`, head.line, head.col);
        if (n !== want) throw new CheckError(`${head.name} takes ${want} arguments, not ${n}`, f.line, f.col);
        for (let i = 1; i <= n; i++) expr(f.items[i], scope);
      }
    }
  };
  for (const d of defs) expr(d.body, d.params);
  expr(forms[k], new Set());
  return { fns, main: forms[k] };
}
