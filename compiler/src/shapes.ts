// What an expression is by how it is written, where more than one pass
// has to agree on it (D18): whether a `return`'s value is list-shaped, and
// which subs give a list back.
import { infixOp, prefixOp } from './names.ts';
import type { Expr, Invoke, Stmt, Sub } from './ast.ts';

// An expression behind any unary plus, which hands on where it stands.
export const behind = (e: Expr): Expr => (e.kind === 'unary' && prefixOp(e.op)?.rt === undefined ? behind(e.operand) : e);

const isRange = (e: Expr): boolean => e.kind === 'binary' && infixOp(e.op)?.range === true;
const isRepeat = (e: Expr): boolean => e.kind === 'binary' && infixOp(e.op)?.list === true && (e.left.kind === 'list' || e.left.bracketed === true);

// Whether a call is of a sub that gives a list back.
export type Gives = (call: Invoke) => boolean;

// A call whose values a place hands on as they come: the call itself,
// through a unary plus, a branch of `? :`, or the right of `|| && //`.
export const handsOn = (in_: Expr, gives: Gives): boolean => {
    const e = behind(in_);
    return (e.kind === 'invoke' && gives(e))
        || (e.kind === 'ternary' && (handsOn(e.then, gives) || handsOn(e.else, gives)))
        || (e.kind === 'binary' && infixOp(e.op)?.when !== undefined && handsOn(e.right, gives));
};

// List-shaped (D18): what gives a call for one value something other
// than its one value, in perl (T183). An array, a list of two or more, or
// of one that is itself list-shaped, a range, a slice, `(LIST) x N`,
// `splice`, `reverse`, `map`, `grep`, `sort`, and `? :` or `|| && //` with such an arm, whichever
// arm is taken; a hash, and `keys` and `values` (T229). `(LIST)[N]` with one index that is one value is that
// element; `()` is nothing, as `return;` is.
export const shaped = (in_: Expr, gives: Gives): boolean => {
    const e = behind(in_);
    switch (e.kind) {
    case 'array': return true;
    case 'list': return e.items.length > 1 || (e.items.length === 1 && shaped(e.items[0]!, gives));
    case 'slice': return e.name !== undefined || e.indexes.length !== 1 || shaped(e.indexes[0]!, gives) || handsOn(e.indexes[0]!, gives);
    case 'arrayop': return e.op === 'splice';
    case 'listop': return e.op === 'reverse';
    case 'hashop': return e.op === 'keys' || e.op === 'values' || e.keys !== undefined;
    case 'binder': return true;
    case 'sort': return true;
    case 'ternary': return shaped(e.then, gives) || shaped(e.else, gives);
    case 'binary': return isRange(e) || isRepeat(e) || (infixOp(e.op)?.when !== undefined && shaped(e.right, gives));
    default: return false;
    }
};

// What a sub may give back: the value of each `return` in it, and its last
// statement if that is an expression.
const returned = (s: Sub): Expr[] => {
    const found: Expr[] = [];
    const walk = (t: Stmt): void => {
        switch (t.kind) {
        case 'return':
            if (t.value) found.push(t.value);
            return;
        case 'block': case 'while': case 'for': case 'foreach': return t.body.forEach(walk);
        case 'if':
            t.arms.forEach(arm => arm.body.forEach(walk));
            return t.otherwise?.forEach(walk);
        default: return;
        }
    };
    s.body.forEach(walk);
    const last = s.body.at(-1);
    if (last?.kind === 'do') found.push(last.expr);
    return found;
};

// Which subs give a list back, by number, the file being 0: one with a
// list-shaped `return` or last statement, or one that hands on the values
// of a call of such a sub; and so on until nothing is added.
export const listSubs = (subs: readonly Sub[], calls: ReadonlyMap<Invoke, number>): boolean[] => {
    const lists = [false, ...subs.map(() => false)];
    const gives: Gives = call => lists[calls.get(call)!] === true;
    for (let grew = true; grew;) {
        grew = false;
        for (const [n, s] of subs.entries()) {
            if (!lists[n + 1] && returned(s).some(e => shaped(e, gives) || handsOn(e, gives))) {
                lists[n + 1] = true;
                grew = true;
            }
        }
    }
    return lists;
};
