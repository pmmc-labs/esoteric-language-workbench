#!/usr/bin/env python3
# Writes step 11a's refusal tests from a table written by hand: the program,
# the text the message points at (its column is counted here, from the
# program's own text), and the message. Nothing here asks the compiler.
import os, sys
T = []
def r(name, why, body, at, message, nth=1, head=''):
    T.append((name, why, body, at, message, nth, head))

BARE = "'$' in a double-quoted string begins a variable, and no name is hard against it: write \\$ for the character"
BAREAT = "'@' in a double-quoted string begins an array, and no name is hard against it: write \\@ for the character"
INDEX = 'in a string an index is a whole number or a scalar variable (D91): take the index into a my first'
REF = lambda s: f'{s} in a string takes a reference, and references are not in the language yet (step 13)'
A = 'my @a = (1, 2, 3);\n'
X = 'my $x = 3;\n'

# ---- a `$` or an `@` that begins no shape (D92, T200, T204)
r('dollar-and-a-blank', 'perl reads `$b`, with the blank: a 7 (T200).', 'my $b = 7;\nsay "a $ b";', '$ b', BARE)
r('dollar-at-the-end', 'perl does not compile it: Final $ should be \\$ or $name (T200).', 'say "cost $";', '$"', BARE)
r('dollar-and-a-digit', "perl's own $1, undef and a warning.", 'say "$1";', '$1', BARE)
r('dollar-dollar', 'the process id (T34).', 'say "cost: $$";', '$$', BARE)
r('dollar-minus', "perl's own $-: a0b, in silence (T204).", 'say "a$-b";', '$-', BARE)
r('dollar-and-a-new-line', 'perl reads `$x`, over the end of the line (T200).', X + 'say "$\nx";', '$\n', BARE)
r('dollar-backslash', "perl's own $\\, indexed as a hash (T204).", X + 'say "$\\{x}";', '$\\', BARE)
r('at-and-a-blank', 'text to perl, in silence; refused all the same (D92).', 'say "a @ b";', '@ b', BAREAT)
r('at-at-the-end', 'text to perl; refused all the same (D92).', 'say "a@";', '@"', BAREAT)
r('at-minus', "perl's own @-: empty, in silence (T204).", 'say "[@-]";', '@-', BAREAT)
r('at-and-a-digit', "perl's own @1: empty, in silence (T204).", 'say "[@1]";', '@1', BAREAT)
r('at-at', 'text to perl; refused all the same (D92).', 'say "@@";', '@@', BAREAT)
r('at-underscore', "perl's own @_: empty, in silence (T204).", 'say "[@_]";', '@_', '@_ is not in the language: a sub has a signature (D17)')
r('element-of-underscore', 'an element of @_, to perl (T210).', A + 'for (@a) { say "$_[0]"; }', '$_[0]', "$_[ is an element of perl's own @_ or %_, which are not in the language")
r('last-index-of-nothing', 'perl does not compile it.', 'say "$# a";', '$# a', "after '$#' in a string comes an array's name, or one in braces: write \\$ for the character")
# ---- braces (T200, T201)
BR = lambda s: f'in a string a name in braces is hard against both of them: {s}'
r('blanks-in-braces', 'perl takes the blanks: 3 (T200).', X + 'say "${ x }";', '${ x', BR('${name}'))
r('brace-that-does-not-close', 'perl does not compile it.', X + 'say "${x";', '${x', BR('${name}'))
r('array-blanks-in-braces', 'perl takes the blanks: 1 2 3.', A + 'say "@{ a }";', '@{ a', BR('@{name}'))
r('last-index-blanks-in-braces', 'perl takes the blanks: 2.', A + 'say "$#{ a }";', '$#{ a', BR('$#{name}'))
r('index-in-braces', 'perl warns: Ambiguous use of ${a[...]} resolved to $a[...] (T201).', A + 'say "${a[1]}";', '${a', '${a[...]} in a string: perl warns that it is ambiguous; write $a[...]')
r('slice-in-braces', 'perl warns: Ambiguous use of @{a[...]} resolved to @a[...] (T201).', A + 'say "@{a[0,1]}";', '@{a', '@{a[...]} in a string: perl warns that it is ambiguous; write @a[...]')
r('reference-to-a-value', 'perl prints 4.', X + 'say "${\\ ($x + 1)}";', '${\\', REF('${\\'))
r('array-of-a-list', 'perl prints 4.', X + 'say "@{[ $x + 1 ]}";', '@{[', REF('@{['))
r('scalar-dereference', 'perl dies: not a SCALAR reference.', X + 'say "$$x";', '$$x', REF('$$'))
r('array-dereference', 'perl dies: not an ARRAY reference.', X + 'say "@$x";', '@$x', REF('@$'))
r('braced-dereference', 'perl dies: not a SCALAR reference.', X + 'say "${$x}";', '${$', REF('${$'))
r('braced-array-dereference', 'perl dies: not an ARRAY reference.', X + 'say "@{$x}";', '@{$', REF('@{$'))
# ---- what follows a shape (D92; T199, T203, T205)
PKG = lambda sh, alt: f"'::' hard after {sh} in a string: perl reads a variable of another package; write {alt + ':: or ' if alt else ''}{sh}\\::"
HASH = lambda sh, alt: f"'{{' hard after {sh} in a string: a hash's, to perl, and a hash in a string is not in the language yet (step 12b); write {alt + '{ or ' if alt else ''}{sh}\\{{"
AGAIN = lambda sh: f"'[' hard after {sh} in a string: another index, to perl; write {sh}\\["
ARROW = lambda sh, c: f"'->{c}' hard after {sh} in a string: a dereference, to perl, and references are not in the language yet (step 13); write {sh}\\->{c}"
r('package-after-a-name', 'perl reads $x::y, undef and a warning (T199).', X + 'say "$x::y";', '::', PKG('$x', '${x}'))
r('package-after-an-array', 'perl reads @a::b, empty.', A + 'say "@a::b";', '::', PKG('@a', '@{a}'))
r('package-after-a-last-index', 'perl prints -1, in silence: the last index of @a:: (T199).', A + 'say "$#a::";', '::', PKG('$#a', '$#{a}'))
r('package-after-an-element', 'text to perl; refused all the same (D92).', A + 'say "$a[0]::x";', '::', PKG('$a[0]', ''))
r('hash-element', 'perl does not compile it: %x is not declared (T203).', X + 'say "$x{a}";', '{a', HASH('$x', '${x}'))
r('hash-slice', 'perl does not compile it: %a is not declared.', A + 'say "@a{0}";', '{0', HASH('@a', '@{a}'))
r('hash-after-an-element', 'perl dies: not a HASH reference (T203).', A + 'say "$a[0]{a}";', '{a', HASH('$a[0]', ''))
r('hash-after-a-last-index', 'perl does not compile it.', A + 'say "$#a{";', '{"', HASH('$#a', '$#{a}'))
r('element-of-an-element', 'perl dies: not an ARRAY reference (T203).', A + 'say "$a[0][0]";', '[0]', AGAIN('$a[0]'), nth=2)
r('index-after-a-slice', 'perl does not compile it (T203).', A + 'say "@a[0, 1][0]";', '[0]', AGAIN('@a[0, 1]'))
r('index-after-a-last-index', 'perl does not compile it (T203).', A + 'say "$#a[0]";', '[0]', AGAIN('$#a'))
r('arrow-and-an-index', 'perl dies: not an ARRAY reference (T203).', X + 'say "$x->[0]";', '->', ARROW('$x', '['))
r('arrow-and-a-key', 'perl dies: not a HASH reference (T203).', X + 'say "$x->{a}";', '->', ARROW('$x', '{'))
r('arrow-and-an-array', 'perl dies: not an ARRAY reference (T203).', X + 'say "$x->@*";', '->', ARROW('$x', '@'))
r('arrow-and-a-scalar', 'perl dies: not a SCALAR reference (T203).', X + 'say "$x->$*";', '->', ARROW('$x', '$'))
r('arrow-after-an-element', 'perl dies: not an ARRAY reference (T203).', A + 'say "$a[0]->[0]";', '->', ARROW('$a[0]', '['))
r('arrow-after-an-array', "perl dies: Can't use an array as a reference (T203).", A + 'say "@a->[0]";', '->', ARROW('@a', '['))
r('letter-past-ascii-after-a-name', 'perl reads the name $x and an e-acute, which is not declared (T205).', 'my $x = "e";\nsay "$xé";', 'é', "a character past ASCII (U+00E9) hard after $x in a string: perl takes a letter, a digit or a mark there into the name; write ${x}",
  head="use utf8;\nuse open ':std', ':encoding(UTF-8)';\n")
