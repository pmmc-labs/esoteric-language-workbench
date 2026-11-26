import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { CompileError } from '../src/errors.ts';

const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => lex(src), (e: unknown) => {
        assert.ok(e instanceof CompileError, String(e));
        assert.deepEqual([e.message, e.line, e.col], [message, line, col]);
        return true;
    });

test('tokens, each with its line and column', () => {
    const tokens = lex('# first\nuse v5.42;\n\tsay 42;  # after\n say\n9223372036854775807 ;');
    assert.deepEqual(tokens.map(t => [t.kind, t.text, t.pos.line, t.pos.col]), [
        ['word', 'use', 2, 1], ['version', 'v5.42', 2, 5], [';', ';', 2, 10],
        ['word', 'say', 3, 2], ['int', '42', 3, 6], [';', ';', 3, 8],
        ['word', 'say', 4, 2], ['int', '9223372036854775807', 5, 1], [';', ';', 5, 21],
        ['eof', '', 5, 22],
    ]);
});

test('an empty file is its end, and a comment needs no newline after it', () => {
    assert.deepEqual(lex(''), [{ kind: 'eof', text: '', pos: { line: 1, col: 1 } }]);
    assert.deepEqual(lex('\n  # only this').at(-1), { kind: 'eof', text: '', pos: { line: 2, col: 14 } });
});

test('a version literal is v, digits, and groups of .digits', () => {
    const kinds = (src: string) => lex(src).map(t => `${t.kind} ${t.text}`.trim());
    assert.deepEqual(kinds('v5.42'), ['version v5.42', 'eof']);
    assert.deepEqual(kinds('v5.42.0'), ['version v5.42.0', 'eof']);
    assert.deepEqual(kinds('v5'), ['version v5', 'eof']);
    assert.deepEqual(kinds('v v5x value'), ['word v', 'word v5x', 'word value', 'eof']);
});

test('a version ends at a blank or a semicolon, as perl has it (T75)', () => {
    const message = (c: string) => `v5.42 runs into '${c}': perl reads a version only before a blank or ';'`;
    refused('use v5.42#c\n;', message('#'), 1, 5);
    refused('use v5.42# c\n;', message('#'), 1, 5);
    refused('v5.42.;', message('.'), 1, 1);
    refused('v5.42x;', message('x'), 1, 1);
    assert.equal(lex('use v5.42 #c\n;').length, 4);
    assert.equal(lex('use v5.42\t;').length, 4);
    assert.equal(lex('use v5.42\n;').length, 4);
    assert.equal(lex('use v5.42').length, 3);
    refused('use v5.42\r\n;', 'a control character (U+000D) is not in the language', 1, 10);
});

const literals = (src: string) => lex(src).slice(0, -1).map(t => `${t.kind} ${t.text}`);
// Each word of `src` on its own: after a value a dot is an operator.
const each = (src: string) => src.split(' ').flatMap(literals);

test('numeric literals (D38)', () => {
    assert.deepEqual(each('0 42 1_000 0x1F 0XfF 0b101 0B1 0o17 0O7 0xff_ff'),
        ['int 0', 'int 42', 'int 1_000', 'int 0x1F', 'int 0XfF', 'int 0b101', 'int 0B1', 'int 0o17', 'int 0O7', 'int 0xff_ff']);
    assert.deepEqual(each('1.5 .5 0.25 1e3 1E3 1.5e-3 .5E+2 1e007 1_0.2_5 1e1_0 0e0'),
        ['num 1.5', 'num .5', 'num 0.25', 'num 1e3', 'num 1E3', 'num 1.5e-3', 'num .5E+2', 'num 1e007', 'num 1_0.2_5', 'num 1e1_0', 'num 0e0']);
    // Leading zeros are the checker's to refuse: they lex.
    assert.deepEqual(each('010 00.5'), ['int 010', 'num 00.5']);
});

