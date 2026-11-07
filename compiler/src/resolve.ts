// Names, scopes, functions and arity, and the placement of `break`,
// `continue` and `return` (D12, D13). Returns a new program: the input is not
// changed.
import { compileError } from './errors.ts';
import type { Pos } from './errors.ts';
import type { Expr, Iter, Program, Stmt, Target } from './parser.ts';

type FnStmt = Extract<Stmt, { kind: 'fn' }>;

// arity: the exact number of arguments, or null for any number.
export const BUILTINS: Record<string, { arity: number | null }> = {
  print: { arity: null },
  str: { arity: 1 },
  len: { arity: 1 },
  int: { arity: 1 },
  lower: { arity: 1 },
  upper: { arity: 1 },
  slice: { arity: 3 },
  read: { arity: 0 },
  fail: { arity: 1 },
  sort: { arity: 1 },
  split: { arity: 2 },
  join: { arity: 2 },
  words: { arity: 1 },
};

// A function body (and the top level) has a stack of block scopes and a count
// of the loops around the statement being resolved; each function has its own,
// so it sees nothing of the top level (D13). `fns` holds the first definition
// of each user function, found before anything is resolved so that a call can
// come above its function; `topVars` every name the top level's code declares,
// which only serves to say a better error inside a function.
type Ctx = {
  scopes: Set<string>[];
  loops: number;
  inFn: boolean;
  fns: Map<string, FnStmt>;
  topVars: Set<string>;
};

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
  if (ctx.inFn && ctx.topVars.has(name)) {
    throw compileError(
      pos,
      `${name} is a top-level variable; functions see only their parameters and their own variables`,
    );
  }
  if (Object.hasOwn(BUILTINS, name) || ctx.fns.has(name)) {
    throw compileError(pos, 'functions are not values');
  }
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
    case 'string':
      return { ...e, parts: e.parts.map((p) => (p.kind === 'text' ? p : { ...p, expr: resolveExpr(ctx, p.expr) })) };
    case 'index':
      return { ...e, target: resolveExpr(ctx, e.target), index: resolveExpr(ctx, e.index) };
    case 'list':
      return { ...e, items: e.items.map((x) => resolveExpr(ctx, x)) };
    case 'unary':
      return { ...e, operand: resolveExpr(ctx, e.operand) };
    case 'binary':
    case 'logic':
      return { ...e, left: resolveExpr(ctx, e.left), right: resolveExpr(ctx, e.right) };
    case 'call': {
      // The name and its arity come before the arguments: leftmost first.
      const isBuiltin = Object.hasOwn(BUILTINS, e.name);
      const fn = ctx.fns.get(e.name);
      if (!isBuiltin && fn === undefined) throw compileError(e.pos, `unknown function ${e.name}`);
      const arity = isBuiltin ? BUILTINS[e.name].arity : fn!.params.length;
      if (arity !== null && e.args.length !== arity) {
        throw compileError(
          e.pos,
          `${e.name} takes ${arity} argument${arity === 1 ? '' : 's'}, got ${e.args.length}`,
        );
      }
      return { ...e, target: isBuiltin ? 'builtin' : 'fn', args: e.args.map((a) => resolveExpr(ctx, a)) };
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
  // The variable first, then each step's index, left to right.
  const cn = useName(ctx, t.name, t.pos);
  const steps = t.steps.map((st) => (st.kind === 'index' ? { ...st, index: resolveExpr(ctx, st.index) } : st));
  return { ...t, cname: cn, steps };
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
    case 'return':
      if (!ctx.inFn) throw compileError(s.pos, 'return outside a function');
      return { ...s, value: s.value === null ? null : resolveExpr(ctx, s.value) };
    case 'fn':
      return resolveFn(ctx, s);
  }
}

// The parser only lets `fn` through at the top level, so `ctx` is the top
// level's. The function gets a context of its own.
function resolveFn(top: Ctx, s: FnStmt): Stmt {
  if (Object.hasOwn(BUILTINS, s.name)) throw compileError(s.namePos, `${s.name} is a builtin`);
  if (top.fns.get(s.name) !== s) throw compileError(s.namePos, `duplicate function ${s.name}`);
  const ctx: Ctx = { ...top, scopes: [new Set()], loops: 0, inFn: true };
  const params = s.params.map((p) => {
    checkNew(ctx, p.name, p.pos);
    declare(ctx, p.name);
    return { ...p, cname: cname(p.name) };
  });
  return { ...s, params, body: resolveBlock(ctx, s.body) };
}

// Every name declared by a `let` or a `for` in the top level's own code, at
// any depth of blocks, before or after a function that uses it.
function collectVars(body: Stmt[], out: Set<string>) {
  for (const s of body) {
    if (s.kind === 'let') out.add(s.name);
    if (s.kind === 'for') out.add(s.name);
    if (s.kind === 'if') { collectVars(s.then, out); if (s.else !== null) collectVars(s.else, out); }
    if (s.kind === 'while' || s.kind === 'for') collectVars(s.body, out);
  }
}

export function resolve(program: Program): Program {
  const fns = new Map<string, FnStmt>();
  for (const s of program.body) {
    if (s.kind === 'fn' && !Object.hasOwn(BUILTINS, s.name) && !fns.has(s.name)) fns.set(s.name, s);
  }
  const topVars = new Set<string>();
  collectVars(program.body, topVars);
  const ctx: Ctx = { scopes: [new Set()], loops: 0, inFn: false, fns, topVars };
  return { ...program, body: program.body.map((s) => resolveStmt(ctx, s)) };
}
