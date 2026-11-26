#!/usr/bin/env python3
# Writes step 12b's refusal tests from a table written by hand: the program,
# the text the message points at (its column is counted here, from the
# program's own text), and the message. Nothing here asks the compiler.
# What perl does with each is in its comment, pasted from perl 5.42.
#
#     python3 docs/briefs/step12b-refusals.py 1720
import sys
T = []
def r(name, why, body, at, message, nth=1):
    T.append((name, why, body, at, message, nth))

H = 'my %h = (a => 1, b => 2, c => 3, d => 4);\n'
A = 'my @a = (1, 2, 3);\n'

# ---- a slice
ONE = lambda s, e: f'{s} with one {"key" if "{" in s else "index"}: perl warns that it is better written {e}'
r('slice-of-one', 'perl warns: Scalar value @h{"a"} better written as $h{"a"}.', H + 'say @h{"a"};', '@h', ONE('@h{...}', '$h{...}'))
r('slice-of-one-word', 'perl warns of it too, and the word is the key a.', H + 'say @h{a};', '@h', ONE('@h{...}', '$h{...}'))
r('slice-of-two-words', 'perl does not compile it: Bareword "a" not allowed.', H + 'say @h{a, b};', 'a,', "'a' is not in the language; a call of a sub of the program's has brackets: a(...)")
r('slice-with-no-key', 'perl does not compile it: syntax error.', H + 'say @h{};', '{}', 'a slice with no key: perl refuses it')
r('slice-for-one-value', 'perl gives the last: 2.', H + 'my $x = @h{"a", "b"};\nsay $x;', '@h', 'a slice where one value is wanted: perl gives its last element; write the element, $h{...}')
r('slice-blank-before-the-brace', 'perl takes the blank: 12.', H + 'say @h {"a", "b"};', '{"a"', "a blank between @h and '{': a slice of a hash is written @h{...}")
r('slice-of-a-slice', 'perl does not compile it: syntax error.', H + 'say @h{"a", "b"}{"c"};', '{"c"', 'an element of an element: a hash of hashes or of arrays is not in the language yet')
r('slice-not-declared', 'perl does not compile it: Global symbol "%nope" requires explicit package name.', 'my @nope = (1);\nsay @nope{"a", "b"};', '@nope{', '%nope is not declared: my %nope')
# ---- a slice on the left (D100, T228)
r('slice-of-one-stored', 'perl takes it, and warns nothing: 9 2 3.', A + '@a[0] = (9);\nsay "@a";', '@a[0]', ONE('@a[...]', '$a[...]'))
r('hash-slice-of-one-stored', 'perl takes it, and warns nothing here: 9.', H + '@h{"a"} = (9);\nsay $h{a};', '@h{', ONE('@h{...}', '$h{...}'))
r('slice-added-to', 'perl takes it, and changes nothing.', A + '@a[0, 1] += 1;', '+=', "'+=' on a slice: a slice is assigned with =")
r('hash-slice-joined-to', 'perl takes it, and prints nothing.', H + '@h{"a", "b"} .= "x";', '.=', "'.=' on a slice: a slice is assigned with =")
r('slice-among-targets', 'perl takes it: 7 8 3. One target, here (D100).', A + '(@a[0, 1], my $z) = (7, 8, 9);\nsay "@a";', '@a[0', 'a target of a list assignment is a variable, an element, undef, or, last, an array or a hash')
r('slice-assignment-as-a-value', 'perl gives the count of the right side: 3 (D78).', A + 'my $n = (@a[0, 1] = (5, 6, 7));\nsay $n;', '= (5', 'an assignment of a list is a statement: perl gives the count of its right side as its value (D78)')
r('slice-index-changes-what-the-right-names', 'perl reads the element after the index has stored to it: 9 9 7.', A + '@a[0, ($a[1] = 9) - 7] = ($a[1], 7);\nsay "@a";', '- 7', 'a later part of this assignment can change @a, which an earlier part names: perl reads it after the change; take the value into a my first')
r('slice-key-changes-what-the-right-reads', 'perl: 5.', H + '@h{"x", delete($h{a})} = ($h{a}, 2);\nsay scalar(%h);', 'delete', 'a later part of this assignment can change %h, which an earlier part names: perl reads it after the change; take the value into a my first')
r('slice-stored-with-a-leading-zero', 'octal, to perl: the index 8, and an array of nine.', A + '@a[010, 1] = (1, 2);\nsay scalar(@a);', '010', '010 starts with a zero: perl reads that as octal, which the language writes 0o17')
# ---- delete of a slice
r('delete-of-a-slice-for-one-value', 'perl gives the last value it deleted: 2.', H + 'my $x = delete @h{"a", "b"};\nsay $x;', 'delete', 'delete of a slice where one value is wanted: perl gives the last value it deleted; delete the element, or assign the list to an array')
r('delete-of-a-slice-of-one', 'perl warns: Scalar value @h{"a"} better written as $h{"a"}.', H + 'delete @h{"a"};', '@h', ONE('@h{...}', '$h{...}'))
r('delete-of-a-slice-before-a-plus', 'perl dies: delete argument is not a HASH or ARRAY element or slice.', H + 'my @d = (delete @h{"a", "b"} + 1);', 'delete', "delete @h{...} before '+': perl reads on for delete's argument, or does not compile it; write delete(...)")
r('exists-of-a-slice', 'perl dies: exists argument is not a HASH or ARRAY element or a subroutine.', H + 'say exists @h{"a", "b"} ? 1 : 0;', '@h', "exists takes an element of a hash, found '@h': exists $h{...}")
r('delete-of-a-slice-after-what-names-the-hash', 'perl: 1213.', H + 'my @l = (@h{"a", "b"}, delete @h{"a", "c"});\nsay @l;', 'delete', 'a later part of this list can change %h, which an earlier part names: perl reads it after the change; take the value into a my first')
r('delete-of-a-slice-whose-keys-change', 'perl reads the first key after the second has changed it: b is deleted twice, and a stays.', H + 'my $i = "a";\nmy @d = delete @h{$i, ($i = "b")};\nsay "@d", scalar(%h);', '= "b"', 'a later part of delete can change $i, which an earlier part names: perl reads it after the change; take the value into a my first')
r('change-in-the-keys-of-a-delete', 'perl reads the element after the store in the keys: y 1 2.', H + 'my %g = (x => 1, y => 2);\nmy @l = ($h{a}, delete @g{"x", ($h{a} = "y")});\nsay "@l";', 'delete', 'a later part of this list can change %h, which an earlier part names: perl reads it after the change; take the value into a my first')
# ---- a hash as a parameter
LAST = lambda p: f'{p} takes every argument that is left, so it is the last parameter: perl refuses one after it'
r('parameter-not-last', 'perl does not compile it: Slurpy parameter not last.', 'sub f(%o, $x) { return 1 }', ', $x', LAST('%o'))
r('parameter-after-an-array', 'perl does not compile it: Multiple slurpy parameters not allowed.', 'sub f(@r, %o) { return 1 }', ', %o', LAST('@r'))
r('parameter-with-a-default', 'perl does not compile it: A slurpy parameter may not have a default value.', 'sub f(%o = (a => 1)) { return 1 }', '= (', 'a slurpy parameter has no default: perl refuses one')
r('parameter-twice', 'perl warns: "my" variable %o masks earlier declaration in same scope.', 'sub f(%o) { my %o = (a => 1); return scalar(%o) }\nsay f();', 'my %o', 'my %o again in one scope: perl warns that it masks the first')
r('parameter-changed-after-it-is-named', 'perl: 5.', 'sub f(%o) { my @l = (%o, delete $o{a}); return scalar(@l) }\nsay f(a => 1, b => 2);', 'delete', 'a later part of this list can change %o, which an earlier part names: perl reads it after the change; take the value into a my first')
# ---- in a string (D99, T227)
KEY = 'in a string a key is a word or a scalar variable, hard against its braces (D99): take the key into a my first'
r('string-key-with-blanks', 'perl takes the blanks: 1.', H + 'say "$h{ a }";', ' a }', KEY)
r('string-key-in-quotes', 'perl takes the quotes: 1.', H + "say \"$h{'a'}\";", "'a'", KEY)
r('string-key-a-number', 'perl takes it for the key 1, which is not there, and warns.', H + 'say "$h{1}";', '1}', KEY)
r('string-key-an-expression', 'perl runs it: 1.', H + 'my $k = "a";\nsay "$h{$k . q()}";', ' . q', KEY)
r('string-key-an-element', 'perl runs it: 2.', H + 'my @k = ("b");\nsay "$h{$k[0]}";', '[0]}', KEY)
r('string-key-not-closed', 'perl does not compile it: Missing right curly or square bracket.', H + 'say "$h{a";', 'a"', KEY)
DEEPER = lambda sh: f"'{{' hard after {sh} in a string: an element of what that holds, to perl, and references are not in the language yet (step 13); write {sh}\\{{"
r('string-element-of-an-element', "perl dies: Can't use string (\"1\") as a HASH ref (T227).", H + 'say "$h{a}{b}";', '{b}', DEEPER('$h{a}'))
r('string-index-of-an-element', "perl dies: Can't use string (\"1\") as an ARRAY ref (T227).", H + 'say "$h{a}[0]";', '[0]', "'[' hard after $h{a} in a string: another index, to perl; write $h{a}\\[")
r('string-arrow-after-an-element', "perl dies: Can't use string (\"1\") as an ARRAY ref (T227).", H + 'say "$h{a}->[0]";', '->[', "'->[' hard after $h{a} in a string: a dereference, to perl, and references are not in the language yet (step 13); write $h{a}\\->[")
r('string-slice', "perl joins the slice: 1 2. Not in a string (D99).", H + "say \"@h{'a','b'}\";", "{'a'", "'{' hard after @h in a string: a slice of a hash, to perl, which is not in a string (D99): join it first; or write @{h}{ or @h\\{")
r('string-element-not-declared', 'perl does not compile it: Global symbol "%nope" requires explicit package name.', 'my $nope = 1;\nsay "$nope{a}";', '$nope{', '%nope is not declared: my %nope')
r('string-key-not-declared', 'perl does not compile it: Global symbol "$k" requires explicit package name.', H + 'say "$h{$k}";', '$k', '$k is not declared: my $k; in a string, \\$ is the character, and ${name} ends a name sooner')
# ---- T230, for a hash's element in a string
r('key-changes-what-a-string-with-an-element-reads', 'perl: 1!. Refused a little more widely than it has to be (T230).', H + 'my $i = "a";\n$h{$i = "b"} = "$h{$i}!";\nsay $h{b};', '= "b"', 'the key changes $i, which the concatenation on the right reads: perl joins its pieces as it stores, after the key is worked out; take the string into a my first')

def write(first):
    n = first
    for name, why, body, at, message, nth in T:
        program = f'# kind: refused\n# {why}\nuse v5.42;\n{body}\n'
        path = f't/{n}-hash-{name}'
        open(path + '.pl', 'w', encoding='utf-8').write(program)
        k = program.index('use v5.42;')
        for _ in range(nth):
            k = program.index(at, k + 1)
        line = program.count('\n', 0, k) + 1
        col = len(program[program.rfind('\n', 0, k) + 1:k]) + 1
        open(path + '.expected', 'w', encoding='utf-8').write(f'{path}.pl:{line}:{col}: {message}\nexit: 1\n')
        n += 1
    print(n - first, 'tests,', first, 'to', n - 1)

write(int(sys.argv[1]))