test('after a value a dot joins and x repeats; before one a dot begins a number (T90)', () => {
    assert.deepEqual(literals('1 .5'), ['int 1', 'op .', 'int 5']);
    assert.deepEqual(literals('1 . .5'), ['int 1', 'op .', 'num .5']);
    assert.deepEqual(literals('"a".5'), ['str "a"', 'op .', 'int 5']);
    assert.deepEqual(literals('(1).5'), ['( (', 'int 1', ') )', 'op .', 'int 5']);
    assert.deepEqual(literals('length .5'), ['word length', 'num .5']);
    assert.deepEqual(literals('say .5 x .5'), ['word say', 'num .5', 'op x', 'num .5']);
    assert.deepEqual(literals('"a" x 3'), ['str "a"', 'op x', 'int 3']);
    assert.deepEqual(literals('"a"x 3'), ['str "a"', 'op x', 'int 3']);
    assert.deepEqual(literals('2 x(3)'), ['int 2', 'op x', '( (', 'int 3', ') )']);
    assert.deepEqual(literals('1 x"2"'), ['int 1', 'op x', 'str "2"']);
    // Where a value is wanted, x is a word, and so is a longer word after one.
    assert.deepEqual(literals('say x'), ['word say', 'word x']);
    assert.deepEqual(literals('1 xy'), ['int 1', 'word xy']);
    refused('say "a" x3;', 'x3: the repetition operator is a word of its own: write x 3', 1, 9);
    refused('say "a"x3;', 'x3: the repetition operator is a word of its own: write x 3', 1, 8);
    // `x=` is one operator, the assignment, as it is to perl.
    assert.deepEqual(literals('$s x= 3'), ['var $s', 'op x=', 'int 3']);
    assert.deepEqual(literals('$s x =3'), ['var $s', 'op x', 'op =', 'int 3']);
});

const value = (src: string) => {
    const t = lex(src)[0]!;
    assert.equal(t.kind, 'str');
    return t.kind === 'str' ? t.value : '';
};

test('a string in single quotes: a backslash is itself, but before a backslash or the quote', () => {
    assert.equal(value("'abc'"), 'abc');
    assert.equal(value("''"), '');
    assert.equal(value("'a\\b'"), 'a\\b');
    assert.equal(value("'it\\'s'"), "it's");
    assert.equal(value("'a\\nb\\q\\x41'"), 'a\\nb\\q\\x41');
    assert.equal(value("'$x @y \"'"), '$x @y "');
    assert.equal(value("'two\nlines\t'"), 'two\nlines\t');
    assert.equal(value("'a\\\\'"), 'a\\');
    refused("say 'abc", "a string that never ends: it begins with ' here", 1, 5);
    refused("say 'abc\\'", "a string that never ends: it begins with ' here", 1, 5);
});

