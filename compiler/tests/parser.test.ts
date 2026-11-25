import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { parse } from '../src/parser.ts';
import { CompileError } from '../src/errors.ts';
import type { Expr, Stmt } from '../src/ast.ts';

const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => parse(lex(src)), (e: unknown) => {
        assert.ok(e instanceof CompileError, String(e));
        assert.deepEqual([e.message, e.line, e.col], [message, line, col]);
        return true;
    });

// An expression's grouping, every operator's operands in brackets, and a
// star where the source had brackets of its own.
const shape = (e: Expr): string => {
    const s = e.kind === 'int' || e.kind === 'num' || e.kind === 'str' ? e.text
        : e.kind === 'unary' ? `(${e.op}${shape(e.operand)})`
        : e.kind === 'apply' ? `${e.name}[${e.args.map(shape).join(', ')}]`
        : e.kind === 'constant' ? e.name
        : e.kind === 'ternary' ? `(${shape(e.test)} ? ${shape(e.then)} : ${shape(e.else)})`
        : e.kind === 'var' ? `$${e.name}`
        : e.kind === 'my' ? `my $${e.name}`
        : e.kind === 'assign' ? `(${shape(e.target)} ${e.op} ${shape(e.value)})`
        : e.kind === 'step' ? (e.before ? `(${e.op}${shape(e.target)})` : `(${shape(e.target)}${e.op})`)
        : e.kind === 'invoke' ? `${e.name}(${e.args.map(shape).join(', ')})`
        : `(${shape(e.left)} ${e.op} ${shape(e.right)})`;
    return e.bracketed ? s + '*' : s;
};
const argument = (src: string): Expr => {
    const stmt = parse(lex(src)).body[0]!;
    assert.equal(stmt.kind, 'call');
    return stmt.kind === 'call' ? stmt.args[0]! : assert.fail();
};
const grouped = (src: string) => shape(argument(src));

test('the tree, with positions', () => {
    assert.deepEqual(parse(lex('use v5.42;\n  say 010;\n')), {
        kind: 'program',
        body: [
            { kind: 'use', version: 'v5.42', pos: { line: 1, col: 1 } },
            { kind: 'call', name: 'say', pos: { line: 2, col: 3 }, args: [
                { kind: 'int', text: '010', value: 10n, pos: { line: 2, col: 7 } },
            ] },
        ],
        end: { line: 3, col: 1 },
    });
    assert.deepEqual(parse(lex(' ')), { kind: 'program', body: [], end: { line: 1, col: 2 } });
});

test('an operator node is at its operator', () => {
    assert.deepEqual(argument('say 1 +\n -2;'), {
        kind: 'binary', op: '+', pos: { line: 1, col: 7 },
        left: { kind: 'int', text: '1', value: 1n, pos: { line: 1, col: 5 } },
        right: { kind: 'unary', op: '-', pos: { line: 2, col: 2 },
            operand: { kind: 'int', text: '2', value: 2n, pos: { line: 2, col: 3 } } },
    });
});

// What perl makes of each is in t/030-precedence.pl, which perl checks.
test("precedence and associativity are perlop's", () => {
    assert.equal(grouped('say 2 - 3 - 4;'), '((2 - 3) - 4)');
    assert.equal(grouped('say 2 + 3 * 4;'), '(2 + (3 * 4))');
    assert.equal(grouped('say 2 * 3 + 4;'), '((2 * 3) + 4)');
    assert.equal(grouped('say 7 % 3 * 2;'), '((7 % 3) * 2)');
    assert.equal(grouped('say 2 * 7 % 3;'), '((2 * 7) % 3)');
    assert.equal(grouped('say 10 - 7 % 3 + 1;'), '((10 - (7 % 3)) + 1)');
    assert.equal(grouped('say -2 * -3;'), '((-2) * (-3))');
    assert.equal(grouped('say - 7 % 3;'), '((-7) % 3)');
    assert.equal(grouped('say - - 5;'), '(-(-5))');
    assert.equal(grouped('say +-+-5;'), '(+(-(+(-5))))');
    assert.equal(grouped('say 1 - - - 2;'), '(1 - (-(-2)))');
});

// What perl makes of each is in t/081-num-precedence.pl, which perl checks.
test('** binds tighter than a sign before it, and groups from the right', () => {
    assert.equal(grouped('say -2 ** 2;'), '(-(2 ** 2))');
    assert.equal(grouped('say 2 ** 3 ** 2;'), '(2 ** (3 ** 2))');
    assert.equal(grouped('say 2 ** -1;'), '(2 ** (-1))');
    assert.equal(grouped('say 2 ** -2 ** 2;'), '(2 ** (-(2 ** 2)))');
    assert.equal(grouped('say - 2 ** - 2;'), '(-(2 ** (-2)))');
    assert.equal(grouped('say 2 * 3 ** 2;'), '(2 * (3 ** 2))');
    assert.equal(grouped('say 2 ** 3 * 2;'), '((2 ** 3) * 2)');
    assert.equal(grouped('say 4 / 2 * 3;'), '((4 / 2) * 3)');
    assert.equal(grouped('say 7 / 2 % 2;'), '((7 / 2) % 2)');
    assert.equal(grouped('say 1 - 2 / 4;'), '(1 - (2 / 4))');
});

