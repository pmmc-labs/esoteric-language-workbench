#!/usr/bin/env python3
# Writes step 13a's refusal tests from a table written by hand: the program,
# the text the message points at (its column is counted here, from the
# program's own text), and the message. Nothing here asks the compiler.
# What perl does with each is in its comment, from perl 5.42 run plain
# (`python3 docs/briefs/step13a-refusals.py --perl` prints each again).
#
#     python3 docs/briefs/step13a-refusals.py 1900
import subprocess
import sys
T = []
def r(name, why, body, at, message, nth=1):
    T.append((name, why, body, at, message, nth))

A = 'my @a = (1, 2, 3);\n'
R = 'my $r = [1, 2];\n'
H = 'my %h = (a => 1);\n'

# ---- cut by D108: a dereference without braces, and what the arrow says
r('deref-no-braces-element', "perl runs it: '1\\n'.", R + 'say $$r[0];', '$$r', "$$ before a name is cut (D108): an element through a reference is written $r->[...] or $r->{...}, and the scalar $r->$* (step 13c)")
r('deref-no-braces-array', "perl runs it, and says nothing.", R + 'my @c = @$r;', '@$r', "@$ before a name is cut (D108): an array through a reference is written $r->@* (step 13b)")
r('deref-no-braces-hash', "perl runs it, and says nothing.", 'my $h = {a => 1};\nmy %c = %$h;', '%$h', "%$ before a name is cut (D108): a hash through a reference is written $r->%* (step 13b)")
r('deref-no-braces-last-index', "perl runs it: '1\\n'.", R + 'say $#$r;', '$#$r', "$#$ before a name is cut (D108): the last index through a reference is written $r->$#* (step 13b)")
r('deref-braces-scalar', "perl runs it: '1\\n'.", R + 'say ${$r}[0];', '${', "${ ... }: a scalar through a reference is not in the language yet (step 13c); a variable is written $name")
r('deref-braces-array', "perl runs it, and says nothing.", R + 'my @c = @{$r};', '@{', "@{ ... }: an array through a reference is not in the language yet (step 13b)")
r('deref-braces-hash', "perl runs it, and says nothing.", 'my $h = {a => 1};\nmy %c = %{$h};', '%{', "%{ ... }: a hash through a reference is not in the language yet (step 13b)")
r('deref-braces-last-index', "perl runs it: '1\\n'.", R + 'say $#{$r};', '$#{', "$#{ ... }: the last index through a reference is not in the language yet (step 13b)")
r('postfix-array', "perl runs it, and says nothing.", R + 'my @c = $r->@*;', '->', "->@*: the whole container through a reference is not in the language yet (step 13b)")
r('postfix-hash', "perl runs it, and says nothing.", 'my $h = {a => 1};\nmy %c = $h->%*;', '->', "->%*: the whole container through a reference is not in the language yet (step 13b)")
r('postfix-last-index', "perl runs it: '1\\n'.", R + 'say $r->$#*;', '->', "->$#*: the whole container through a reference is not in the language yet (step 13b)")
r('postfix-slice', "perl runs it, and says nothing.", R + 'my @c = $r->@[0, 1];', '->', "->@[...: a slice through a reference is not in the language yet (step 13b)")
r('postfix-hash-slice', "perl runs it, and says nothing.", 'my $h = {a => 1};\nmy @c = $h->@{"a"};', '->', "->@{...: a slice through a reference is not in the language yet (step 13b)")
r('postfix-key-value-slice', "perl runs it, and says nothing.", 'my $h = {a => 1};\nmy %c = $h->%{"a"};', '->', "->%{...: a slice of keys and values is cut (D108)")
r('postfix-scalar', "perl dies: Not a SCALAR reference.", R + 'say $r->$*;', '->', "->$*: a scalar through a reference is not in the language yet (step 13c)")
r('method-call', "perl dies: Can't call method 'size' on unblessed reference.", R + 'say $r->size;', '->', "'->' and a name: a method call, and classes are not in the language yet (step 17)")
r('code-call', "perl dies: Not a CODE reference.", R + 'say $r->(1);', '->', "->(...): a call through a reference is not in the language yet (step 14)")
r('arrow-and-a-blank', "perl runs it: '1\\n'.", R + 'say $r-> [0];', '->', "after '->' comes '[' or '{', hard against it: $r->[0], $r->{k}")
# ---- \ (D110)
r('reference-to-a-scalar', "perl runs it, and says nothing.", 'my $x = 1;\nmy $s = \\$x;', '\\$x', '\\$x: a reference to a scalar is not in the language yet (step 13c)')
r('reference-to-an-element', "perl runs it, and says nothing.", A + 'my $s = \\$a[0];', '\\$a', '\\ before an element: a reference to an element is cut (D110); take a reference to the array or the hash')
r('reference-to-a-key', "perl runs it, and says nothing.", H + 'my $s = \\$h{a};', '\\$h', '\\ before an element: a reference to an element is cut (D110); take a reference to the array or the hash')
r('reference-to-a-slice', "perl runs it, and says nothing.", A + 'my @s = \\@a[0, 1];', '\\@a', '\\ before a slice: perl makes a list of a reference to each element, which is cut (D110)')
r('reference-to-a-list', "perl runs it, and says nothing.", 'my ($x, $y) = (1, 2);\nmy @s = \\($x, $y);', '\\(', '\\ before a list: perl makes a list of a reference to each, which is cut (D110)')
r('reference-to-a-my', "perl runs it, and says nothing.", 'my $s = \\my @a;', '\\my', "\\ before 'my': \\ takes a named array or a named hash, \\@a or \\%h (D110)")
r('reference-to-a-value', "perl runs it, and says nothing.", 'my $s = \\5;', '\\5', '\\ before 5: \\ takes a named array or a named hash, \\@a or \\%h (D110)')
# ---- ref (T242)
r('ref-of-a-concatenation', "perl runs it: '\\n'.", R + 'say ref $r . "x";', 'ref', "ref before '.': perl takes all of it for ref's argument, which is then no reference; write ref(...) . ...")
r('ref-alone', "perl runs it: '\\n'.", 'for my $x ([1]) {\n    say ref;\n}', 'ref', 'ref needs an argument')
# ---- { and [ (D113, T243, T254)
r('brace-first-after-say', "perl runs it: '1\\n'.", 'say {a => 1}->{a};', '{a', "'{' first after say: perl takes it for a block that gives a file handle; write +{ ... } for a new hash")
r('brace-first-in-say-brackets', "perl does not compile it: syntax error near '}->'.", 'my $k = "a";\nsay({ $k => 1 }->{a});', '{ $k', "'{' first in say(...): perl does not compile it; write +{ ... } for a new hash")
r('brace-first-in-print-brackets', "perl runs it: '1'.", 'print({ a => 1 }->{a});', '{ a', "'{' first in print(...): perl does not compile it; write +{ ... } for a new hash")
r('block-that-looks-like-a-hash', "perl runs it, and says nothing.", 'sub f($x) {\n    { $x, 1 }\n}', ', 1', "a comma after an assignment's right side: perl takes the assignment for the first item of a list; put the list in brackets")
r('block-word-and-a-comma', "perl runs it ('') and warns: Useless use of anonymous hash ({}) in void context.", '{ a => 1 }', '{ a', "a block that begins with a and a comma: perl guesses that it is a new hash; write +{ ... } for one, or put the list in brackets")
r('block-string-and-a-comma', "perl runs it ('') and warns: Useless use of anonymous hash ({}) in void context.", 'my $x = 1;\n{ "$x", 1 }', '{ "', 'a block that begins with "$x" and a comma: perl guesses that it is a new hash; write +{ ... } for one, or put the list in brackets')
r('block-number-and-a-comma', "perl runs it ('') and warns: Useless use of anonymous hash ({}) in void context.", '{ 1, 2 }', '{ 1', "a block that begins with 1 and a comma: perl guesses that it is a new hash; write +{ ... } for one, or put the list in brackets")
r('brace-first-in-a-map', "perl runs it, and says nothing.", 'my @l = map { { n => $_ } } (1, 2);', '{ n', "'{' first in map's block: an anonymous hash, to perl")
# ---- where an arrow may stand, and a subscript
r('arrow-after-a-number', "perl runs it ('\\n') and warns: Use of uninitialized value in say.", 'say 5->[0];', '->', "'->' after this: an arrow follows a scalar variable, an element, a call, [ ], { }, or brackets round one value")
r('arrow-after-an-array', "perl dies: Can't use an array as a reference.", A + 'say @a->[0];', '->', "'->' after this: an arrow follows a scalar variable, an element, a call, [ ], { }, or brackets round one value")
r('arrow-after-a-list', "perl dies: Can't use string ('2') as an ARRAY ref while 'strict refs' in use.", 'say((1, 2)->[0]);', '->', "'->' after this: an arrow follows a scalar variable, an element, a call, [ ], { }, or brackets round one value")
r('subscript-after-a-new-array', "perl does not compile it: syntax error near ']['.", 'my $x = [1, 2][0];', '[0', "expected ';', found '['")
r('subscript-after-a-slice', "perl runs it, and says nothing.", 'my $x = ([1, 2])[0][1];', '[1]', 'a subscript after a slice: take the element into a my first')
r('blank-between-subscripts', "perl runs it: '2\\n'.", 'my @a = ([1, 2]);\nsay $a[0] [1];', '[1]', 'a blank between two subscripts: perl takes it, and reads on; write them hard together, $a[0][1]')
r('blank-between-keys', "perl runs it: '3\\n'.", 'my %g = (x => {y => 3});\nsay $g{x} {y};', '{y', "a blank between a subscript and '{': perl takes it for another key; write them hard together, $h{a}{b}", nth=2)
r('no-key', "perl does not compile it: syntax error near '{}'.", 'my $h = {};\nsay $h->{};', '{}', '{} has no key: perl does not compile it', nth=2)
r('no-index', "perl does not compile it: syntax error near '[]'.", R + 'say $r->[];', '[]', '[] has no index: perl does not compile it')
r('comma-in-a-key', "perl does not compile it: Multidimensional hash lookup is disabled near '2}'.", 'my $h = {};\nsay $h->{1, 2};', ',', "a comma in a hash's key: perl joins the values into one key")
r('word-key-across-a-line', "perl does not compile it: Bareword 'a' not allowed while 'strict subs' in use.", 'my $h = {a => 1};\nsay $h->{\na};', '{', "a word alone in a hash's braces is on one line with them: across the end of a line perl does not make a string of every word; write the word in quotes", nth=2)
r('exists-through-an-array', "perl runs it: '1\\n'.", R + 'say exists $r->[0] ? 1 : 0;', '$r', "exists takes an element of a hash, found '$r': exists $h{...}", nth=2)
r('delete-through-a-call', "perl runs it, and says nothing.", 'sub f() {\n    return {};\n}\ndelete f()->{a};', 'f()', "delete takes an element of a hash, found 'f': delete $h{...}", nth=2)
r('increment-of-a-new-array', "perl does not compile it: Can't modify anonymous array ([]) in postincrement (++) near ']++'.", 'my $x = [1]++;', '++', "expected ';', found '++'")
r('index-a-string', "perl runs it ('1\\n') and warns: Argument 'x' isn't numeric in array element.", R + 'say $r->["x"];', '"x"', '"x" as an index is not a number: perl warns of it as it compiles')
# ---- in a string: step 13d
r('string-arrow', "perl runs it: '1\\n'.", R + 'say "$r->[0]";', '->[', "'->[' hard after $r in a string: a dereference, to perl, and a dereference in a string is not in the language yet (step 13d); write $r\\->[")
r('string-element-of-an-element', "perl runs it: '1\\n'.", 'my %g = (a => {b => 1});\nsay "$g{a}{b}";', '{b}', "'{' hard after $g{a} in a string: an element of what that holds, to perl, and an element through a reference in a string is not in the language yet (step 13d); write $g{a}\\{")
r('string-index-of-an-element', "perl runs it: '1\\n'.", 'my @g = ([1]);\nsay "$g[0][0]";', '[0]"', "'[' hard after $g[0] in a string: another index, to perl, and an element through a reference in a string is not in the language yet (step 13d); write $g[0]\\[")
r('string-braces', "perl runs it: '1 2\\n'.", R + 'say "@{$r}";', '@', '@{$ in a string takes a reference, and a reference in a string is not in the language yet (step 13d)')
# ---- D109: what references reach, in every walk
r('reach-list-store-after-read', "perl runs it: '55\\n'.", A + 'my $r = \\@a;\nsay $a[0], ($r->[0] = 5);', '= 5', "a later part of say's list can change what references reach, which an earlier part names: perl reads it after the change; take the value into a my first")
r('reach-list-named-array-changed', "perl runs it: '55\\n'.", A + 'my $r = \\@a;\nsay $r->[0], ($a[0] = 5);', '= 5', "a later part of say's list can change what references reach, which an earlier part names: perl reads it after the change; take the value into a my first")
r('reach-list-sub-stores', "perl runs it: 'x1\\n'.", 'my $s = [9];\nsub f($t) {\n    $t->[0] = "x";\n    return 1;\n}\nsay $s->[0], f($s);', 'f($s)', "a later part of say's list can change what references reach, which an earlier part names: perl reads it after the change; take the value into a my first")
r('reach-concat-sub-stores', "perl runs it: 'x1\\n'.", 'my $s = [9];\nsub f($t) {\n    $t->[0] = "x";\n    return 1;\n}\nsay $s->[0] . f($s);', 'f($s)', "a later piece of a concatenation calls f, which can change what references reach, which an earlier piece reads: perl joins the pieces as one operation and reads each late; make the call a statement of its own")
r('reach-sum-sub-stores', "perl runs it: '2\\n'.", 'my $s = [9];\nsub f($t) {\n    $t->[0] = 1;\n    return 1;\n}\nsay $s->[0] + f($s);', 'f($s)', "a later part of '+' can change what references reach, which an earlier part names: perl reads it after the change; take the value into a my first")
r('reach-head-replaced', "perl runs it ('7\\n') and warns: Use of uninitialized value in say.", R + 'say $r->[0], ($r = [7, 8, 9])->[0];', '= [7', "a later part of say's list can change $r, which an earlier part names: perl reads it after the change; take the value into a my first")
r('reach-head-made', "perl runs it, and says nothing.", 'my $r;\nmy @l = ($r, ($r->[0] = 1));', '= 1', "a later part of this list can change $r, which an earlier part names: perl reads it after the change; take the value into a my first")
r('reach-head-made-by-a-sub', "perl runs it, and says nothing.", 'my $cfg;\nsub get() {\n    $cfg->{x} = 1;\n    return 0;\n}\nmy @l = ($cfg, get());', 'get()', "a later part of this list can change $cfg, which an earlier part names: perl reads it after the change; take the value into a my first", nth=2)
r('reach-element-made', "perl runs it, and says nothing.", 'my @a = (undef);\nmy @l = ($a[0], ($a[0][0] = 1));', '= 1', "a later part of this list can change @a, which an earlier part names: perl reads it after the change; take the value into a my first")
r('reach-made-what-the-right-took', "perl runs it, and says nothing.", 'my @a = (undef);\n$a[0][0] = $a[0];', '$a[0][0]', 'the store makes what it goes through, which the right side has already taken: perl takes it after it is made; take the value into a my first')
r('reach-made-in-a-list-assignment', "perl runs it, and says nothing.", 'my ($q, $x);\n($q->[0], $x) = ($q, 1);', '$q->', 'the store makes what $q holds, which the right side has already taken: perl takes it after it is made; take the value into a my first')
r('reach-loop-head-assigned', "perl dies: Use of freed value in iteration.", R + 'for my $x ($r->[0], $r->[1]) {\n    $r = [7];\n}', '= [7]', "this can change $r, which the list of the loop it is in names: perl's loop walks the variable itself; take the value into a my before the loop")
r('reach-loop-head-made', "perl runs it, and says nothing.", 'my $r;\nfor my $v ($r, 1) {\n    $r->{k} = 1;\n}', '= 1;', "this can change $r, which the list of the loop it is in names: perl's loop walks the variable itself; take the value into a my before the loop")
r('reach-map-head-assigned', "perl crashes (a segmentation fault).", R + 'my @l = map { $r = [7]; $_ } ($r->[0], $r->[1]);', '= [7]', "this can change $r, which the list of the map it is in names: perl's map walks the variable itself; take the value into a my before the map")
r('reach-index-concat', "perl runs it, and says nothing.", 'my $r = [];\nmy $i = 0;\n$r->[$i = 2] = $i . "v";', '= 2]', 'the index changes $i, which the concatenation on the right reads: perl joins its pieces as it stores, after the index is worked out; take the string into a my first')
r('reach-key-concat-deep', "perl runs it, and says nothing.", 'my %h;\nmy $k = "a";\n$h{x}{$k = "b"} = "$k!";', '= "b"', 'the key changes $k, which the concatenation on the right reads: perl joins its pieces as it stores, after the key is worked out; take the string into a my first')
r('reach-taken-hash-deleted', "perl runs it, and says nothing.", H + 'my $r = \\%h;\nmy @l = ($r->{a}, delete $h{a});', 'delete', 'a later part of this list can change what references reach, which an earlier part names: perl reads it after the change; take the value into a my first')
r('reach-operand-store', "perl runs it: '10\\n'.", R + 'my $s = $r;\nsay $r->[0] + ($s->[0] = 5);', '= 5', "a later part of '+' can change what references reach, which an earlier part names: perl reads it after the change; take the value into a my first")
r('reach-arguments', "perl runs it: '55\\n'.", R + 'sub f($x, $y) {\n    return $x . $y;\n}\nsay f($r->[0], ($r->[0] = 5));', '= 5)', "a later part of the arguments of f can change what references reach, which an earlier part names: perl reads it after the change; take the value into a my first")

def write(first):
    n = first
    for name, why, body, at, message, nth in T:
        program = f'# kind: refused\n# {why}\nuse v5.42;\n{body}\n'
        path = f't/{n}-ref-{name}'
        open(path + '.pl', 'w', encoding='utf-8').write(program)
        k = program.index('use v5.42;')
        for _ in range(nth):
            k = program.index(at, k + 1)
        line = program.count('\n', 0, k) + 1
        col = len(program[program.rfind('\n', 0, k) + 1:k]) + 1
        open(path + '.expected', 'w', encoding='utf-8').write(f'{path}.pl:{line}:{col}: {message}\nexit: 1\n')
        n += 1

if __name__ == '__main__':
    if sys.argv[1] == '--perl':
        import os
        for name, why, body, at, message, nth in T:
            r_ = subprocess.run([os.environ.get('CURLY_PERL', 'perl'), '-e', 'use v5.42;\n' + body], capture_output=True, text=True, timeout=10)
            print(f'{name}: exit {r_.returncode}; {r_.stdout!r}; {r_.stderr.strip()[:200]!r}')
    else:
        write(int(sys.argv[1]))