test('a string in double quotes: the escapes (D43)', () => {
    assert.equal(value('"a\\n\\t\\r\\f\\b\\a\\e\\0"'), 'a\n\t\r\f\b\x07\x1b\0');
    assert.equal(value('"\\\\ \\" \\$ \\@"'), '\\ " $ @');
    assert.equal(value('"\\x41\\x7e\\xFF"'), 'A~\xff');
    assert.equal(value('"\\x{41}\\x{263A}\\x{1F600}\\x{10FFFF}"'), 'A\u263a\u{1F600}\u{10FFFF}');
    assert.equal(value('"\\101\\7\\12\\777\\0000"'), 'A\x07\n\u01ff\x000');
    assert.equal(value('"\\o{101}\\N{U+263a}"'), 'A\u263a');
    assert.equal(value('"\\-\\ \\_\\{\\\'"'), "- _{'");
    assert.equal(value('"it\'s\ntwo # lines"'), "it's\ntwo # lines");
    const at = (src: string, message: string, col: number) => refused(src, message, 1, col);
    at('"\\q"', '\\q is not an escape in the language', 2);
    at('"ab\\8"', '\\8 is not an escape in the language', 4);
    at('"\\c["', '\\c is not an escape in the language', 2);
    at('"\\Ux"', '\\U is not an escape in the language', 2);
    at('"\\N{LATIN SMALL LETTER A}"', '\\N{...} is not an escape in the language', 2);
    at('"\\x"', '\\x: \\x takes two hex digits, or any number in braces: \\x0A, \\x{263A}', 2);
    at('"\\x4"', '\\x4: \\x takes two hex digits, or any number in braces: \\x0A, \\x{263A}', 2);
    at('"\\x4g"', '\\x4: \\x takes two hex digits, or any number in braces: \\x0A, \\x{263A}', 2);
    at('"\\x{}"', '\\x{...}: hex digits between the braces, and nothing else', 2);
    at('"\\x{4 1}"', '\\x{...}: hex digits between the braces, and nothing else', 2);
    at('"\\x{41"', '\\x{...}: hex digits between the braces, and nothing else', 2);
    at('"\\o{8}"', '\\o{...}: octal digits between the braces, and nothing else', 2);
    at('"\\N{U+}"', '\\N{U+...}: hex digits between the braces, and nothing else', 2);
    at('"\\x{D800}"', '\\x{D800} is not a character: a surrogate, or past U+10FFFF', 2);
    at('"\\x{110000}"', '\\x{110000} is not a character: a surrogate, or past U+10FFFF', 2);
    at('"\\x{FFFFFFFFFFFFFFFFFFFF}"', '\\x{FFFFFFFFFFFFFFFFFFFF} is not a character: a surrogate, or past U+10FFFF', 2);
    at('"\\N{U+DFFF}"', '\\N{U+DFFF} is not a character: a surrogate, or past U+10FFFF', 2);
    at('"\\18"', '\\18: an octal escape that 8 cuts short, and perl warns: write \\001', 2);
    at('"\\129"', '\\129: an octal escape that 9 cuts short, and perl warns: write \\012', 2);
    at('"a\\\tb"', 'a backslash before a tab is not in the language', 3);
    at('"a\\\nb"', 'a backslash before the end of a line is not in the language', 3);
    at('"cost: $x"', "'$' in a double-quoted string is a variable to perl: write \\$ (interpolation is not in the language yet)", 8);
    at('"a@b"', "'@' in a double-quoted string is a variable to perl: write \\@ (interpolation is not in the language yet)", 3);
    at('"abc', 'a string that never ends: it begins with " here', 1);
    at('"abc\\', 'a string that never ends: it begins with " here', 1);
    at('"abc\\"', 'a string that never ends: it begins with " here', 1);
});

test('a string token is the literal as written, and where it starts', () => {
    const tokens = lex('say "a\nb" . \'c\';');
    assert.deepEqual(tokens.map(t => [t.kind, t.text, t.pos.line, t.pos.col]), [
        ['word', 'say', 1, 1], ['str', '"a\nb"', 1, 5], ['op', '.', 2, 4], ['str', "'c'", 2, 6], [';', ';', 2, 9], ['eof', '', 2, 10],
    ]);
});