test('what a literal is worth', () => {
    const worth = (src: string) => { const e = argument(src); return e.kind === 'int' || e.kind === 'num' ? `${e.kind} ${e.value}` : assert.fail(); };
    assert.equal(worth('say 1_000;'), 'int 1000');
    assert.equal(worth('say 0x1F;'), 'int 31');
    assert.equal(worth('say 0XfF;'), 'int 255');
    assert.equal(worth('say 0b1_01;'), 'int 5');
    assert.equal(worth('say 0O17;'), 'int 15');
    assert.equal(worth('say 9223372036854775808;'), 'int 9223372036854775808');
    assert.equal(worth('say 1.5;'), 'num 1.5');
    assert.equal(worth('say .5_5;'), 'num 0.55');
    assert.equal(worth('say 1e1_0;'), 'num 10000000000');
    assert.equal(worth('say 1.5E-3;'), 'num 0.0015');
    assert.equal(worth('say 1e400;'), 'num Infinity');
    assert.equal(worth('say 0.1;'), 'num 0.1');
});

test('brackets group, and are remembered', () => {
    assert.equal(grouped('say 2 * (3 + 4);'), '(2 * (3 + 4)*)');
    assert.equal(grouped('say -(7 % 3);'), '(-(7 % 3)*)');
    assert.equal(grouped('say +(1 + 2) * 3;'), '((+(1 + 2)*) * 3)');
    assert.equal(grouped('say 1 - ((2));'), '(1 - 2*)');
    assert.equal(grouped('say(1 + 2);'), '(1 + 2)*');
    assert.equal(grouped('say((1 + 2) * 3);'), '((1 + 2)* * 3)*');
    assert.equal(grouped('say (5);'), '5*');
    assert.equal(grouped('say\n(5)\n;'), '5*');
});

test('what a statement may start with', () => {
    refused('use v5.42;\n;', "expected a statement, found ';'", 2, 1);
    refused('v5.42;', 'expected a value, found v5.42', 1, 1);
    refused('use v5.42;\n}', "expected a statement, found '}'", 2, 1);
    refused(')', "expected a statement, found ')'", 1, 1);
    refused('else { say 1; }', 'else without an if before it', 1, 1);
    refused('elsif (1) { say 1; }', 'elsif without an if before it', 1, 1);
    refused('use v5.42;\nprintf 42;', "'printf' is not in the language", 2, 1);
    // A word perl has no meaning for could be a sub's name (D72).
    refused('say42;', "'say42' is not in the language; a call of a sub of the program's has brackets: say42(...)", 1, 1);
    refused('redo;', "'redo' is not in the language", 1, 1);
});

// The statements of a program, in brackets, each block in braces.
const stmt = (s: Stmt): string =>
    s.kind === 'call' ? `${s.name} ${shape(s.args[0]!)};`
    : s.kind === 'do' ? `${shape(s.expr)};`
    : s.kind === 'block' ? `{ ${s.body.map(stmt).join(' ')} }`
    : s.kind === 'while' ? (s.modifier
        ? `[${stmt(s.body[0]!)} ${s.negate ? 'until' : 'while'} ${shape(s.test)}]`
        : `${s.label ? s.label.name + ': ' : ''}${s.negate ? 'until' : 'while'} ${shape(s.test)} { ${s.body.map(stmt).join(' ')} }`)
    : s.kind === 'for' ? `${s.label ? s.label.name + ': ' : ''}for (${s.first.map(shape).join(', ')}; ${s.test ? shape(s.test) : ''}; ${s.each.map(shape).join(', ')}) { ${s.body.map(stmt).join(' ')} }`
    : s.kind === 'jump' ? `${s.name}${s.label ? ' ' + s.label.name : ''};`
    : s.kind === 'if' ? (s.modifier
        ? `[${stmt(s.arms[0]!.body[0]!)} ${s.arms[0]!.negate ? 'unless' : 'if'} ${shape(s.arms[0]!.test)}]`
        : s.arms.map(a => `${a.negate ? 'unless' : 'if'} ${shape(a.test)} { ${a.body.map(stmt).join(' ')} }`).join(' els')
            + (s.otherwise ? ` else { ${s.otherwise.map(stmt).join(' ')} }` : ''))
    : s.kind;
const program = (src: string) => parse(lex(src)).body.map(stmt).join(' ');

// What perl makes of each is in t/560-shapes.pl, which perl checks.
test('a variable, my, and the steps, which bind tightest of all', () => {
    assert.equal(grouped('say $x;'), '$x');
    assert.equal(grouped('say $x++;'), '($x++)');
    assert.equal(grouped('say --$x;'), '(--$x)');
    assert.equal(grouped('say -$x++;'), '(-($x++))');
    assert.equal(grouped('say $x++ ** 2;'), '(($x++) ** 2)');
    assert.equal(grouped('say 2 ** ++$x;'), '(2 ** (++$x))');
    assert.equal(grouped('say $x+++$y;'), '(($x++) + $y)');
    assert.equal(grouped('say $x---$y;'), '(($x--) - $y)');
    assert.equal(grouped('say $x + ++$y;'), '($x + (++$y))');
    assert.equal(grouped('say !$x++;'), '(!($x++))');
    assert.equal(grouped('say length $x++;'), 'length[($x++)]');
    assert.equal(grouped('say ($x)++;'.replace('($x)++', '($x++)')), '($x++)*');
    assert.equal(program('my $x;'), 'my $x;');
    assert.deepEqual(parse(lex('my $x = $y++;')).body[0], {
        kind: 'do', pos: { line: 1, col: 1 },
        expr: { kind: 'assign', op: '=', pos: { line: 1, col: 7 },
            target: { kind: 'my', name: 'x', pos: { line: 1, col: 1 } },
            value: { kind: 'step', op: '++', before: false, pos: { line: 1, col: 11 },
                target: { kind: 'var', name: 'y', pos: { line: 1, col: 9 } } } },
    });
    assert.deepEqual(argument('say --$y;'), {
        kind: 'step', op: '--', before: true, pos: { line: 1, col: 5 },
        target: { kind: 'var', name: 'y', pos: { line: 1, col: 7 } },
    });
});

