import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { parse } from '../src/parser.ts';
import { resolve } from '../src/resolver.ts';
import { CompileError } from '../src/errors.ts';
import type { Expr, Stmt } from '../src/ast.ts';

const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => resolve(parse(lex(src))), (e: unknown) => {
        assert.ok(e instanceof CompileError, String(e));
        assert.deepEqual([e.message, e.line, e.col], [message, line, col]);
        return true;
    });

// Every variable of a program in the order it is written, with the number
// of the declaration it means: `x0` is the first `my`, a `my` has a star.
const uses = (src: string): string => {
    const program = parse(lex(src));
    const names = resolve(program);
    const out: [number, number, string][] = [];
    const expr = (e: Expr): void => {
        if (e.kind === 'var' || e.kind === 'my') out.push([e.pos.line, e.pos.col, `${e.name}${names.of.get(e)}${e.kind === 'my' ? '*' : ''}`]);
        else if (e.kind === 'assign') [e.target, e.value].forEach(expr);
        else if (e.kind === 'step') expr(e.target);
        else if (e.kind === 'unary') expr(e.operand);
        else if (e.kind === 'binary') [e.left, e.right].forEach(expr);
        else if (e.kind === 'ternary') [e.test, e.then, e.else].forEach(expr);
        else if (e.kind === 'apply') e.args.forEach(expr);
    };
    const stmt = (s: Stmt): void => {
        if (s.kind === 'call') s.args.forEach(expr);
        else if (s.kind === 'do') expr(s.expr);
        else if (s.kind === 'block') s.body.forEach(stmt);
        else if (s.kind === 'if') {
            s.arms.forEach(a => { expr(a.test); a.body.forEach(stmt); });
            s.otherwise?.forEach(stmt);
        }
    };
    program.body.forEach(stmt);
    return out.sort((a, b) => a[0] - b[0] || a[1] - b[1]).map(o => o[2]).join(' ');
};

// What perl makes of each is in t/562-scopes.pl, which perl checks.
test('a variable means the nearest my before it', () => {
    assert.equal(uses('my $x = 1; say $x; $x++; $x = $x + 1;'), 'x0* x0 x0 x0 x0');
    assert.equal(uses('my $x; my $y = $x; say $y . $x;'), 'x0* y1* x0 y1 x0');
    assert.deepEqual(resolve(parse(lex('my $x; my $y; { my $x; }'))).names, ['x', 'y', 'x']);
});

test('a block is a scope: a my in it hides an outer one, and ends with it', () => {
    assert.equal(uses('my $x; { my $x; $x++; } $x++;'), 'x0* x1* x1 x0');
    assert.equal(uses('my $x; { $x++; my $x; $x++; { my $x; $x++; } $x++; }'), 'x0* x0 x1* x1 x2* x2 x1');
    assert.equal(uses('{ my $x; } { my $x; }'), 'x0* x1*');
    refused('{ my $x; } say $x;', '$x is not declared: my $x', 1, 16);
});

test('a my is seen from the statement after its own (T58)', () => {
    assert.equal(uses('my $x = 1; { my $x = $x + 1; say $x; }'), 'x0* x1* x0 x1');
    assert.equal(uses('my $y; my $x = $y = 2;'), 'y0* x1* y0');
    refused('my $x = $x;', '$x is not declared: my $x', 1, 9);
    refused('my $x = 1 + (my $y = 2) + $y;', '$y is not declared: my $y', 1, 27);
    refused('say $x; my $x;', '$x is not declared: my $x', 1, 5);
});

test('a second my of a name in one scope', () => {
    const message = (name: string) => `my $${name} again in one scope: perl warns that it masks the first`;
    refused('my $x; my $x;', message('x'), 1, 8);
    refused('my $x;\n{ my $y; }\nmy $x = 2;', message('x'), 3, 1);
    refused('{ my $y; say 1; my $y; }', message('y'), 1, 17);
    refused('my $x = my $x = 1;', message('x'), 1, 9);
});

test('an if is a scope for its tests, and each of its blocks one inside it', () => {
    assert.equal(uses('if (my $x = 1) { say $x; } elsif ($x) { say $x; } else { $x++; }'), 'x0* x0 x0 x0 x0');
    assert.equal(uses('my $x; if (my $x = 1) { my $x; $x++; } $x++;'), 'x0* x1* x2* x2 x0');
    assert.equal(uses('if (1) { my $x; } elsif (my $x = 2) { say $x; } else { my $x; }'), 'x0* x1* x1 x2*');
    assert.equal(uses('my $x; if ((my $y = $x) == 1) { } elsif (my $z = $y) { $z = $y; }'), 'x0* y1* x0 z2* y1 z2 y1');
    refused('if (my $x = 1) { } say $x;', '$x is not declared: my $x', 1, 24);
    refused('if (1) { my $x; } else { say $x; }', '$x is not declared: my $x', 1, 30);
    refused('if (my $x = 1) { } elsif (my $x = 2) { }', 'my $x again in one scope: perl warns that it masks the first', 1, 27);
    refused('unless (my $x = 1) { say $x; } $x++;', '$x is not declared: my $x', 1, 32);
});

test("a modifier's statement and test are in the scope they stand in", () => {
    assert.equal(uses('my $x; $x++ if $x; say $x unless $x;'), 'x0* x0 x0 x0 x0');
    refused('say $y if my $y = 1;', '$y is not declared: my $y', 1, 5);
});