test('the operators of step 4: the longest wins, and a word is one only where an operator may stand', () => {
    assert.deepEqual(literals('1 <=> 2 <= 3 < 4 == 5 != 6 >= 7 > 8'),
        ['int 1', 'op <=>', 'int 2', 'op <=', 'int 3', 'op <', 'int 4', 'op ==', 'int 5', 'op !=', 'int 6', 'op >=', 'int 7', 'op >', 'int 8']);
    assert.deepEqual(literals('1&&2||3//4'), ['int 1', 'op &&', 'int 2', 'op ||', 'int 3', 'op //', 'int 4']);
    assert.deepEqual(literals('!1 ? !!2 : 3'), ['op !', 'int 1', '? ?', 'op !', 'op !', 'int 2', ': :', 'int 3']);
    assert.deepEqual(literals('1?2:3'), ['int 1', '? ?', 'int 2', ': :', 'int 3']);
    assert.deepEqual(literals('"a"lt"b" cmp 1 eq 2'), ['str "a"', 'op lt', 'str "b"', 'op cmp', 'int 1', 'op eq', 'int 2']);
    assert.deepEqual(literals('1 and 2 or not 3 xor 4'), ['int 1', 'op and', 'int 2', 'op or', 'op not', 'int 3', 'op xor', 'int 4']);
    // Where a value is wanted `lt` and `and` are words, and where an
    // operator is, `not` is; and a longer word is never an operator.
    assert.deepEqual(literals('say lt'), ['word say', 'word lt']);
    assert.deepEqual(literals('1 not 2'), ['int 1', 'word not', 'int 2']);
    assert.deepEqual(literals('1 lt2'), ['int 1', 'word lt2']);
    assert.deepEqual(literals('1 andy 2'), ['int 1', 'word andy', 'int 2']);
    // `true`, `false` and `undef` are values: an operator comes next.
    assert.deepEqual(literals('true .5'), ['word true', 'op .', 'int 5']);
    assert.deepEqual(literals('false x 3'), ['word false', 'op x', 'int 3']);
    assert.deepEqual(literals('undef lt 1'), ['word undef', 'op lt', 'int 1']);
    assert.deepEqual(literals('defined .5'), ['word defined', 'num .5']);
    // Only a sign is ambiguous after a named unary operator.
    assert.deepEqual(literals('defined !1'), ['word defined', 'op !', 'int 1']);
    assert.deepEqual(literals('length ! 1'), ['word length', 'op !', 'int 1']);
    assert.deepEqual(literals('length not 1'), ['word length', 'op not', 'int 1']);
    refused('say defined - 1;', 'defined -: perl warns that this is ambiguous: write defined(-...)', 1, 13);
});

test('a sign after a named unary operator: a blank before it and none after', () => {
    assert.deepEqual(literals('length -5'), ['word length', 'op -', 'int 5']);
    assert.deepEqual(literals('ord +"a"'), ['word ord', 'op +', 'str "a"']);
    assert.deepEqual(literals('length\t-5'), ['word length', 'op -', 'int 5']);
    refused('length\n-5', 'length -: perl warns that this is ambiguous: write length(-...)', 2, 1);
    refused('length\n  -5', 'length -: perl warns that this is ambiguous: write length(-...)', 2, 3);
    refused('length # c\n -5', 'length -: perl warns that this is ambiguous: write length(-...)', 2, 2);
    assert.deepEqual(literals('length(- 5)'), ['word length', '( (', 'op -', 'int 5', ') )']);
    assert.deepEqual(literals('say - 5'), ['word say', 'op -', 'int 5']);
    refused('say length - 5;', 'length -: perl warns that this is ambiguous: write length(-...)', 1, 12);
    refused('say length-5;', 'length -: perl warns that this is ambiguous: write length(-...)', 1, 11);
    refused('say chr +\n65;', 'chr +: perl warns that this is ambiguous: write chr(+...)', 1, 9);
    refused('say uc#c\n-5;', 'uc -: perl warns that this is ambiguous: write uc(-...)', 2, 1);
});

