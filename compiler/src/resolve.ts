// Names, scopes and the placement of `break`/`continue` (D12); step 3 adds
// user functions and arity. Returns a new program: the input is not changed.
import { compileError } from './errors.ts';
import type { Pos } from './errors.ts';
import type { Expr, Iter, Program, Stmt, Target } from './parser.ts';

// arity: the exact number of arguments, or null for any number.
export const BUILTINS: Record<string, { arity: number | null }> = {
  print: { arity: null },
};

// A function body (and the top level) has a stack of block scopes and a count
// of the loops around the statement being resolved. Step 3 makes one per
// function, so a function sees nothing of the top level (D13).
type Ctx = { scopes: Set<string>[]; loops: number };

// C names: no shadowing means a name is one variable within a function, so the
// name alone is enough to tell variables apart.
const cname = (name: string) => `v_${name}`;

const isDeclared = (ctx: Ctx, name: string) => ctx.scopes.some((s) => s.has(name));

// Declaring is checked at the new name, against every enclosing block.
function checkNew(ctx: Ctx, name: string, pos: Pos) {
  if (isDeclared(ctx, name)) throw compileError(pos, `${name} is already declared`);
}

function declare(ctx: Ctx, name: string) {
  ctx.scopes[ctx.scopes.length - 1].add(name);
}

function useName(ctx: Ctx, name: string, pos: Pos): string {
  if (isDeclared(ctx, name)) return cname(name);
  if (Object.hasOwn(BUILTINS, name)) throw compileError(pos, 'functions are not values');
  throw compileError(pos, `unknown variable ${name}`);
}

function resolveExpr(ctx: Ctx, e: Expr): Expr {
  switch (e.kind) {
    case 'int':
    case 'bool':
    case 'nil':
      return e;
    case 'name':
      return { ...e, cname: useName(ctx, e.name, e.pos) };
    case 'unary':
      return { ...e, operand: resolveExpr(ctx, e.operand) };
    case 'binary':
    case 'logic':
      return { ...e, left: resolveExpr(ctx, e.left), right: resolveExpr(ctx, e.right) };
    case 'call': {
      if (!Object.hasOwn(BUILTINS, e.name)) throw compileError(e.pos, `unknown function ${e.name}`);
      return { ...e, target: 'builtin', args: e.args.map((a) => resolveExpr(ctx, a)) };
    }
  }
}

function resolveBlock(ctx: Ctx, body: Stmt[], first?: string): Stmt[] {
  ctx.scopes.push(new Set(first === undefined ? [] : [first]));
  try {
    return body.map((s) => resolveStmt(ctx, s));
  } finally {
    ctx.scopes.pop();
  }
}

function resolveTarget(ctx: Ctx, t: Target): Target {
  // The index expressions of a path's steps are resolved here (step 5).
  return { ...t, cname: useName(ctx, t.name, t.pos), steps: t.steps };
}

function resolveIter(ctx: Ctx, it: Iter): Iter {
  if (it.kind === 'range') return { ...it, lo: resolveExpr(ctx, it.lo), hi: resolveExpr(ctx, it.hi) };
  return { ...it, expr: resolveExpr(ctx, it.expr) };
}

function resolveStmt(ctx: Ctx, s: Stmt): Stmt {
  switch (s.kind) {
    case 'exprStmt':
      // D21: catches `x == 1` written for `x = 1`.
      if (s.expr.kind !== 'call') throw compileError(s.pos, 'expression statement must be a call');
      return { ...s, expr: resolveExpr(ctx, s.expr) };
    case 'let': {
      // The name is checked first (it is leftmost), the value before the name
      // is in scope: `let x = x + 1` is an unknown variable.
      checkNew(ctx, s.name, s.namePos);
      const value = resolveExpr(ctx, s.value);
      declare(ctx, s.name);
      return { ...s, value, cname: cname(s.name) };
    }
    case 'assign': {
      const target = resolveTarget(ctx, s.target);
      return { ...s, target, value: resolveExpr(ctx, s.value) };
    }
    case 'if': {
      const cond = resolveExpr(ctx, s.cond);
      const then = resolveBlock(ctx, s.then);
      return { ...s, cond, then, else: s.else === null ? null : resolveBlock(ctx, s.else) };
    }
    case 'while': {
      const cond = resolveExpr(ctx, s.cond);
      ctx.loops++;
      try {
        return { ...s, cond, body: resolveBlock(ctx, s.body) };
      } finally {
        ctx.loops--;
      }
    }
    case 'for': {
      // The bounds can't see the loop variable; the body's scope holds it.
      const iter = resolveIter(ctx, s.iter);
      checkNew(ctx, s.name, s.namePos);
      ctx.loops++;
      try {
        return { ...s, iter, cname: cname(s.name), body: resolveBlock(ctx, s.body, s.name) };
      } finally {
        ctx.loops--;
      }
    }
    case 'break':
    case 'continue':
      if (ctx.loops === 0) throw compileError(s.pos, `${s.kind} outside a loop`);
      return s;
  }
}

export function resolve(program: Program): Program {
  const ctx: Ctx = { scopes: [new Set()], loops: 0 };
  return { ...program, body: program.body.map((s) => resolveStmt(ctx, s)) };
}