r('arrow-past-ascii-after-a-name', 'text to perl: e and the arrow; refused all the same (D95).', 'my $x = "e";\nsay "$x→";', '→', "a character past ASCII (U+2192) hard after $x in a string: perl takes a letter, a digit or a mark there into the name; write ${x}",
  head="use utf8;\nuse open ':std', ':encoding(UTF-8)';\n")
r('letter-past-ascii-after-an-array', 'perl reads the name @a and an e-acute, which is not declared.', A + 'say "@aé";', 'é', "a character past ASCII (U+00E9) hard after @a in a string: perl takes a letter, a digit or a mark there into the name; write @{a}",
  head="use utf8;\nuse open ':std', ':encoding(UTF-8)';\n")
# ---- the index (D91; T197, T202, T211)
I = A + 'my $i = 1;\n'
r('index-arithmetic', 'perl prints 3.', I + 'say "$a[$i+1]";', '+', INDEX)
r('index-arithmetic-with-blanks', 'perl prints 3.', I + 'say "$a[$i + 1]";', '+ 1', INDEX)
r('index-last-index', 'perl prints 3.', A + 'say "$a[$#a]";', '$#', INDEX)
r('index-fraction', 'perl prints 2: the index cut down (T202).', A + 'say "$a[1.9]";', '.9', INDEX)
r('index-exponent', 'perl prints 2 (T202).', A + 'say "$a[1e0]";', 'e0', INDEX)
r('index-hex', 'perl prints 2 (T202).', A + 'say "$a[0x1]";', 'x1', INDEX)
r('index-underscore', 'perl reads 10 (T202).', A + 'say "$a[1_0]";', '_0', INDEX)
r('index-quoted', 'perl prints 2 (T202).', A + "say \"$a['1']\";", "'1", INDEX)
r('index-call', 'perl prints 2.', A + 'sub f($n) { return $n; }\nsay "$a[f(1)]";', 'f(1', INDEX)
r('index-two', 'perl warns: Multidimensional syntax $a[1,2] not supported (T202).', A + 'say "$a[1,2]";', ',2', INDEX)
r('index-element', 'perl prints 2.', A + 'say "$a[$a[0]]";', '[0]', INDEX)
r('index-minus-a-scalar', 'perl prints 3.', I + 'say "$a[-$i]";', '-$', INDEX)
r('index-minus-and-a-blank', 'perl prints 3.', A + 'say "$a[- 1]";', '- 1', INDEX)
r('index-none', 'perl does not compile it.', A + 'say "$a[]";', ']', INDEX)
r('index-over-two-lines', 'perl prints 2 (T202).', A + 'say "$a[\n1]";', '\n1', INDEX)
r('index-assignment', 'perl prints 12: the string reads $i late (T197).', I + 'say "$i$a[$i = 2]";', '= 2', INDEX)
r('index-step', 'perl prints 1 2 2 (T197).', I + '$i = 0;\nsay "$i $a[$i++] $i";', '++', INDEX)
r('slice-by-an-array', 'perl prints 1 3.', A + 'my @w = (0, 2);\nsay "@a[@w]";', '@w]', INDEX)
r('slice-three-dots', 'perl prints 1 2.', A + 'say "@a[0 ... 1]";', '. 1', INDEX)
r('slice-range-with-no-end', 'perl does not compile it.', A + 'say "@a[0 .. ]";', ']', INDEX)
r('slice-two-commas', 'perl prints 1 2.', A + 'say "@a[0,,1]";', ',1', INDEX)
OCT = lambda d: f'{d} in an index in a string: a leading zero makes it octal, to perl; write the number without it'
r('index-leading-zero', 'perl prints 9: 010 is octal (T211).', 'my @a = (1 .. 20);\nsay "$a[010]";', '010', OCT('010'))
r('index-leading-zero-and-an-eight', 'perl does not compile it: Illegal octal digit (T211).', 'my @a = (1 .. 20);\nsay "$a[08]";', '08', OCT('08'))
r('index-negative-leading-zero', 'perl prints 13: -010 is -8 (T211).', 'my @a = (1 .. 20);\nsay "$a[-010]";', '010', OCT('010'))
r('slice-leading-zero', 'perl prints 8 9 (T211).', 'my @a = (0 .. 20);\nsay "@a[010, 011]";', '010', OCT('010'))
BIG = 'an index of 9223372036854775808 or more in a string: perl wraps it round to the other end of the array'
r('index-too-large', 'perl prints 3: the last element (T211).', A + 'say "$a[18446744073709551615]";', '1844', BIG)
r('index-at-two-to-the-63', 'perl warns: an element at the smallest integer (T211).', A + 'say "$a[9223372036854775808]";', '9223', BIG)
OPEN = "an index in a string that does not close: write \\[ for the character"
r('index-that-does-not-close', 'perl does not compile it.', A + 'say "$a[0";', '[0', OPEN)
r('slice-that-does-not-close', 'perl does not compile it.', A + 'say "@a[0, 1";', '[0', OPEN)
r('index-that-opens-and-ends', 'perl does not compile it.', A + 'say "$a[";', '["', OPEN)
r('slice-that-ends-after-a-comma', 'perl does not compile it.', A + 'say "@a[0,";', '[0', OPEN)
r('slice-of-one-index', 'perl warns: Scalar value @a[0] better written as $a[0] (T206).', A + 'say "@a[0]";', '@a[', '@a[...] with one index: perl warns that it is better written $a[...]')
r('slice-of-one-scalar', 'perl warns: Scalar value @a[...] better written as $a[...] (T206).', I + 'say "@a[$i]";', '@a[', '@a[...] with one index: perl warns that it is better written $a[...]')
# ---- what is not declared
SC = lambda n: f"${n} is not declared: my ${n}; in a string, \\$ is the character, and ${{name}} ends a name sooner"
AR = lambda n: f"@{n} is not declared: my @{n}; in a string, \\@ is the character"
EL = lambda n: f"@{n} is not declared: my @{n}; in a string ${n}[ is an element of @{n}: for the scalar and a bracket, ${{{n}}}[ or ${n}\\["
r('name-runs-on', 'perl reads the name $x_y, which is not declared (T205).', X + 'say "$x_y";', '$x_y', SC('x_y'))
r('name-runs-into-digits', 'perl reads the name $x1.', X + 'say "$x1";', '$x1', SC('x1'))
r('email-address', 'perl does not compile it: Possible unintended interpolation of @example (T204).', 'say "user@example.com";', '@example', AR('example'))
r('scalar-for-an-array', 'perl does not compile it.', X + 'say "@x";', '@x', AR('x'))
r('array-for-a-scalar', 'perl does not compile it.', A + 'say "$a";', '$a', "$a outside the block of a sort: $a and $b are the two values a sort gives its block, and are seen there alone")
r('element-with-no-array', 'perl does not compile it: @x is not declared (T201).', X + 'say "$x[1]";', '$x[', EL('x'))
r('last-index-with-no-array', 'perl does not compile it.', X + 'say "$#x";', '$#x', AR('x'))
r('it-outside-a-block', 'perl prints an empty line and warns.', 'say "<$_>";', '$_', '$_ outside the block of a for, a map or a grep: it is the value they give their block, and is seen there alone (D17)')
r('own-variable-in-its-my', 'perl does not compile it: $s is not declared yet.', 'my $s = "a$s";', '$s"', SC('s'))
# ---- D57, T198, T212: the assignment perl loses
LOST = lambda n: f"'.=' of an assignment of an interpolated string: perl makes one operation of them and never assigns ${n}; make the assignment a statement of its own"
TU = 'my $t = "t";\nmy $u = "u";\nmy $x = "a";\nmy $z = "z";\n'
r('lost-assignment', 'perl prints taz and then u: $u is never assigned (T198).', TU + '$t .= ($u = "$x$z");\nsay $t;\nsay $u;', '= "$', LOST('u'))
r('lost-assignment-of-text-and-a-scalar', 'perl prints taa and then u (T198).', TU + '$t .= ($u = "a$x");\nsay $t;\nsay $u;', '= "a$', LOST('u'))
r('lost-assignment-of-three-pieces', 'perl prints taza and then u (T212).', TU + '$t .= ($u = "$x$z$x");\nsay $t;\nsay $u;', '= "$', LOST('u'))
r('lost-assignment-behind-a-plus', 'perl prints taz and then u (T198).', TU + '$t .= +($u = "$x$z");\nsay $t;\nsay $u;', '= "$', LOST('u'))
r('lost-assignment-behind-a-test', 'perl prints taz and then u (T212).', TU + '$t .= ($u = (1 ? "$x$z" : 0));\nsay $t;\nsay $u;', '= (1', LOST('u'))
r('lost-assignment-of-an-array-and-text', 'perl prints t1 2 3- and then u (T198).', A + 'my $t = "t";\nmy $u = "u";\n$t .= ($u = "@a-");\nsay $t;\nsay $u;', '= "@', LOST('u'))
# ---- what was refused of a string before, and is of this one
r('map-block-begins-with-a-string-and-a-comma', 'perl does not compile it: a hash, to perl (T175, T210).', A + 'my @b = map { "$_", 1 } @a;', '"$_"', '"$_" and a comma first in map\'s block: perl takes the block for an anonymous hash, and does not compile it; put the list in brackets')
r('repeat-hard-against-a-number', 'perl prints a3a3; refused as of any string (T57).', X + 'say "a$x" x2;', 'x2', 'x2: the repetition operator is a word of its own: write x 2')
r('string-as-a-statement', 'perl warns: Useless use of string in void context.', X + '"a$x";', '"a', None)
r('assignment-to-a-string', "perl does not compile it: Can't modify string in scalar assignment.", X + '"$x" = 5;', '= 5', None)
r('blank-after-a-brace', 'perl takes the blank: 3 (T200).', X + 'say "${ x}";', '${ x', BR('${name}'))
r('blank-before-a-brace', 'perl takes the blank: 3 (T200).', X + 'say "${x }";', '${x', BR('${name}'))