test('use utf8: a character past ASCII, in a string or a comment, on a later line (T73)', () => {
    const tokens = lex('use utf8;\n# caf\u00e9\nsay "\u{1F600}\u00e9" . "a"; # \u263a');
    assert.deepEqual(tokens.slice(3).map(t => [t.kind, t.text, t.pos.line, t.pos.col]), [
        ['word', 'say', 3, 1], ['str', '"\u{1F600}\u00e9"', 3, 5], ['op', '.', 3, 10], ['str', '"a"', 3, 12], [';', ';', 3, 15], ['eof', '', 3, 20],
    ]);
    const needs = (c: string) => `a character past ASCII (${c}) needs 'use utf8;' on a line before it`;
    refused('use utf8; say "\u00e9";', needs('U+00E9'), 1, 16);
    refused('use utf8; # \u00e9', needs('U+00E9'), 1, 13);
    refused('use utf8\n; say "\u00e9";', needs('U+00E9'), 2, 8);
    assert.equal(lex('use utf8\n;\nsay "\u00e9";').length, 7);
    refused('say "\u00e9";\nuse utf8;', needs('U+00E9'), 1, 6);
    refused('use utf8;\nsay \u00e9;', 'a character past ASCII (U+00E9) outside a string or a comment is not in the language', 2, 5);
    refused('use utf8;\nsay "\\\u00e9";', 'a backslash before U+00E9 is not in the language', 2, 6);
    refused('use utf8;\n"\x85', 'a string that never ends: it begins with " here', 2, 1);
    refused('use utf8;\n"a\x00"', 'a control character (U+0000) is not in the language', 2, 3);
});

test('a number hard against an operator is still one number', () => {
    assert.deepEqual(literals('2*.5'), ['int 2', 'op *', 'num .5']);
    assert.deepEqual(literals('2**-.5'), ['int 2', 'op **', 'op -', 'num .5']);
    assert.deepEqual(literals('1e3-1'), ['num 1e3', 'op -', 'int 1']);
    assert.deepEqual(literals('1e-3-1'), ['num 1e-3', 'op -', 'int 1']);
    assert.deepEqual(literals('1e+3+1'), ['num 1e+3', 'op +', 'int 1']);
    assert.deepEqual(literals('7%.5'), ['int 7', 'op %', 'num .5']);
    assert.deepEqual(literals('(.5)'), ['( (', 'num .5', ') )']);
});

test('a number that runs into a letter, a digit or a dot is not one (T62, T78)', () => {
    const not = (text: string) => `${text} is not a number in the language`;
    refused('say 42x3;', not('42x3'), 1, 5);
    refused('say 1.5.5;', not('1.5.5'), 1, 5);
    refused('say .5.5;', not('.5.5'), 1, 5);
    // (`1..3` is a range, from step 9: two dots are an operator.)
    assert.deepEqual(lex('1..3').map(t => t.text), ['1', '..', '3', '']);
    refused('say 0x1.8;', not('0x1.8'), 1, 5);
    refused('say 0x1p3;', not('0x1p3'), 1, 5);
    refused('say 0xG;', not('0xG'), 1, 5);
    refused('say 0b12;', not('0b12'), 1, 5);
    refused('say 0o8;', not('0o8'), 1, 5);
    refused('say 1e;', not('1e'), 1, 5);
    refused('say 1e+;', not('1e'), 1, 5);
    refused('say 1e3e3;', not('1e3e3'), 1, 5);
    refused('say 1.5e3.2;', not('1.5e3.2'), 1, 5);
    refused('say 0x;', not('0x'), 1, 5);
    refused('say 1.e3;', not('1.e3'), 1, 5);
});

test('a point needs a digit after it', () => {
    refused('say 1.;', '1. ends with a point: write 1.0', 1, 5);
    refused('say (1.);', '1. ends with a point: write 1.0', 1, 6);
    refused('say 1. + 2;', '1. ends with a point: write 1.0', 1, 5);
});

test('an underscore goes between two digits (T82)', () => {
    const message = (text: string) => `${text}: an underscore goes between two digits`;
    refused('say 1__0;', message('1__0'), 1, 5);
    refused('say 1_;', message('1_'), 1, 5);
    refused('say 0x_ff;', message('0x_ff'), 1, 5);
    refused('say 0xff_;', message('0xff_'), 1, 5);
    refused('say 1_.5;', message('1_.5'), 1, 5);
    refused('say 1.5_;', message('1.5_'), 1, 5);
    refused('say 1e3_;', message('1e3_'), 1, 5);
    refused('say 0b_1;', message('0b_1'), 1, 5);
});

