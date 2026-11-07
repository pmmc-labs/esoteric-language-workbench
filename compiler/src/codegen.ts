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

  // A string literal is built once, the first time control reaches it.
  function literal(value: string, depth: number): string {
    const t = `t${++temps}`;
    emit(depth, `static Value s${temps};`);
    emit(depth, `if (s${temps}.tag != T_STR) s${temps} = dt_str_new(${cString(value)}, ${value.length});`);
    emit(depth, `Value ${t} = s${temps};`);
    return t;
  }

  // The `miss` labels of the `else`s whose left operand is being compiled,
  // innermost last. A lookup written there branches to the innermost one when
  // it finds nothing (D20): which misses are caught is where the code is
  // written, so a called function's body, compiled apart, has no label.
  const catchers: string[] = [];
  // Labels some lookup jumps to: an unused label is a -Wunused-label error (D37),
  // which happens when an inner `else` catches every lookup of a left operand.
  const usedLabels = new Set<string>();

  // `Value t = dt_try_X(...)`: with a catcher, a miss is a `goto`; without, the
  // faulting form.
  function lookupCall(depth: number, t: string, tryFn: string, faultFn: string, args: string) {
    if (catchers.length === 0) {
      emit(depth, `Value ${t} = ${faultFn}(${args});`);
    } else {
      emit(depth, `Value ${t} = dt_nil();`);
      const label = catchers[catchers.length - 1];
      usedLabels.add(label);
      emit(depth, `if (!${tryFn}(${args}, &${t})) goto ${label};`);
    }
  }

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
        if (e.op === 'in' || e.op === 'not in') {
          emit(depth, `Value ${t} = dt_bool(${e.op === 'in' ? '' : '!'}dt_in(${line}, ${col}, ${l}, ${r}));`);
        } else if (e.op === '==') emit(depth, `Value ${t} = dt_bool(dt_equal(${l}, ${r}));`);
        else if (e.op === '!=') emit(depth, `Value ${t} = dt_bool(!dt_equal(${l}, ${r}));`);
        else emit(depth, `Value ${t} = ${ARITH[e.op]}(${line}, ${col}, ${l}, ${r});`);
        return t;
      }
      case 'name': {
        const t = `t${++temps}`;
        emit(depth, `Value ${t} = ${e.cname};`);
        return t;
      }
      case 'string': {
        // Text is a literal built the first time it is reached; every part is
        // computed in order, then joined.
        const vals = e.parts.map((p) => (p.kind === 'text' ? literal(p.value, depth) : expr(p.expr, depth)));
        if (e.parts.length === 0) return literal('', depth);
        if (e.parts.length === 1 && e.parts[0].kind === 'text') return vals[0];
        const t = `t${++temps}`;
        emit(depth, `Value a${temps}[] = {${vals.join(', ')}};`);
        emit(depth, `Value ${t} = dt_interp(${vals.length}, a${temps});`);
        return t;
      }
      case 'list': {
        // Every item is computed in order, then the list is built once.
        const vals = e.items.map((x) => expr(x, depth));
        const t = `t${++temps}`;
        if (vals.length === 0) {
          emit(depth, `Value ${t} = dt_list_new(0, NULL);`);
        } else {
          emit(depth, `Value a${temps}[] = {${vals.join(', ')}};`);
          emit(depth, `Value ${t} = dt_list_new(${vals.length}, a${temps});`);
        }
        return t;
      }
      case 'index': {
        const c = expr(e.target, depth);
        const i = expr(e.index, depth);
        const t = `t${++temps}`;
        // dt_index is dt_try_index plus the fault for a miss; inside an `else`'s
        // left operand the try form is called and a miss branches.
        lookupCall(depth, t, 'dt_try_index', 'dt_index', `${e.pos.line}, ${e.pos.col}, ${c}, ${i}`);
        return t;
      }
      case 'field': {
        const c = expr(e.target, depth);
        const k = literal(e.name, depth);
        const t = `t${++temps}`;
        // Like an index: dt_field is dt_try_field plus the fault for a miss.
        lookupCall(depth, t, 'dt_try_field', 'dt_field', `${e.pos.line}, ${e.pos.col}, ${c}, ${k}`);
        return t;
      }
      case 'map': {
        // Keys are literals; each key and value is computed in order, then the
        // map is built once from the two arrays.
        const keys: string[] = [];
        const vals: string[] = [];
        for (const en of e.entries) {
          keys.push(expr(en.key, depth));
          vals.push(expr(en.value, depth));
        }
        const t = `t${++temps}`;
        if (keys.length === 0) {
          emit(depth, `Value ${t} = dt_map_new(0, NULL, NULL);`);
        } else {
          emit(depth, `Value a${temps}[] = {${keys.join(', ')}};`);
          emit(depth, `Value b${temps}[] = {${vals.join(', ')}};`);
          emit(depth, `Value ${t} = dt_map_new(${keys.length}, a${temps}, b${temps});`);
        }
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
      case 'else': {
        // The result is the left operand, computed in a block whose lookups
        // `goto miss` when they find nothing; the right operand runs only from
        // there, outside the catcher, so a miss in it belongs to an `else`
        // further out (D30: `if` and `goto`, nothing nested).
        const n = ++temps;
        const t = `t${n}`;
        emit(depth, `Value ${t} = dt_nil();`);
        emit(depth, '{');
        catchers.push(`miss${n}`);
        const l = expr(e.left, depth + 1);
        catchers.pop();
        emit(depth + 1, `${t} = ${l};`);
        emit(depth + 1, `goto done${n};`);
        emit(depth, '}');
        if (usedLabels.has(`miss${n}`)) emit(depth, `miss${n}: ;`);
        emit(depth, '{');
        const r = expr(e.right, depth + 1);
        emit(depth + 1, `${t} = ${r};`);
        emit(depth, '}');
        emit(depth, `done${n}: ;`);
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
        if (e.name === 'int' && catchers.length > 0) {
          // The one builtin that is a lookup: a string that isn't a number is a miss.
          lookupCall(depth, t, 'dt_try_int', '', `${line}, ${col}, ${args[0]}`);
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
  // operator, then stores (LANGUAGE.md, Assignment). A target is a variable
  // and its steps. `evalSteps` computes each step's key into a temporary;
  // `load` looks the whole path up as an expression would; `store` looks up
  // every step but the last, sets the last, and rebuilds the spine from the
  // inside out (D7: nothing is written, each level is a new value). A `.name`
  // step is a key that is a string literal, with its own lookup and set
  // (they fault with their own messages, at the `.`).
  function evalSteps(t: Target, depth: number): string[] {
    return t.steps.map((st) => (st.kind === 'index' ? expr(st.index, depth) : literal(st.name, depth)));
  }

  // The value one step down from `c`, faulting at the step as an expression would.
  function lookup(st: Target['steps'][number], c: string, key: string, depth: number): string {
    const r = `t${++temps}`;
    const fn = st.kind === 'index' ? 'dt_index' : 'dt_field';
    emit(depth, `Value ${r} = ${fn}(${st.pos.line}, ${st.pos.col}, ${c}, ${key});`);
    return r;
  }

  // `c` with the step's key set to `v`: a new value.
  function setStep(st: Target['steps'][number], c: string, key: string, v: string, depth: number): string {
    const r = `t${++temps}`;
    const fn = st.kind === 'index' ? 'dt_set_index' : 'dt_set_field';
    emit(depth, `Value ${r} = ${fn}(${st.pos.line}, ${st.pos.col}, ${c}, ${key}, ${v});`);
    return r;
  }

  function load(t: Target, steps: string[], depth: number): string {
    let r = `t${++temps}`;
    emit(depth, `Value ${r} = ${t.cname};`);
    t.steps.forEach((st, k) => { r = lookup(st, r, steps[k], depth); });
    return r;
  }

  function store(t: Target, steps: string[], value: string, depth: number) {
    if (t.steps.length === 0) {
      emit(depth, `${t.cname} = ${value};`);
      return;
    }
    // containers[k] is the value the k-th step acts on.
    let r = `t${++temps}`;
    emit(depth, `Value ${r} = ${t.cname};`);
    const containers = [r];
    for (let k = 0; k < t.steps.length - 1; k++) {
      r = lookup(t.steps[k], r, steps[k], depth);
      containers.push(r);
    }
    let built = value;
    for (let k = t.steps.length - 1; k >= 0; k--) {
      built = setStep(t.steps[k], containers[k], steps[k], built, depth);
    }
    emit(depth, `${t.cname} = ${built};`);
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