test('a step is for a variable, and is not stepped again', () => {
    refused('say --5;', "'--' is for a variable: --$x", 1, 5);
    refused('say ++5;', "'++' is for a variable: ++$x", 1, 5);
    refused('say ++($x);', "'++' is for a variable: ++$x", 1, 5);
    refused('say ++ ++$x;', "'++' is for a variable: ++$x", 1, 5);
    refused('say - --$x++;', "expected ';', found '++'", 1, 11);
    refused('say 1--2;', "expected ';', found '--'", 1, 6);
    refused('say ($x)++;', "'++' after say (...): perl takes the brackets for all of say's arguments; bracket the whole expression", 1, 9);
    refused('$y = ($x)++;', "expected ';', found '++'", 1, 10);
    refused('say $x++ ++;', "expected ';', found '++'", 1, 10);
    refused('my 5;', "after 'my', expected a variable, found 5", 1, 4);
    refused('my ($x);', "after 'my', expected a variable, found '('", 1, 4);
});

test('assignment is right to left, below ? : and above the word operators', () => {
    assert.equal(program('$x = $y = 1;'), '($x = ($y = 1));');
    assert.equal(program('$x += $y *= 2;'), '($x += ($y *= 2));');
    assert.equal(program('$x = 1 ? 2 : 3;'), '($x = (1 ? 2 : 3));');
    assert.equal(program('$x = $y || 2;'), '($x = ($y || 2));');
    assert.equal(program('$x = 1 + 2 . 3;'), '($x = ((1 + 2) . 3));');
    assert.equal(program('my $x = my $y = 1;'), '(my $x = (my $y = 1));');
    assert.equal(program('$x x= 2 x 3;'), '($x x= (2 x 3));');
    assert.equal(program('$x ||= $y //= 3;'), '($x ||= ($y //= 3));');
    assert.equal(program('$x = not 1;'), '($x = (not1));');
    assert.equal(grouped('say $x = 5;'), '($x = 5)');
    assert.equal(grouped('say 1 + ($x = 5);'), '(1 + ($x = 5)*)');
    assert.equal(grouped('say not $x = 5;'), '(not($x = 5))');
});

test('the left side of an assignment is a variable, bare', () => {
    const message = (op: string) => `the left side of '${op}' is a variable, $x or my $x, with no brackets round it`;
    refused('say 2 **= 3;', message('**='), 1, 7);
    refused('say 1 = 2;', message('='), 1, 7);
    refused('($x) = 5;', message('='), 1, 6);
    refused('($x = 5) = 7;', message('='), 1, 10);
    refused('$x + 1 = 7;', message('='), 1, 8);
    refused('1 ? $x : $y = 7;', message('='), 1, 13);
    refused('$x++ = 7;', message('='), 1, 6);
    refused('-$x = 7;', message('='), 1, 5);
    refused('"a" x= 3;', message('x='), 1, 5);
    refused('(my $x) = 7;', message('='), 1, 9);
    // A statement is one assignment, not two joined (D56).
    const joins = (op: string) => `'${op}' after a statement joins it to what follows, to perl, which binds '${op}' more loosely than '=': write it as an if`;
    refused('$x = 1 and $y = 2;', joins('and'), 1, 8);
    refused('$x++ or $y = 2;', joins('or'), 1, 6);
    refused('my $x = 1 xor 2;', joins('xor'), 1, 11);
});

test('blocks, if with its elsifs and else, unless, and the modifiers', () => {
    assert.equal(program('{ say 1; { say 2; } }'), '{ say 1; { say 2; } }');
    assert.equal(program('if ($x) { say 1; }'), 'if $x { say 1; }');
    assert.equal(program('if ($x) { say 1; } elsif ($y) { } else { say 3; say 4; }'),
        'if $x { say 1; } elsif $y {  } else { say 3; say 4; }');
    assert.equal(program('if ($x) { } else { }'), 'if $x {  } else {  }');
    assert.equal(program('unless ($x == 1) { say 1; }'), 'unless ($x == 1) { say 1; }');
    assert.equal(program('say 1 if $x;'), '[say 1; if $x]');
    assert.equal(program('$x++ unless $y > 2;'), '[($x++); unless ($y > 2)]');
    assert.equal(program('$x = 1 if $y or $z;'), '[($x = 1); if ($y or $z)]');
    assert.equal(program('if (my $x = $y) { say $x; } say 2;'), 'if (my $x = $y) { say $x; } say 2;');
    // An arm is at its `if` or `elsif`, and a modified statement at its start.
    const chain = parse(lex('if (1) {\n} elsif (2) {\n}\nsay 3\n  unless 4;'));
    const [first, second] = chain.body;
    assert.ok(first?.kind === 'if' && second?.kind === 'if');
    assert.deepEqual(first.arms.map(a => a.pos), [{ line: 1, col: 1 }, { line: 2, col: 3 }]);
    assert.deepEqual([second.pos, second.arms[0]!.pos, second.modifier], [{ line: 4, col: 1 }, { line: 5, col: 3 }, true]);
});

// perl looks along the bracket's own line for what may follow a call, a
// modifier as well as a semicolon (T128).
test('say, one blank, brackets, and a modifier that is not on their line', () => {
    const message = (name: string, word: string) =>
        `${name} (...) after one blank: perl warns unless the brackets close on this line, one in a string counting too, with '${word}' after them: write ${name}(...)`;
    refused('say ("a")\nif $x;', message('say', 'if'), 1, 5);
    refused('say ("a") # why\n  unless $x;', message('say', 'unless'), 1, 5);
    refused('print ("a" .\n"b") if $x;', message('print', 'if'), 1, 7);
    refused('say (")") if $x;', message('say', 'if'), 1, 5);
    assert.equal(program('say ("a") if $x;'), '[say "a"*; if $x]');
    assert.equal(program('say ("a")   unless $x;'), '[say "a"*; unless $x]');
    assert.equal(program('say("a")\nif $x;'), '[say "a"*; if $x]');
    assert.equal(program('say  ("a")\nif $x;'), '[say "a"*; if $x]');
});