test('brackets and operators', () => {
    const tokens = lex('say(1+-2 %3)\n* 4;');
    assert.deepEqual(tokens.map(t => [t.kind, t.text, t.pos.line, t.pos.col]), [
        ['word', 'say', 1, 1], ['(', '(', 1, 4], ['int', '1', 1, 5], ['op', '+', 1, 6], ['op', '-', 1, 7],
        ['int', '2', 1, 8], ['op', '%', 1, 10], ['int', '3', 1, 11], [')', ')', 1, 12],
        ['op', '*', 2, 1], ['int', '4', 2, 3], [';', ';', 2, 4], ['eof', '', 2, 5],
    ]);
});

test("the longest of perl's operators is the token, in the language or not (T27)", () => {
    assert.deepEqual(lex('--5 1--2 ++5 2**=3').map(t => t.text), ['--', '5', '1', '--', '2', '++', '5', '2', '**=', '3', '']);
    assert.deepEqual(lex('$x+++$y').map(t => t.text), ['$x', '++', '+', '$y', '']);
    assert.deepEqual(lex('$x---$y').map(t => t.text), ['$x', '--', '-', '$y', '']);
    assert.deepEqual(lex('$x||=1 $x//=1 $x&&=1 $x.=1 $x%=1').map(t => t.text),
        ['$x', '||=', '1', '$x', '//=', '1', '$x', '&&=', '1', '$x', '.=', '1', '$x', '%=', '1', '']);
    refused('say 1 << 2;', "'<<' is not in the language yet", 1, 7);
    refused('say 1 ^^ 2;', "'^^' is not in the language yet", 1, 7);
    refused('say 1 ~~ 2;', "'~~' is not in the language yet", 1, 7);
    refused('say 1 =~ 2;', "'=~' is not in the language yet", 1, 7);
    refused('say 1 !~ 2;', "'!~' is not in the language yet", 1, 7);
    refused('say 1 -> 2;', "'->' is not in the language yet", 1, 7);
    refused('say 7 <<= 2;', "'<<=' is not in the language yet", 1, 7);
    refused('say 7 |= 2;', "'|=' is not in the language yet", 1, 7);
    refused('say 1 ... 5;', "'...' is not in the language yet", 1, 7);
    refused('say 1 & 2;', "'&' is not in the language yet", 1, 7);
    refused('say 1 => 2;', "'=>' is not in the language yet", 1, 7);
    // With a blank between them they are two, as they are to perl.
    assert.deepEqual(lex('- - + +').map(t => t.text), ['-', '-', '+', '+', '']);
});

test('a character the language has no use for yet', () => {
    refused('say `x`;', "'`' is not in the language yet", 1, 5);
    // An array, its last index, and an element, from step 9.
    assert.deepEqual(lex('@x $#x $x[1] @x[0, 1]').map(t => t.kind), ['array', 'lastindex', 'var', '[', 'int', ']', 'array', '[', 'int', ',', 'int', ']', 'eof']);
    refused('say @ x;', "after '@' comes a name: a letter or '_', then letters, digits and '_'", 1, 5);
    refused('say $# x;', "after '$#' comes an array's name: $#a is the last index of @a", 1, 5);
    refused('say @_;', '@_ is not in the language: a sub has a signature (D17)', 1, 5);
});

