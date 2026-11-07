// AST to C11. Every subexpression is computed into a fresh temporary, in
// source order, so C's unspecified argument order never shows (D30). Names:
// `t1, t2, ...` temporaries; `v_x` the variable x (a Ditto block is a C block,
// and there is no shadowing, so the names never clash); `lo3`, `hi3`, `k3`,
// `more3`, `n3` the counters of the loop whose number is 3; `f_f` the Ditto
// function f, with its parameters as C parameters named like variables. `break` and `continue` are C's, since every Ditto loop
// is one C loop.
import type { Expr, Iter, Program, Stmt, Target } from './parser.ts';

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
      case 'name': {
        const t = `t${++temps}`;
        emit(depth, `Value ${t} = ${e.cname};`);
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
        if (e.target === 'fn') {
          // The depth is counted from the call being made, after its arguments.
          emit(depth, `dt_enter(${line}, ${col});`);
          emit(depth, `Value ${t} = f_${e.name}(${args.join(', ')});`);
          emit(depth, 'dt_leave();');
          return t;
        }
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

  const COMPOUND: Record<string, string> = { '+=': '+', '-=': '-', '*=': '*', '/=': '/', '%=': '%' };

  // An assignment evaluates, in order: the target's index expressions, the
  // current value at the path (compound only), the right-hand side, the
  // operator, then stores. A target is a variable and its steps (steps 5 and
  // 6 add `[i]` and `.f`: index temporaries here, a rebuilt spine in
  // `store`); until then a target is a variable.
  function evalSteps(t: Target, depth: number): string[] {
    return t.steps.map(() => { throw new Error(`internal: path steps arrive in step 5 (${depth})`); });
  }

  function load(t: Target, _steps: string[], depth: number): string {
    const r = `t${++temps}`;
    emit(depth, `Value ${r} = ${t.cname};`);
    return r;
  }

  function store(t: Target, _steps: string[], value: string, depth: number) {
    emit(depth, `${t.cname} = ${value};`);
  }

  // The statements of a Ditto block, in the C block the caller opened.
  function block(body: Stmt[], depth: number) {
    for (const s of body) statement(s, depth);
  }

  // Evaluates a condition and faults unless it is a bool; returns its temporary.
  function condition(e: Expr, pos: { line: number; col: number }, depth: number): string {
    const t = expr(e, depth);
    emit(depth, `dt_need_cond(${pos.line}, ${pos.col}, ${t});`);
    return t;
  }

  function loop(iter: Iter, name: string, body: Stmt[], depth: number) {
    const n = ++temps;
    emit(depth, '{');
    if (iter.kind === 'range') {
      // Both bounds are evaluated, then checked, lo first. The loop runs on
      // an inclusive int64 range, advanced by `k += more` after testing
      // `k < hi`, so a range ending at the largest int never overflows.
      const lo = expr(iter.lo, depth + 1);
      const hi = expr(iter.hi, depth + 1);
      emit(depth + 1, `dt_need_range_bound(${iter.loPos.line}, ${iter.loPos.col}, ${lo});`);
      emit(depth + 1, `dt_need_range_bound(${iter.hiPos.line}, ${iter.hiPos.col}, ${hi});`);
      emit(depth + 1, `int64_t lo${n} = ${lo}.i, hi${n} = ${hi}.i;`);
      if (iter.inclusive) {
        emit(depth + 1, `bool more${n} = lo${n} <= hi${n};`);
      } else {
        emit(depth + 1, `bool more${n} = lo${n} < hi${n};`);
        emit(depth + 1, `if (more${n}) hi${n}--;`);
      }
      emit(depth + 1, `for (int64_t k${n} = lo${n}; more${n}; more${n} = k${n} < hi${n}, k${n} += more${n}) {`);
      emit(depth + 2, `Value ${name} = dt_int(k${n});`);
    } else {
      // The value is evaluated once and walked by index, so changing the
      // variable it came from can't change the loop (D19).
      const coll = expr(iter.expr, depth + 1);
      emit(depth + 1, `int64_t n${n} = dt_iter_len(${iter.exprPos.line}, ${iter.exprPos.col}, ${coll});`);
      emit(depth + 1, `for (int64_t k${n} = 0; k${n} < n${n}; k${n}++) {`);
      emit(depth + 2, `Value ${name} = dt_iter_item(${coll}, k${n});`);
    }
    emit(depth + 2, `(void)${name};`);
    block(body, depth + 2);
    emit(depth + 1, '}');
    emit(depth, '}');
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
      case 'let': {
        // The variable lives in the C block of the Ditto block; the `(void)`
        // keeps -Wunused-but-set-variable quiet for a variable never read.
        const t = expr(s.value, depth);
        emit(depth, `Value ${s.cname} = ${t};`);
        emit(depth, `(void)${s.cname};`);
        return;
      }
      case 'assign': {
        emit(depth, '{');
        const steps = evalSteps(s.target, depth + 1);
        const cur = s.op === '=' ? null : load(s.target, steps, depth + 1);
        const rhs = expr(s.value, depth + 1);
        let value = rhs;
        if (cur !== null) {
          value = `t${++temps}`;
          const { line, col } = s.pos;
          emit(depth + 1, `Value ${value} = ${ARITH[COMPOUND[s.op]]}(${line}, ${col}, ${cur}, ${rhs});`);
        }
        store(s.target, steps, value, depth + 1);
        emit(depth, '}');
        return;
      }
      case 'if': {
        emit(depth, '{');
        const t = condition(s.cond, s.condPos, depth + 1);
        emit(depth + 1, `if (${t}.b) {`);
        block(s.then, depth + 2);
        if (s.else === null) {
          emit(depth + 1, '}');
        } else {
          emit(depth + 1, '} else {');
          block(s.else, depth + 2);
          emit(depth + 1, '}');
        }
        emit(depth, '}');
        return;
      }
      case 'while': {
        emit(depth, 'for (;;) {');
        const t = condition(s.cond, s.condPos, depth + 1);
        emit(depth + 1, `if (!${t}.b) break;`);
        block(s.body, depth + 1);
        emit(depth, '}');
        return;
      }
      case 'for':
        loop(s.iter, s.cname!, s.body, depth);
        return;
      case 'return': {
        if (s.value === null) {
          emit(depth, 'return dt_nil();');
        } else {
          emit(depth, '{');
          const t = expr(s.value, depth + 1);
          emit(depth + 1, `return ${t};`);
          emit(depth, '}');
        }
        return;
      }
      case 'fn':
        throw new Error('internal: a function is not a statement of main');
      case 'break':
        emit(depth, 'break;');
        return;
      case 'continue':
        emit(depth, 'continue;');
        return;
    }
  }

  // Functions are prototyped first, so each can call any other (hoisting). They
  // have external linkage: a static one that is never called would be a
  // -Wunused-function warning, and D37 makes warnings errors.
  const fns = program.body.filter((s): s is Extract<Stmt, { kind: 'fn' }> => s.kind === 'fn');
  const signature = (f: (typeof fns)[number]) =>
    `Value f_${f.name}(${f.params.length === 0 ? 'void' : f.params.map((p) => `Value ${p.cname}`).join(', ')})`;

  emit(0, '#include "ditto.h"');
  emit(0, '');
  // A Ditto function that always calls itself is a program that ends in a
  // stack overflow fault (D28), not a mistake the C compiler should report.
  if (fns.length > 0) emit(0, '#pragma GCC diagnostic ignored "-Winfinite-recursion"');
  for (const f of fns) emit(0, `${signature(f)};`);
  if (fns.length > 0) emit(0, '');
  for (const f of fns) {
    emit(0, `${signature(f)} {`);
    for (const p of f.params) emit(1, `(void)${p.cname};`);
    block(f.body, 1);
    emit(1, 'return dt_nil();');
    emit(0, '}');
    emit(0, '');
  }
  emit(0, 'int main(void) {');
  emit(1, `dt_path = ${cString(path)};`);
  block(program.body.filter((s) => s.kind !== 'fn'), 1);
  emit(1, 'return 0;');
  emit(0, '}');
  return lines.join('\n') + '\n';
}