test('what a block and an if may not be', () => {
    refused('{ }', 'an empty block is an anonymous hash, to perl: put a statement in it, or take it out', 1, 1);
    refused('{ { } }', 'an empty block is an anonymous hash, to perl: put a statement in it, or take it out', 1, 3);
    refused('{ say 1;', "expected '}', found the end of the file", 1, 9);
    refused('if 1 { say 1; }', "expected '(' after if, found 1", 1, 4);
    refused('if (1) say 1;', "expected '{', found 'say'", 1, 8);
    refused('if (1) { say 1; } else if (2) { }', "expected '{', found 'if'", 1, 24);
    refused('if (1) { } else { } else { }', 'else without an if before it', 1, 21);
    refused('unless (1) { } else { }', 'else after unless: write it as an if', 1, 16);
    refused('unless (1) { } elsif (2) { }', 'elsif after unless: write it as an if', 1, 16);
    refused('say 1 if 2 if 3;', "expected ';', found 'if'", 1, 12);
    refused('say 1 if;', "expected a value, found ';'", 1, 9);
    refused('if (1) { say 1; } if 2;', "expected '(' after if, found 2", 1, 22);
    refused('{ say 1; } if 2;', "expected '(' after if, found 2", 1, 15);
    refused('if () { }', "expected a value, found ')'", 1, 5);
});

// What perl makes of each is in t/740-loop-shapes.pl, which perl checks.
test('while, until and for, with a label or without (D61, D62)', () => {
    assert.equal(program('while ($x) { say 1; }'), 'while $x { say 1; }');
    assert.equal(program('until ($x) { }'), 'until $x {  }');
    assert.equal(program('OUTER: while ($x) { next OUTER; last; }'), 'OUTER: while $x { next OUTER; last; }');
    assert.equal(program('A_1:\n  for (;;) { last A_1 if $x; }'), 'A_1: for (; ; ) { [last A_1; if $x] }');
    assert.equal(program('for (my $i = 0, my $j = 9; $i < $j; $i++, $j--) { say $i; }'),
        'for ((my $i = 0), (my $j = 9); ($i < $j); ($i++), ($j--)) { say $i; }');
    assert.equal(program('for ($i = 0; ; ) { }'), 'for (($i = 0); ; ) {  }');
    assert.equal(program('for (; $i < 3; ) { }'), 'for (; ($i < 3); ) {  }');
    assert.equal(program('for (;; $i++) { }'), 'for (; ; ($i++)) {  }');
    assert.equal(program('for (; $i or $j; ) { }'), 'for (; ($i or $j); ) {  }');
    assert.equal(program('$i++ while $i < 3;'), '[($i++); while ($i < 3)]');
    assert.equal(program('say $i until $i;'), '[say $i; until $i]');
    assert.equal(program('next unless $x;'), '[next; unless $x]');
    assert.equal(program('while ($x) { } while ($y) { }'), 'while $x {  } while $y {  }');
    assert.equal(program('$x = undef while $y;'), '[($x = undef); while $y]');
    assert.equal(program('if ($x) { L: until ($y) { last L; } }'), 'if $x { L: until $y { last L; } }');
    const [w] = parse(lex('  L: until ($x) {\n last L; }')).body;
    assert.ok(w?.kind === 'while');
    assert.deepEqual([w.pos, w.negate, w.label], [{ line: 1, col: 6 }, true, { name: 'L', pos: { line: 1, col: 3 } }]);
    assert.deepEqual(w.body[0], { kind: 'jump', name: 'last', label: { name: 'L', pos: { line: 2, col: 7 } }, pos: { line: 2, col: 2 } });
    // A modified statement is at its start, as under if.
    const [m] = parse(lex('$i++\n  while $i;')).body;
    assert.ok(m?.kind === 'while');
    assert.deepEqual([m.pos, m.modifier], [{ line: 1, col: 1 }, true]);
});

test('what a loop may not be', () => {
    const list = 'for over a list is not in the language yet: this for is for (FIRST; TEST; EACH)';
    refused('while () { }', 'while () is while (1), to perl: say that, or for (;;)', 1, 7);
    refused('until () { }', "expected a value, found ')'", 1, 8);
    refused('for my $i (1, 2) { }', list, 1, 5);
    refused('for (1, 2) { }', list, 1, 5);
    refused('for ($x) { }', list, 1, 5);
    refused('foreach (;;) { }', "'foreach' is not in the language", 1, 1);
    refused('do { } while ($x);', "'do' is not in the language", 1, 1);
    refused('while ($x) say 1;', "expected '{', found 'say'", 1, 12);
    refused('while $x { }', "expected '(' after while, found '$x'", 1, 7);
    refused('while ($x) { } else { }', 'else without an if before it', 1, 16);
    refused('for (;;;) { }', "expected a value, found ';'", 1, 8);
    refused('for ($i = 0 or 1; ; ) { }', "'or' in a part of a for joins the parts on either side of it, to perl: bracket what it joins", 1, 13);
    refused('for (; $i < 3, $j; ) { }', "expected ';', found ','", 1, 14);
    refused('say 1 while $x if $y;', "expected ';', found 'if'", 1, 16);
    refused('say ("a")\nwhile $x;', "say (...) after one blank: perl warns unless the brackets close on this line, one in a string counting too, with 'while' after them: write say(...)", 1, 5);
});