test('a variable is a dollar and a name, hard against it (D55)', () => {
    const tokens = lex('my $x = $y_2;\n{ $_z }');
    assert.deepEqual(tokens.map(t => [t.kind, t.text, t.pos.line, t.pos.col]), [
        ['word', 'my', 1, 1], ['var', '$x', 1, 4], ['op', '=', 1, 7], ['var', '$y_2', 1, 9], [';', ';', 1, 13],
        ['{', '{', 2, 1], ['var', '$_z', 2, 3], ['}', '}', 2, 7], ['eof', '', 2, 8],
    ]);
    assert.deepEqual(tokens[1], { kind: 'var', text: '$x', name: 'x', pos: { line: 1, col: 4 } });
    const message = "after '$' comes a name: a letter or '_', then letters, digits and '_'";
    refused('say $ x;', message, 1, 5);
    refused('say ${x};', message, 1, 5);
    refused('say $1;', message, 1, 5);
    refused('say $$;', message, 1, 5);
    refused('say $', message, 1, 5);
    // perl's own. `$_` is a token since step 10b, and an element of
    // perl's `@_` is not.
    // `$a` and `$b` are tokens since step 10c: a `sort` block's. That
    // they are nowhere else is the parser's and the resolver's to say.
    assert.deepEqual(lex('my $a = $b;').map(t => t.text), ['my', '$a', '=', '$b', ';', '']);
    assert.deepEqual(lex('say $_;').map(t => t.text), ['say', '$_', ';', '']);
    refused('say $_[0];', "$_[ is an element of perl's own @_ or %_, which are not in the language", 1, 5);
    assert.deepEqual(lex('$ab $_1 $A').map(t => t.text), ['$ab', '$_1', '$A', '']);
    // perl's longest name is 251 characters (T126).
    assert.equal(lex('$' + 'n'.repeat(251)).length, 2);
    refused('my $' + 'n'.repeat(252) + ';', 'a name of more than 251 characters: perl refuses it as too long', 1, 4);
});

test("a sign hard after '=' with a blank after it, which perl warns is an operator reversed (T127)", () => {
    const message = (sign: string) => `'=${sign}' with a blank after it: perl warns that it reads as '${sign}=' reversed; put a blank after the '='`;
    refused('$x =- $y;', message('-'), 1, 4);
    refused('$x =+ $y;', message('+'), 1, 4);
    refused('my $x =-\n$y;', message('-'), 1, 7);
    refused('$x =-\t1;', message('-'), 1, 4);
    for (const src of ['$x =-$y;', '$x = -$y;', '$x = - $y;', '$x=-$y;', '$x ==- 1;', '$x +=- 1;', '$x .=- 1;', '$x -=+ 1;', '$x =--$y;', '$x <=- 1;']) {
        assert.ok(lex(src).length > 3, src);
    }
});

test('after a variable an operator comes, as after any value', () => {
    const kinds = (src: string) => lex(src).map(t => `${t.kind} ${t.text}`).slice(0, -1);
    assert.deepEqual(kinds('$n x 3'), ['var $n', 'op x', 'int 3']);
    assert.deepEqual(kinds('$n .5'), ['var $n', 'op .', 'int 5']);
    assert.deepEqual(kinds('$n.$m'), ['var $n', 'op .', 'var $m']);
    // And after a `++` or `--` that came after one, but not before one.
    assert.deepEqual(kinds('$n++ x 3'), ['var $n', 'op ++', 'op x', 'int 3']);
    assert.deepEqual(kinds('$n-- .5'), ['var $n', 'op --', 'op .', 'int 5']);
    assert.deepEqual(kinds('$n++ or 1'), ['var $n', 'op ++', 'op or', 'int 1']);
    assert.deepEqual(kinds('1 + ++ .5'), ['int 1', 'op +', 'op ++', 'num .5']);
});

