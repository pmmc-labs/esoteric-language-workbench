import { fail } from "./errors.ts";
import type { Expr, Program, Stmt } from "./parser.ts";

// Names (D14). `scopes` is a stack of sets, innermost last: a name is
// visible if any scope holds it, and declaring a visible name is an error,
// so there is no shadowing. A block pushes a scope on entry and pops it on
// exit, so a name from a finished block is gone (D38); step 4's functions
// start from an empty stack.
export function resolve(prog: Program): Program {
  const scopes: Set<string>[] = [new Set()];
  const visible = (n: string) => scopes.some((s) => s.has(n));

  const expr = (e: Expr): void => {
    switch (e.k) {
      case "int": return;
      case "name":
        if (!visible(e.name)) fail(e.line, e.col, `unknown variable ${e.name}`);
        return;
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
    } else {
      expr(s.e);
    }
  };

  prog.stmts.forEach(stmt);
  return prog;
}