test('a label is on a loop, in capitals, hard against its colon (D61)', () => {
    const on = (name: string) => `a label is on a loop: after ${name}: comes while, until or for`;
    refused('outer: while ($x) { }', 'a label is written in capitals: OUTER:', 1, 1);
    refused('Outer: while ($x) { }', 'a label is written in capitals: OUTER:', 1, 1);
    refused('OUTER : while ($x) { }', 'a label is hard against its colon: OUTER:', 1, 7);
    refused('L: say 1;', on('L'), 1, 4);
    refused('L: { say 1; }', on('L'), 1, 4);
    refused('L: if ($x) { }', on('L'), 1, 4);
    refused('A: B: while ($x) { }', on('A'), 1, 4);
    refused('L: $i++ while $x;', on('L'), 1, 4);
    refused('L:', on('L'), 1, 3);
});

test('last and next are statements: alone, with a label, under if or unless (T120)', () => {
    const after = (word: string) => `after '${word}' comes ';', a label in capitals, or an if or unless: perl takes anything else for an expression that names a label`;
    refused('last + 1;', after('last'), 1, 6);
    refused('last $l;', after('last'), 1, 6);
    refused('last "L";', after('last'), 1, 6);
    refused('next while $x;', after('next'), 1, 6);
    refused('last() if $x;', after('last'), 1, 5);
    refused('next outer;', after('next'), 1, 6);
    refused('last L M;', after('last'), 1, 8);
    refused('last L while $x;', after('last'), 1, 8);
    const value = (word: string) => `${word} is a statement, not a value: write '${word} if ...;' or '${word} unless ...;'`;
    refused('say last;', value('last'), 1, 5);
    refused('my $v = next;', value('next'), 1, 9);
    refused('$x = $y ? last : next;', value('last'), 1, 11);
    refused('$x++ and last;', value('last'), 1, 10);
    refused('$x == 2 or next;', value('next'), 1, 12);
    refused('last if $x while $y;', "expected ';', found 'while'", 1, 12);
});

test('undef before a variable or a brace is undef of it, to perl (T105)', () => {
    const before = (what: string) => `undef before ${what}: perl takes what follows undef for its argument; write (undef)`;
    refused('say undef $x;', before("'$x'"), 1, 5);
    refused('$x = undef $x;', before("'$x'"), 1, 6);
    refused('if (undef) { } elsif (undef { }', before("'{'"), 1, 23);
    // A modifier is not an argument.
    assert.equal(program('$x = undef if $y;'), '[($x = undef); if $y]');
    assert.equal(program('$x = undef unless undef;'), '[($x = undef); unless undef]');
});

// What perl makes of each is in t/173-named-unary.pl and
// t/174-dot-and-x.pl, which perl checks.
test("the dot is at the level of + and -, and x at the level of * (perlop)", () => {
    assert.equal(grouped('say 1 . 2 + 3;'), '((1 . 2) + 3)');
    assert.equal(grouped('say 1 + 2 . 3;'), '((1 + 2) . 3)');
    assert.equal(grouped('say 1 . 2 * 3;'), '(1 . (2 * 3))');
    assert.equal(grouped('say "a" x 2 x 3;'), '(("a" x 2) x 3)');
    assert.equal(grouped('say "a" . "b" x 2;'), '("a" . ("b" x 2))');
    assert.equal(grouped('say 2 * 3 x 2;'), '((2 * 3) x 2)');
    assert.equal(grouped('say 2 x 3 + 2;'), '((2 x 3) + 2)');
    assert.equal(grouped('say -"2" x 2;'), '((-"2") x 2)');
    assert.equal(grouped('say 2 x 2 ** 2;'), '(2 x (2 ** 2))');
});

test('a named unary operator: brackets are its argument, and without them all that binds tighter (D41, T87)', () => {
    assert.equal(grouped('say length "abc";'), 'length["abc"]');
    assert.equal(grouped('say length("abc") . "de";'), '(length["abc"] . "de")');
    assert.equal(grouped('say length ("abc") . "de";'), '(length["abc"] . "de")');
    assert.equal(grouped('say length "abc" . "de";'), 'length[("abc" . "de")]');
    assert.equal(grouped('say length "abc" + 1 * 2;'), 'length[("abc" + (1 * 2))]');
    assert.equal(grouped('say 1 + length "ab";'), '(1 + length["ab"])');
    assert.equal(grouped('say 2 * length "ab" x 3;'), '(2 * length[("ab" x 3)])');
    assert.equal(grouped('say - length "ab" . "c";'), '(-length[("ab" . "c")])');
    assert.equal(grouped('say length -5;'), 'length[(-5)]');
    assert.equal(grouped('say uc lc "A" . "b";'), 'uc[lc[("A" . "b")]]');
    assert.equal(grouped('say ord(chr 65) + 1;'), '(ord[chr[65]] + 1)');
    assert.equal(grouped('say(length "abc");'), 'length["abc"]*');
    assert.equal(grouped('say (length "abc");'), 'length["abc"]*');
    refused('say length;', 'length needs an argument', 1, 5);
    refused('say length();', 'length needs an argument', 1, 5);
    refused('say (uc);', 'uc needs an argument', 1, 6);
    refused('say length("a", "b");', "expected ')', found ','", 1, 15);
    refused('say length * 2;', "expected a value, found '*'", 1, 12);
});

