// Names and arity. Step 0 knows one builtin; steps 2 and 3 add scopes and
// user functions. Returns a new program: the input is not changed.
import { compileError } from './errors.ts';
import type { Expr, Program, Stmt } from './parser.ts';

// arity: the exact number of arguments, or null for any number.
export const BUILTINS: Record<string, { arity: number | null }> = {
  print: { arity: null },
};

function resolveExpr(e: Expr): Expr {
  switch (e.kind) {
    case 'int':
    case 'bool':
    case 'nil':
      return e;
    case 'unary':
      return { ...e, operand: resolveExpr(e.operand) };
    case 'binary':
    case 'logic':
      return { ...e, left: resolveExpr(e.left), right: resolveExpr(e.right) };
    case 'call': {
      if (!Object.hasOwn(BUILTINS, e.name)) throw compileError(e.pos, `unknown function ${e.name}`);
      return { ...e, target: 'builtin', args: e.args.map(resolveExpr) };
    }
  }
}

function resolveStmt(s: Stmt): Stmt {
  switch (s.kind) {
    case 'exprStmt':
      // D21: catches `x == 1` written for `x = 1`.
      if (s.expr.kind !== 'call') throw compileError(s.pos, 'expression statement must be a call');
      return { ...s, expr: resolveExpr(s.expr) };
  }
}

export function resolve(program: Program): Program {
  return { ...program, body: program.body.map(resolveStmt) };
}