BY_HAND = {
    'string-as-a-statement': ('"a', 'this statement only has a value, and nothing is done with it: perl warns that it is useless'),
    'assignment-to-a-string': ('= 5', "the left side of '=' is a variable, an element, an array, a hash, or a list of them in brackets"),
}

def write(first):
    n = first
    for name, why, body, at, message, nth, head in T:
        program = f'# kind: refused\n# {why}\nuse v5.42;\n{head}{body}\n'
        path = f't/{n}-interpolate-{name}'
        open(path + '.pl', 'w', encoding='utf-8').write(program)
        if message is not None:
            k = program.index('use v5.42;')
            for _ in range(nth):
                k = program.index(at, k + 1)
            line = program.count('\n', 0, k) + 1
            col = len(program[program.rfind('\n', 0, k) + 1:k]) + 1
            open(path + '.expected', 'w', encoding='utf-8').write(f'{path}.pl:{line}:{col}: {message}\nexit: 1\n')
        else:
            at_, text_ = BY_HAND[name]
            k = program.index(at_, program.index('use v5.42;'))
            line = program.count('\n', 0, k) + 1
            col = len(program[program.rfind('\n', 0, k) + 1:k]) + 1
            open(path + '.expected', 'w', encoding='utf-8').write(f'{path}.pl:{line}:{col}: {text_}\nexit: 1\n')
        n += 1
    print(n - first, 'tests,', first, 'to', n - 1)

write(int(sys.argv[1]))