test('substr and index take their arguments in brackets (D41)', () => {
    assert.equal(grouped('say substr("abc", 1);'), 'substr["abc", 1]');
    assert.equal(grouped('say substr ("abc", 1, 1 + 1) . "d";'), '(substr["abc", 1, (1 + 1)] . "d")');
    assert.equal(grouped('say index("abc", "c", length "a");'), 'index["abc", "c", length["a"]]');
    refused('say substr "abc", 1;', 'substr needs brackets round its arguments: substr(...)', 1, 5);
    refused('say index;', 'index needs brackets round its arguments: index(...)', 1, 5);
    refused('say substr("abc");', 'substr takes 2 to 3 arguments, and here are 1', 1, 5);
    refused('say substr();', 'substr takes 2 to 3 arguments, and here are 0', 1, 5);
    refused('say index("a", "b", 0, 1);', 'index takes 2 to 3 arguments, and here are 4', 1, 5);
    refused('say substr("abc", 1,);', "expected a value, found ')'", 1, 21);
    refused('say substr("abc" 1);', "expected ')', found 1", 1, 18);
});

test('say and print take one argument, and are statements', () => {
    assert.equal(grouped('print "a" . "b";'), '("a" . "b")');
    assert.equal(grouped('print("a");'), '"a"*');
    refused('say "a", "b";', "',' after say's argument: a list is not in the language yet", 1, 8);
    refused('print("a", "b");', "expected ')', found ','", 1, 10);
    refused('say 1 + say 2;', 'say is a statement, and has no value', 1, 9);
    refused('say print "a";', 'print is a statement, and has no value', 1, 5);
    refused('print ("a") . "b";', "'.' after print (...): perl takes the brackets for all of print's arguments; bracket the whole expression", 1, 13);
    refused('print ("a") x 2;', "'x' after print (...): perl takes the brackets for all of print's arguments; bracket the whole expression", 1, 13);
    refused('print ("a"\n);', "print (...) after one blank: perl warns unless the brackets close on this line, one in a string counting too, with ';' after them: write print(...)", 1, 7);
});

test('use takes a version, or a pragma and its arguments', () => {
    assert.deepEqual(parse(lex("use utf8;\nuse open ':std', \":x\";")).body, [
        { kind: 'pragma', name: 'utf8', args: [], pos: { line: 1, col: 1 } },
        { kind: 'pragma', name: 'open', pos: { line: 2, col: 1 }, args: [
            { kind: 'str', text: "':std'", value: ':std', pos: { line: 2, col: 10 } },
            { kind: 'str', text: '":x"', value: ':x', pos: { line: 2, col: 18 } },
        ] },
    ]);
    refused('use strict;', "'use strict' is not in the language", 1, 5);
    refused('use warnings;', "'use warnings' is not in the language", 1, 5);
    refused('use 5;', "after 'use', expected a version or a pragma, found 5", 1, 5);
    refused('use "utf8";', "after 'use', expected a version or a pragma, found \"utf8\"", 1, 5);
    refused('use', "after 'use', expected a version or a pragma, found the end of the file", 1, 4);
    refused('use utf8', "expected a value, found the end of the file", 1, 9);
    refused('use open qw(:std);', "expected a value, found 'qw'", 1, 10);
    refused('use open qw(std);', "expected a value, found 'qw'", 1, 10);
    refused('use v5.42 say 1;', "expected ';', found 'say'", 1, 11);
});

test('where an operand is wanted', () => {
    const wanted = (found: string) => `expected a value, found ${found}`;
    refused('say;', wanted("';'"), 1, 4);
    refused('say 1 + ;', wanted("';'"), 1, 9);
    refused('say 1 +', wanted('the end of the file'), 1, 8);
    refused('say -;', wanted("';'"), 1, 6);
    refused('say ();', wanted("')'"), 1, 6);
    refused('say (+);', wanted("')'"), 1, 7);
    refused('say use 1;', wanted("'use'"), 1, 5);
    refused('say x 3;', wanted("'x'"), 1, 5);
    refused('say v5.42;', wanted('v5.42'), 1, 5);
    // perl has a glob `*3` and a hash `%2` here.
    refused('say 2 * *3;', wanted("'*'"), 1, 9);
    refused('say * 2;', wanted("'*'"), 1, 5);
    refused('say % 2;', wanted("'%'"), 1, 5);
    refused('say 1 % % 2;', wanted("'%'"), 1, 9);
});

test('where an operator or an end is wanted', () => {
    refused('say 1 2;', "expected ';', found 2", 1, 7);
    refused('say 1.5 5;', "expected ';', found 5", 1, 9);
    refused('say "a" "b";', "expected ';', found \"b\"", 1, 9);
    refused('say "a" "a string of more than twenty";', "expected ';', found a string", 1, 9);
    refused('say 1 (2);', "expected ';', found '('", 1, 7);
    refused('say(1 + 2;', "expected ')', found ';'", 1, 10);
    refused('say 1 + 2);', "expected ';', found ')'", 1, 10);
    refused('say (1) (2);', "expected ';', found '('", 1, 9);
    refused('say 1 + (2 3);', "expected ')', found 3", 1, 12);
    // One of perl's operators that is a word.
    refused('say 1 isa 2;', "'isa' is not in the language yet", 1, 7);
    refused('say lt 1;', "expected a value, found 'lt'", 1, 5);
    refused('say 1 foo 2;', "expected ';', found 'foo'", 1, 7);
});

test("an operator after say's brackets (T25)", () => {
    const message = (op: string) => `'${op}' after say (...): perl takes the brackets for all of say's arguments; bracket the whole expression`;
    refused('say (1 + 2) * 3;', message('*'), 1, 13);
    refused('say(1 + 2) * 3;', message('*'), 1, 12);
    refused('say ((1 + 2)) - 3;', message('-'), 1, 15);
    refused('say (1) + 2;', message('+'), 1, 9);
    refused('say\n(1)\n% 2;', message('%'), 3, 1);
});

