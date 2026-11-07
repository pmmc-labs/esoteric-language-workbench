import { fail } from "./errors.ts";
import type { Expr, Fn, Program, Stmt } from "./parser.ts";

// Names (D14). `scopes` is a stack of sets, innermost last: a name is
// visible if any scope holds it, and declaring a visible name is an error,
// so there is no shadowing. A block pushes a scope on entry and pops it on
// exit, so a name from a finished block is gone (D38); each function starts
// from an empty stack, so it sees none of the main program's names (D18).
// Function names are a separate namespace, collected before any body is
// checked, which is what makes hoisting work (D39).
const BUILTINS = new Set(["len", "at", "str"]);

export function resolve(prog: Program): Program {
  let scopes: Set<string>[] = [new Set()];
  let inFn = false;
  const fns = new Map<string, Fn>();
  for (const f of prog.fns) {
    if (BUILTINS.has(f.name)) fail(f.line, f.col, `${f.name} is a builtin`);
    if (fns.has(f.name)) fail(f.line, f.col, `${f.name} is already defined`);
    fns.set(f.name, f);
  }
  const visible = (n: string) => scopes.some((s) => s.has(n));

  const expr = (e: Expr): void => {
    switch (e.k) {
      case "int": return;
      case "name":
        if (!visible(e.name)) fail(e.line, e.col, `unknown variable ${e.name}`);
        return;
      case "call": {
        const f = fns.get(e.name);
        if (!f) fail(e.line, e.col, `unknown function ${e.name}`);
        if (f.params.length !== e.args.length) {
          const n = f.params.length;
          fail(e.line, e.col,
            `${e.name} takes ${n} argument${n === 1 ? "" : "s"}, given ${e.args.length}`);
        }
        e.args.forEach(expr);
        return;
      }
      case "list": e.elems.forEach(expr); return;
      case "at": expr(e.e); expr(e.i); return;
      case "un": expr(e.e); return;
      case "bin": expr(e.l); expr(e.r); return;
    }
  };

  // A block's names die with it. The condition is resolved outside it.
  const block = (body: Stmt[]): void => {
    scopes.push(new Set());
    body.forEach(stmt);
    scopes.pop();
  };

  const stmt = (s: Stmt): void => {
    if (s.k === "if") {
      expr(s.cond);
      block(s.then);
      if (s.els) block(s.els);
    } else if (s.k === "while") {
      expr(s.cond);
      block(s.body);
    } else if (s.k === "let") {
      // Checked before the initializer is resolved (source order), but the
      // name is added after it: `let x = x` reads an unknown x.
      if (visible(s.name)) fail(s.line, s.col, `${s.name} is already declared`);
      expr(s.e);
      scopes[scopes.length - 1].add(s.name);
    } else if (s.k === "set") {
      if (!visible(s.name)) fail(s.nline, s.ncol, `unknown variable ${s.name}`);
      expr(s.e);
    } else if (s.k === "return") {
      if (!inFn) fail(s.line, s.col, "return outside a function");
      expr(s.e);
    } else {
      expr(s.e);
    }
  };

  for (const f of prog.fns) {
    scopes = [new Set()];
    for (const a of f.params) {
      if (scopes[0].has(a.name)) fail(a.line, a.col, `${a.name} is already declared`);
      scopes[0].add(a.name);
    }
    inFn = true;
    block(f.body);
  }
  inFn = false;
  scopes = [new Set()];
  prog.stmts.forEach(stmt);
  return prog;
}