// What perl makes of each is in t/561-handle-shapes.pl, which perl checks,
// and in the refused tests after it.
test('a variable first after say or print, a blank, and what could begin a value (T111)', () => {
    const message = (lop: string, tail: string, c: string) =>
        `${lop} $x ${tail}: perl takes $x for a file handle here; put a blank after the '${c}', or none before it`;
    refused('say $x -1;', message('say', '-1', '-'), 1, 5);
    refused('print $x +1;', message('print', '+1', '+'), 1, 7);
    refused('say($x -$y);', message('say', '-$', '-'), 1, 5);
    refused('say (($x -1));', message('say', '-1', '-'), 1, 7);
    refused('say $x\n  # why\n -1;', message('say', '-1', '-'), 1, 5);
    refused('say $x .5;', message('say', '.5', '.'), 1, 5);
    refused('say $x *y;', message('say', '*y', '*'), 1, 5);
    refused('say $x %y;', message('say', '%y', '%'), 1, 5);
    refused('say $x <y;', message('say', '<y', '<'), 1, 5);
    refused('say $x /2;', message('say', '/2', '/'), 1, 5);
    refused('say $x ++;', message('say', '++', '+'), 1, 5);
    // substr and index are list operators to perl too (T125), in their
    // first argument; length and its kin are not.
    refused('say substr($x -1, 0);', message('substr', '-1', '-'), 1, 12);
    refused('say index($x .5, "c");', message('index', '.5', '.'), 1, 11);
    refused('say substr(($x -1), 0);', message('substr', '-1', '-'), 1, 13);
    for (const src of ['say substr($s, $x -1);', 'say substr($s, 0, $x -1);', 'say index($s, $x -1);', 'say length($x -1);',
        'say length $x -1;', 'say uc($x -1);', 'say substr($x - 1, 0);', 'say substr($x-1, 0);', 'say defined($x -1);']) {
        assert.ok(lex(src).length > 3, src);
    }
    // Not a handle: a blank after the operator, none before it, an
    // assignment, a slash that is `//`, and anywhere but first after say.
    for (const src of ['say $x - 1;', 'say $x-1;', 'say $x -= 1;', 'say $x += 1;', 'say $x //2;', 'say $x /= 2;',
        'say $x *2;', 'say $x %2;', 'say $x <2;', 'say $x ."a";', 'say $x . 5;', 'say 1 + $x -1;', 'say -$x -1;',
        'my $y = $x -1;', 'say $x ?1 : 2;', 'say $x x 2;', 'say $x;', 'say $x if $x -1;']) {
        assert.ok(lex(src).length > 3, src);
    }
});

test('a character past ASCII, wherever it stands', () => {
    const needs = (c: string) => `a character past ASCII (${c}) needs 'use utf8;' on a line before it`;
    refused('say 42; # café', needs('U+00E9'), 1, 14);
    refused('\nsay é;', needs('U+00E9'), 2, 5);
    refused('# \u{1F600}', needs('U+1F600'), 1, 3);
    refused('say "é";', needs('U+00E9'), 1, 6);
    // A byte order mark.
    refused('﻿use v5.42;', needs('U+FEFF'), 1, 1);
    // Half of a pair, which no file that is UTF-8 holds.
    refused('use utf8;\n"\ud800"', 'U+D800 is not a character', 2, 2);
});

test('a control character, wherever it stands', () => {
    refused('use v5.42;\r\nsay 42;', 'a control character (U+000D) is not in the language', 1, 11);
    refused('say 1; # \x04', 'a control character (U+0004) is not in the language', 1, 10);
    refused('say 1;\x1a', 'a control character (U+001A) is not in the language', 1, 7);
    refused('\x00', 'a control character (U+0000) is not in the language', 1, 1);
    refused('say\x0c1;', 'a control character (U+000C) is not in the language', 1, 4);
    refused('# \x7f', 'a control character (U+007F) is not in the language', 1, 3);
});

test("a line that starts '#!', the first or any other (T72)", () => {
    const message = "a line that starts '#!' is not in the language: perl can take switches from it";
    refused('#!/usr/bin/perl -n\nuse v5.42;', message, 1, 1);
    refused('#!', message, 1, 1);
    refused(' \t#!perl', message, 1, 3);
    refused('\n#!/usr/bin/perl -n\nuse v5.42;', message, 2, 1);
    refused('use v5.42;\n# line 1\n  #!perl -n\nsay 2;', message, 3, 3);
    refused('use v5.42;\nsay\n#!perl\n1;', message, 3, 1);
    // After a token on its line, or after another `#`, it is a comment.
    assert.equal(lex('use v5.42; #!perl -n').length, 4);
    assert.equal(lex('# !perl -n\n# #!perl -n\n##!').length, 1);
});