test('say, one blank, and a bracket: all on one line (T76)', () => {
    const message = "say (...) after one blank: perl warns unless the brackets close on this line, one in a string counting too, with ';' after them: write say(...)";
    refused('say (1 +\n2);', message, 1, 5);
    refused('say (1 + 2)\n;', message, 1, 5);
    refused('say (1 + 2) # then\n;', message, 1, 5);
    refused('say (\n1);', message, 1, 5);
    // perl goes by the text: a bracket in a string counts (T100).
    refused('say ("(");', message, 1, 5);
    refused('say (")" . "a");', message, 1, 5);
    refused('say (1) # and then\n;', message, 1, 5);
    assert.equal(grouped('say (1); # and ('), '1*');
    assert.equal(grouped('say\t("(");'), '"("*');
    assert.equal(grouped('say  ("(");'), '"("*');
    assert.equal(grouped('say("(");'), '"("*');
    assert.equal(grouped('say (1 + 2) ;'), '(1 + 2)*');
    assert.equal(grouped('say (1 + 2); # after'), '(1 + 2)*');
    // perl doesn't look after two blanks, a newline, or none.
    assert.equal(grouped('say  (1 +\n2)\n;'), '(1 + 2)*');
    assert.equal(grouped('say\n(1 +\n2)\n;'), '(1 + 2)*');
    assert.equal(grouped('say(1 +\n2)\n;'), '(1 + 2)*');
});

test('every statement ends with its semicolon, and only one', () => {
    refused('use v5.42;\nsay 1', "expected ';', found the end of the file", 2, 6);
    refused('say 1\nsay 2;', "expected ';', found 'say'", 2, 1);
    refused('say 1;;', "expected a statement, found ';'", 1, 7);
});

// What perl makes of each is in t/360-logic-precedence.pl, t/361 and
// t/362, which perl checks.
test("comparison and logic: perlop's rows", () => {
    assert.equal(grouped('say !2 ** 2;'), '(!(2 ** 2))');
    assert.equal(grouped('say !1 + 1;'), '((!1) + 1)');
    assert.equal(grouped('say - !0;'), '(-(!0))');
    assert.equal(grouped('say 1 + 2 == 3 . 0;'), '((1 + 2) == (3 . 0))');
    assert.equal(grouped('say 1 < 2 == 3 > 4;'), '((1 < 2) == (3 > 4))');
    assert.equal(grouped('say 1 == 2 < 3;'), '(1 == (2 < 3))');
    assert.equal(grouped('say 1 <=> 2 lt 3;'), '(1 <=> (2 lt 3))');
    assert.equal(grouped('say 1 && 0 || 2;'), '((1 && 0) || 2)');
    assert.equal(grouped('say 1 || 0 && 2;'), '(1 || (0 && 2))');
    assert.equal(grouped('say 0 || 0 // 5 || 6;'), '(((0 || 0) // 5) || 6)');
    assert.equal(grouped('say 1 == 1 && 2 == 2;'), '((1 == 1) && (2 == 2))');
    assert.equal(grouped('say length "ab" == 2;'), '(length["ab"] == 2)');
    assert.equal(grouped('say defined 1 + 1 && 2;'), '(defined[(1 + 1)] && 2)');
    assert.equal(grouped('say(1 or 2 and 3 xor 4);'), '((1 or (2 and 3)) xor 4)*');
    assert.equal(grouped('say(not 1 || 2 and 3);'), '((not(1 || 2)) and 3)*');
    assert.equal(grouped('say(1 + not 0 || 1);'), '(1 + (not(0 || 1)))*');
    assert.equal(grouped('say(not not 1);'), '(not(not1))*');
    assert.equal(grouped('say not 1;'), '(not1)');
});

test('? : groups from the right, and its middle is its own', () => {
    assert.equal(grouped('say 1 ? 2 : 3;'), '(1 ? 2 : 3)');
    assert.equal(grouped('say 0 ? 2 : 3 ? 4 : 5;'), '(0 ? 2 : (3 ? 4 : 5))');
    assert.equal(grouped('say 1 ? 0 ? 1 : 2 : 3;'), '(1 ? (0 ? 1 : 2) : 3)');
    assert.equal(grouped('say 1 || 2 ? 3 : 4 || 5;'), '((1 || 2) ? 3 : (4 || 5))');
    assert.equal(grouped('say 1 + 2 ? 3 + 4 : 5 + 6;'), '((1 + 2) ? (3 + 4) : (5 + 6))');
    assert.equal(grouped('say(not 1 ? 2 : 3);'), '(not(1 ? 2 : 3))*');
    assert.equal(grouped('say(1 ? 2 : 3 or 4);'), '((1 ? 2 : 3) or 4)*');
    assert.equal(grouped('say 1 ? not 0 : 2;'), '(1 ? (not0) : 2)');
    refused('say 1 ? 2;', "expected ':', found ';'", 1, 10);
    refused('say 1 ? : 2;', "expected a value, found ':'", 1, 9);
    refused('say 1 ? 2 : ;', "expected a value, found ';'", 1, 13);
    refused('say ? 1 : 2;', "expected a value, found '?'", 1, 5);
    refused('say 1 : 2;', "expected ';', found ':'", 1, 7);
});

test('two comparisons of one row are refused (D50)', () => {
    const message = (b: string, a: string) => `'${b}' after '${a}': perl chains two comparisons, or refuses them, and never reads them from the left; bracket one, or join two with &&`;
    refused('say 1 < 2 < 3;', message('<', '<'), 1, 11);
    refused('say 1 < 2 ge 3;', message('ge', '<'), 1, 11);
    refused('say 1 == 2 == 3;', message('==', '=='), 1, 12);
    refused('say 1 != 2 eq 3;', message('eq', '!='), 1, 12);
    refused('say 1 <=> 2 <=> 3;', message('<=>', '<=>'), 1, 13);
    refused('say 1 cmp 2 == 3;', message('==', 'cmp'), 1, 13);
    refused('say 1 < 2 == 3 == 4;', message('==', '=='), 1, 16);
    assert.equal(grouped('say((1 < 2) < 3);'), '((1 < 2)* < 3)*');
    assert.equal(grouped('say 1 < 2 && 2 < 3;'), '((1 < 2) && (2 < 3))');
});

