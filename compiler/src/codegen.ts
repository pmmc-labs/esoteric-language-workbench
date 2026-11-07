// AST to C11. Every subexpression is computed into a fresh temporary, in
// source order, so C's unspecified argument order never shows (D30). Names:
// `t1, t2, ...` temporaries; `v_` variables and `f_` functions arrive with
// steps 2 and 3.
import type { Expr, Program, Stmt } from './parser.ts';

const cString = (s: string) =>
  '"' + s.replace(/[\\"?]/g, (c) => '\\' + c).replace(/[^\x20-\x7e]/g, (c) =>
    '\\' + c.charCodeAt(0).toString(8).padStart(3, '0')) + '"';

const ARITH: Record<string, string> = {
  '+': 'dt_add', '-': 'dt_sub', '*': 'dt_mul', '/': 'dt_div', '%': 'dt_mod',
  '<': 'dt_lt', '<=': 'dt_le', '>': 'dt_gt', '>=': 'dt_ge',
};

export function codegen(program: Program, path: string): string {
  let temps = 0;
  const lines: string[] = [];
  const emit = (depth: number, s: string) => lines.push('  '.repeat(depth) + s);

  // Emits the code for `e` and returns the name of the temporary holding it.
  function expr(e: Expr, depth: number): string {
    switch (e.kind) {
      case 'int': {
        const t = `t${++temps}`;
        emit(depth, `Value ${t} = dt_int(INT64_C(${e.value}));`);
        return t;
      }
      case 'bool': {
        const t = `t${++temps}`;
        emit(depth, `Value ${t} = dt_bool(${e.value});`);
        return t;
      }
      case 'nil': {
        const t = `t${++temps}`;
        emit(depth, `Value ${t} = dt_nil();`);
        return t;
      }
      case 'unary': {
        const a = expr(e.operand, depth);
        const t = `t${++temps}`;
        const fn = e.op === '-' ? 'dt_neg' : 'dt_not';
        emit(depth, `Value ${t} = ${fn}(${e.pos.line}, ${e.pos.col}, ${a});`);
        return t;
      }
      case 'binary': {
        const l = expr(e.left, depth);
        const r = expr(e.right, depth);
        const t = `t${++temps}`;
        const { line, col } = e.pos;
        // == and != never fault, so they take no position.
        if (e.op === '==') emit(depth, `Value ${t} = dt_bool(dt_equal(${l}, ${r}));`);
        else if (e.op === '!=') emit(depth, `Value ${t} = dt_bool(!dt_equal(${l}, ${r}));`);
        else emit(depth, `Value ${t} = ${ARITH[e.op]}(${line}, ${col}, ${l}, ${r});`);
        return t;
      }
      case 'logic': {
        // The result starts as the left operand and is replaced by the right
        // one only when the left doesn't decide (D30: `if`, not `&&`).
        const { line, col } = e.pos;
        const l = expr(e.left, depth);
        const t = `t${++temps}`;
        emit(depth, `dt_need_bool(${line}, ${col}, "${e.op}", ${l});`);
        emit(depth, `Value ${t} = ${l};`);
        emit(depth, `if (${e.op === 'and' ? '' : '!'}${t}.b) {`);
        const r = expr(e.right, depth + 1);
        emit(depth + 1, `dt_need_bool(${line}, ${col}, "${e.op}", ${r});`);
        emit(depth + 1, `${t} = ${r};`);
        emit(depth, '}');
        return t;
      }
      case 'call': {
        const args = e.args.map((a) => expr(a, depth));
        const t = `t${++temps}`;
        const { line, col } = e.pos;
        let argv = 'NULL';
        if (args.length > 0) {
          argv = `a${temps}`;
          emit(depth, `Value ${argv}[] = {${args.join(', ')}};`);
        }
        emit(depth, `Value ${t} = dt_b_${e.name}(${line}, ${col}, ${args.length}, ${argv});`);
        return t;
      }
    }
  }

  function statement(s: Stmt, depth: number) {
    switch (s.kind) {
      case 'exprStmt': {
        emit(depth, '{');
        const t = expr(s.expr, depth + 1);
        emit(depth + 1, `(void)${t};`);
        emit(depth, '}');
        return;
      }
    }
  }

  emit(0, '#include "ditto.h"');
  emit(0, '');
  emit(0, 'int main(void) {');
  emit(1, `dt_path = ${cString(path)};`);
  for (const s of program.body) statement(s, 1);
  emit(1, 'return 0;');
  emit(0, '}');
  return lines.join('\n') + '\n';
}
