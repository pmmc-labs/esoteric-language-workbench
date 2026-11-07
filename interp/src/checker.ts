// The checker: every error D28 and D31 say comes before running, found
// before anything is evaluated, in every definition and branch whether
// taken or not (D7). It recurses over the forms, which the reader has
// bounded (D30). A program is definitions and then one expression (D31);
// what comes back is the program split into those two parts, with each
// function's parameters resolved.

import { CheckError } from "./errors.ts";
import type { Form, ListForm } from "./reader.ts";
import { OPERATORS } from "./evaluator.ts";

export type Def = { name: string; params: string[]; body: Form };
export type Program = { defs: Map<string, Def>; expr: Form };

// Names that are not a function's: the operators, and the forms that
// aren't operators (D31).
const reserved = (name: string) => OPERATORS.has(name) || name === "if" || name === "within" || name === "def";

const isDef = (f: Form): f is ListForm => f.t === "list" && f.items[0]?.t === "sym" && f.items[0].name === "def";

export function check(forms: Form[]): Program {
  // Definitions, then one expression, and nothing after it (D31).
  const j = forms.findIndex((f) => !isDef(f));
  if (j === -1) {
    const last = forms[forms.length - 1];
    throw new CheckError("a program of definitions needs an expression after them", last.line, last.col);
  }
  if (j + 1 < forms.length) {
    const g = forms[j + 1];
    throw new CheckError(
      isDef(g) ? "a definition after the expression" : "a second expression after the program's expression",
      g.line, g.col);
  }

  // Pass one: each definition's shape and name. Every name is known
  // before any parameter is checked against it, since a parameter may not
  // have the name of any function (D31).
  const heads: { name: string; sig: ListForm; body: Form }[] = [];
  const names = new Set<string>();
  for (const d of forms.slice(0, j) as ListForm[]) {
    if (d.items.length !== 3)
      throw new CheckError(`def takes 2 arguments, not ${d.items.length - 1}`, d.line, d.col);
    const sig = d.items[1];
    if (sig.t !== "list")
      throw new CheckError("a definition's first part is its name and parameters, in a list", sig.line, sig.col);
    const nm = sig.items[0];
    if (nm === undefined) throw new CheckError("a definition needs a name", sig.line, sig.col);
    if (nm.t !== "sym") throw new CheckError("a definition needs a name", nm.line, nm.col);
    if (reserved(nm.name)) throw new CheckError(`${nm.name} is not a name for a function`, nm.line, nm.col);
    if (names.has(nm.name)) throw new CheckError(`two definitions of ${nm.name}`, nm.line, nm.col);
    names.add(nm.name);
    heads.push({ name: nm.name, sig, body: d.items[2] });
  }

  // Pass two: parameters, each a name no function or operator has, and no
  // two of one name.
  const defs = new Map<string, Def>();
  for (const h of heads) {
    const params: string[] = [];
    for (const p of h.sig.items.slice(1)) {
      if (p.t !== "sym") throw new CheckError("a parameter is a name, not a number or boolean", p.line, p.col);
      if (reserved(p.name)) throw new CheckError(`${p.name} is not a name for a parameter`, p.line, p.col);
      if (names.has(p.name)) throw new CheckError(`${p.name} is the name of a function`, p.line, p.col);
      if (params.includes(p.name)) throw new CheckError(`two parameters named ${p.name}`, p.line, p.col);
      params.push(p.name);
    }
    defs.set(h.name, { name: h.name, params, body: h.body });
  }

  // Pass three: every body, then the expression, with the parameters in
  // scope, and no definition anywhere but the top (D31).
  for (const d of defs.values()) checkForm(d.body, new Set(d.params), defs);
  checkForm(forms[j], new Set(), defs);
  return { defs, expr: forms[j] };
}

function checkForm(f: Form, scope: Set<string>, defs: Map<string, Def>): void {
  switch (f.t) {
    case "int":
    case "bool":
      return;
    case "sym":
      if (scope.has(f.name)) return;
      if (defs.has(f.name)) throw new CheckError(`${f.name} is a function, not a value`, f.line, f.col);
      throw new CheckError(`unknown name ${f.name}`, f.line, f.col);
    case "list": {
      const head = f.items[0];
      if (head === undefined || head.t !== "sym")
        throw new CheckError("a list must start with an operator", f.line, f.col);
      if (head.name === "def")
        throw new CheckError("a definition is only at the top of the program", f.line, f.col);
      if (scope.has(head.name))
        throw new CheckError(`${head.name} is a parameter, not a function`, head.line, head.col);
      const arity = defs.has(head.name)
        ? defs.get(head.name)!.params.length
        : OPERATORS.has(head.name) ? 2 : head.name === "if" ? 3 : head.name === "within" ? 2 : undefined;
      if (arity === undefined) throw new CheckError(`unknown name ${head.name}`, head.line, head.col);
      const n = f.items.length - 1;
      if (n !== arity) throw new CheckError(`${head.name} takes ${arity} arguments, not ${n}`, f.line, f.col);
      for (let k = 1; k <= n; k++) checkForm(f.items[k], scope, defs);
    }
  }
}