test('undef, true and false (D47, D48)', () => {
    assert.equal(grouped('say undef // 1;'), '(undef // 1)');
    assert.equal(grouped('say undef || undef && 2;'), '(undef || (undef && 2))');
    assert.equal(grouped('say undef ? 1 : undef;'), '(undef ? 1 : undef)');
    assert.equal(grouped('say defined undef;'), 'defined[undef]');
    assert.equal(grouped('say defined(undef) // 1;'), '(defined[undef] // 1)');
    assert.equal(grouped('say defined undef // 1;'), '(defined[undef] // 1)');
    assert.equal(grouped('say substr("a", undef, undef);'), 'substr["a", undef, undef]');
    assert.equal(grouped('say((undef) + 1);'), '(undef* + 1)*');
    assert.equal(grouped('say(undef or undef xor 1);'), '((undef or undef) xor 1)*');
    assert.equal(grouped('say true -1 . false x 3;'), '((true - 1) . (false x 3))');
    const before = (what: string) => `undef before ${what}: perl takes what follows undef for its argument; write (undef)`;
    refused('say undef + 1;', before("'+'"), 1, 5);
    refused('say undef * 2;', before("'*'"), 1, 5);
    refused('say undef == 1;', before("'=='"), 1, 5);
    refused('say undef . "a";', before("'.'"), 1, 5);
    refused('say undef x 3;', before("'x'"), 1, 5);
    refused('say undef lt 1;', before("'lt'"), 1, 5);
    refused('say undef 1;', before('1'), 1, 5);
    refused('say undef "a";', before('"a"'), 1, 5);
    refused('say undef undef;', before("'undef'"), 1, 5);
    refused('say undef !1;', before("'!'"), 1, 5);
    refused('say undef(1);', 'undef is written without brackets', 1, 10);
    refused('say undef ();', 'undef is written without brackets', 1, 11);
    refused('say true();', 'true is written without brackets', 1, 9);
    refused('say false (1);', 'false is written without brackets', 1, 11);
});

test('the word operators: after say, in a list of arguments, after not (...) (D51)', () => {
    const loose = (op: string) => `'${op}' after say's argument: it binds more loosely than say does, and joins what say returns, to perl; bracket the argument, say(... ${op} ...)`;
    refused('say 0 or 2;', loose('or'), 1, 7);
    refused('say 1 and 2;', loose('and'), 1, 7);
    refused('say not 1 xor 2;', loose('xor'), 1, 11);
    refused('say (0) or 2;', "'or' after say (...): perl takes the brackets for all of say's arguments; bracket the whole expression", 1, 9);
    const rest = 'not in a list of arguments takes the rest of the list, to perl: write not(...)';
    refused('say substr("abc", not 0, 1);', rest, 1, 19);
    refused('say substr("abc", 1 + not 0, 1);', rest, 1, 23);
    refused('say index("abc", length not 1);', rest, 1, 25);
    refused('say substr("abc", 0 or 1);', "'or' in a list of arguments takes the whole list for its left side, to perl: bracket what it joins", 1, 21);
    assert.equal(grouped('say substr("abc", (not 0), not(1));'), 'substr["abc", (not0)*, (not1*)]');
    assert.equal(grouped('say substr("abc", (0 or 1));'), 'substr["abc", (0 or 1)*]');
    assert.equal(grouped('say length(not 1);'), 'length[(not1)]');
    const after = (op: string) => `'${op}' after not (...): perl takes the brackets for all of not's operand; bracket the whole of it, not ((...) ${op} ...), or the not itself`;
    refused('say(not (0) || 1);', after('||'), 1, 13);
    refused('say(not(0) + 1);', after('+'), 1, 12);
    refused('say(not (0) == 1);', after('=='), 1, 13);
    refused('say(not (0) ? 1 : 2);', after('?'), 1, 13);
    refused('say(not (0) x 2);', after('x'), 1, 13);
    refused('say(not());', 'not needs an operand', 1, 5);
    assert.equal(grouped('say(not (0) and 1);'), '((not0*) and 1)*');
    assert.equal(grouped('say(not (0) or not (1));'), '((not0*) or (not1*))*');
    assert.equal(grouped('say not (1);'), '(not1*)');
    assert.equal(grouped('say((not 0) || 1);'), '((not0)* || 1)*');
});

test('an unbracketed ! on the left of a comparison (T115)', () => {
    const message = (op: string) => `'!' before '${op}': perl warns of a precedence problem; write !(... ${op} ...), or (!...) ${op} ...`;
    refused('say !1 == 0;', message('=='), 1, 5);
    refused('say ! defined 1 lt 2;', message('lt'), 1, 5);
    refused('say +!1 < 2;', message('<'), 1, 6);
    refused('say !!1 != 2;', message('!='), 1, 5);
    refused('say !1 <=> 2;', message('<=>'), 1, 5);
    assert.equal(grouped('say((!1) == 0);'), '((!1)* == 0)*');
    assert.equal(grouped('say !(1 == 0);'), '(!(1 == 0)*)');
    assert.equal(grouped('say 0 == !1;'), '(0 == (!1))');
    assert.equal(grouped('say !1 + 1 == 1;'), '(((!1) + 1) == 1)');
    assert.equal(grouped('say !1 && 2 == 2;'), '((!1) && (2 == 2))');
    assert.equal(grouped('say -1 == -1;'), '((-1) == (-1))');
});
