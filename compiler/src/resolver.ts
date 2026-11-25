// Names to their declarations (D29): every `$x` is tied to the `my` it
// means before any code is made, and the three ways that can fail are
// refused here, as perl refuses or warns of each (D56):
//   a variable with no `my` in sight (perl: `Global symbol requires
//   explicit package name`);
//   a second `my` of a name in one scope (perl warns that it masks the
//   first);
//   `my $x = $x` with no outer `$x`, which is the first again: a `my` is
//   seen from the statement after its own (T58).
// A scope is a block, and an `if` with its tests: a `my` in a test is
// seen in the blocks of that `if`, in its later tests, and no further.
import { refuse } from './errors.ts';
import type { Expr, My, Program, Stmt, Var } from './ast.ts';

// A declaration is a number, in the order the `my`s are met; `of` says
// which one each variable in the tree means, and `names` what each is
// called.
export type Resolution = { of: ReadonlyMap<Var | My, number>; names: readonly string[] };

export const resolve = (program: Program): Resolution => {
    const of = new Map<Var | My, number>();
    const names: string[] = [];
    const scopes: Map<string, number>[] = [new Map()];

    // The variables an expression uses, each looked up as it is met; and
    // the ones it declares, which are returned and not yet seen.
    const walk = (e: Expr, declared: My[]): void => {
        switch (e.kind) {
        case 'var': {
            const found = [...scopes].reverse().find(s => s.has(e.name));
            if (found === undefined) return refuse(`$${e.name} is not declared: my $${e.name}`, e.pos);
            of.set(e, found.get(e.name)!);
            return;
        }
        case 'my':
            of.set(e, names.length);
            names.push(e.name);
            declared.push(e);
            return;
        case 'assign':
            // The right side first: it is worked out first, and in `my $x
            // = $x` its `$x` is the outer one.
            walk(e.value, declared);
            return walk(e.target, declared);
        case 'step': return walk(e.target, declared);
        case 'unary': return walk(e.operand, declared);
        case 'binary':
            walk(e.left, declared);
            return walk(e.right, declared);
        case 'ternary':
            walk(e.test, declared);
            walk(e.then, declared);
            return walk(e.else, declared);
        case 'apply': return e.args.forEach(a => walk(a, declared));
        default: return;
        }
    };

    // An expression of a statement, or a test: what it declares is seen
    // once the whole of it has been read.
    const whole = (e: Expr): void => {
        const declared: My[] = [];
        walk(e, declared);
        // In the order they are written: the second of two is the one at
        // fault.
        declared.sort((a, b) => a.pos.line - b.pos.line || a.pos.col - b.pos.col);
        for (const d of declared) {
            const scope = scopes.at(-1)!;
            if (scope.has(d.name)) refuse(`my $${d.name} again in one scope: perl warns that it masks the first`, d.pos);
            scope.set(d.name, of.get(d)!);
        }
    };

    const inner = (body: readonly Stmt[]): void => {
        scopes.push(new Map());
        body.forEach(statement);
        scopes.pop();
    };

    const statement = (s: Stmt): void => {
        switch (s.kind) {
        case 'call': return s.args.forEach(whole);
        case 'do': return whole(s.expr);
        case 'block': return inner(s.body);
        case 'if':
            // A modifier's statement is in the scope it stands in, and is
            // written before its test; an `if` with blocks is a scope of
            // its own, for its tests.
            if (s.modifier) {
                s.arms[0]!.body.forEach(statement);
                return whole(s.arms[0]!.test);
            }
            scopes.push(new Map());
            for (const arm of s.arms) {
                whole(arm.test);
                inner(arm.body);
            }
            if (s.otherwise) inner(s.otherwise);
            scopes.pop();
            return;
        default: return;
        }
    };

    program.body.forEach(statement);
    return { of, names };
};
