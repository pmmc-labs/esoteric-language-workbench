#!/usr/bin/env python3
# Writes step 12a's refusal tests from a table written by hand: the program,
# the text the message points at (its column is counted here, from the
# program's own text), and the message. Nothing here asks the compiler.
# What perl does with each is in its comment, pasted from perl 5.42.
#
#     python3 docs/briefs/step12a-refusals.py 1550
import sys
T = []
def r(name, why, body, at, message, nth=1):
    T.append((name, why, body, at, message, nth))

H = 'my %h = (a => 1, b => 2, c => 3, d => 4);\n'
A = 'my @a = (1, 2, 3);\n'

# ---- a word that is a string, on one line (D102; T223, T224)
WORD = "a word alone in a hash's braces is on one line with them: across the end of a line perl does not make a string of every word; write the word in quotes"
FAT = lambda w: f"{w} and its '=>' are on one line: across the end of a line perl does not make a string of every word; write the word in quotes"
r('word-in-braces-across-a-line', 'perl reads the key 1, and warns of the undef it finds there (T223).', H + 'say $h{\n  true\n};', '{', WORD)
r('word-in-braces-before-a-comment', 'perl does not compile it: Bareword "a" not allowed.', H + 'say $h{a # the key\n};', '{', WORD)
r('fat-comma-on-the-next-line', 'perl reads a version string: the key A (T224).', 'my %g = (v65\n  => 1);\nsay join(",", sort keys %g);', 'v65', FAT('v65'))
r('fat-comma-after-a-comment', 'perl makes the string: a. One rule for every word (D102).', 'my %g = (a # the key\n  => 1);\nsay join(",", sort keys %g);', 'a #', FAT('a'))
r('minus-word-in-braces', 'the key -bar, to perl: 0.', H + 'say defined($h{-bar}) ? 1 : 0;', '-bar', "-bar alone in a hash's braces is the string -bar, to perl: write it in quotes")
r('minus-word-before-a-fat-comma', 'the key -bar, to perl: -bar,x.', 'my %g = (-bar => 1, x => 2);\nsay join(",", sort keys %g);', '-bar', "'-' before the word bar, which is a string here: perl makes one string of the two; write it in quotes")

# ---- the element
r('no-key', 'perl does not compile it: syntax error.', H + 'say $h{};', '{}', '$h{} has no key: perl does not compile it')
r('element-of-an-element', "perl dies: Can't use string (\"1\") as a HASH ref.", H + 'say $h{a}{b};', '{b', 'an element of an element: a hash of hashes or of arrays is not in the language yet')
r('index-of-an-element', "perl dies: Can't use string (\"1\") as an ARRAY ref.", H + 'say $h{a}[0];', '[0', 'an element of an element: a hash of hashes or of arrays is not in the language yet')
r('stored-through-an-element', 'perl makes a hash in the element, and a reference to it (step 13).', 'my %g;\n$g{x}{y} = 1;', '{y', 'an element of an element: a hash of hashes or of arrays is not in the language yet')
r('comma-in-a-key', 'perl 5.42 does not compile it: Multidimensional hash lookup is disabled.', H + 'say defined($h{1, 2}) ? 1 : 0;', ', 2', "a comma in a hash's key: perl joins the values into one key")
r('blank-before-the-brace', 'perl takes the blank: 1.', H + 'say $h {a};', '{a', "a blank between $h and '{': an element of a hash is written $h{...}")
r('not-declared', 'perl does not compile it: Global symbol "%nope" requires explicit package name.', 'say scalar(%nope);', '%nope', '%nope is not declared: my %nope')
r('element-not-declared', 'perl does not compile it: Global symbol "%nope" requires explicit package name.', 'my $nope = 1;\nmy @nope = (1);\nsay $nope{a};', '$nope{', '%nope is not declared: my %nope')
r('my-twice', 'perl warns: "my" variable %h masks earlier declaration in same scope.', H + 'my %h = (z => 1);\nsay scalar(%h);', 'my %h', 'my %h again in one scope: perl warns that it masks the first', 2)
r('underscore', 'perl does not compile it: Can\'t use global %_ in "my".', 'my %_ = (a => 1);', '%_', "%_ is perl's own, and not in the language")
r('key-value-slice', 'a slice of keys and values, to perl: 2.', H + 'my %g = %h{"a", "b"};\nsay scalar(%g);', '%h{', '%h{...} is a slice of keys and values, and not in the language')
r('of-a-reference', "perl dies: Can't use string (\"1\") as a HASH ref.", 'my $r = 1;\nsay %$r;', '%$', "'%' before a reference: references are not in the language yet (step 13)")
r('no-name', 'the hash %2, to perl, which is empty: an empty line.', 'say % 2;', '% 2', "after '%' comes a name: a letter or '_', then letters, digits and '_'")

# ---- exists, delete, keys, values (T220, T225)
ON = lambda shown, op, word: f"{shown} before '{op}': perl reads on for {word}'s argument, or does not compile it; write {word}(...)"
r('exists-before-a-plus', 'perl dies: exists argument is not a HASH or ARRAY element or a subroutine (T220).', H + 'say exists $h{a} + 1;', 'exists', ON('exists $h{...}', '+', 'exists'))
r('delete-before-a-dot', 'perl dies: delete argument is not a HASH or ARRAY element or slice (T220).', H + 'say delete $h{a} . "x";', 'delete', ON('delete $h{...}', '.', 'delete'))
r('keys-before-a-plus', 'perl does not compile it: Type of arg 1 to keys must be hash or array (T225).', H + 'say keys %h + 1;', 'keys', ON('keys %h', '+', 'keys'))
r('values-before-a-repeat', 'perl does not compile it: Type of arg 1 to values must be hash or array (T225).', H + 'say values %h x 2;', 'values', ON('values %h', 'x', 'values'))
r('keys-indexed', 'perl does not compile it: syntax error.', H + 'say keys(%h)[0];', '[0', "'[' after keys(...): perl does not compile it; bracket the whole, (keys(...))[...]")
r('exists-of-an-array-element', "perl's exists takes it: 1. Not in the language.", A + 'say exists $a[0] ? 1 : 0;', '$a[', "exists takes an element of a hash, found '$a': exists $h{...}")
r('delete-of-an-array-element', "perl's delete takes it: 1. Not in the language.", A + 'say delete $a[0];', '$a[', "delete takes an element of a hash, found '$a': delete $h{...}")
r('keys-of-an-array', "perl's keys takes it, for the indexes: 3. Not in the language.", A + 'say scalar(keys @a);', '@a)', "keys names a hash, found '@a': keys %h")
r('exists-of-a-hash', 'perl dies: exists argument is not a HASH or ARRAY element or a subroutine.', H + 'say exists %h;', '%h;', "exists takes an element of a hash, found '%h': exists $h{...}")
r('exists-as-a-statement', 'perl runs it, and nothing is done.', H + 'exists $h{a};', 'exists', 'this statement only has a value, and nothing is done with it')
r('keys-as-a-statement', "perl runs it: it sets each's place back, and the language has no each (D101).", H + 'keys %h;', 'keys', 'this statement only has a value, and nothing is done with it')
r('keys-assigned', "perl takes it, to make room: nothing printed.", H + 'keys(%h) = 100;', '= 100', "the left side of '=' is a variable, an element, an array, a hash, or a list of them in brackets")
r('each', "perl's each: a. Not in the language (D101).", H + 'while (my ($k, $v) = each %h) { say $k if $k eq "a"; }', 'each', "expected a value, found 'each'")

# ---- assignment
r('plus-assigned', "perl does not compile it: Can't modify private hash in addition (+).", H + '%h += 1;', '+=', "'+=' on a hash: a hash is assigned with =")
r('assignment-as-a-value', 'perl gives the count of the right side: 2 (D78).', H + 'my $n = (%h = (a => 1));\nsay $n;', '= (a', 'an assignment of a list is a statement: perl gives the count of its right side as its value (D78)', 2)
r('not-the-last-target', 'perl gives the hash everything: 1.', H + 'my (%g, $x) = (a => 1);\nsay scalar(%g);', '%g', 'a hash among the targets takes every value that is left: it is the last target')
r('where-one-value-is-declared', 'perl takes the count of an empty hash: 0.', 'my $n = my %g;\nsay $n;', 'my %g', 'my %g where one value is wanted')
r('length-of-a-hash', 'perl warns: length() used on %h (did you mean "scalar(keys %h)"?).', H + 'say length(%h);', 'length', 'length of a hash: perl warns, and means the length of its count; scalar(%h) is how many it holds')
r('defined-of-a-hash', "perl dies: Can't use 'defined(%hash)' (Maybe you should just omit the defined()?).", H + 'say defined(%h) ? 1 : 0;', 'defined', 'defined of a hash: perl refuses it; scalar(%h) is how many it holds')

# ---- D76: a later part may not change what an earlier part names
LATER = lambda what: f'a later part of {what} can change %h, which an earlier part names: perl reads it after the change; take the value into a my first'
r('element-and-a-delete', 'perl: 2.', H + 'say $h{a} + delete($h{a});', 'delete', LATER("'+'"))
r('hash-in-a-list-and-a-delete', 'perl: 9, and reads a value that was freed (D102).', H + 'my @l = (%h, delete($h{a}));\nsay scalar(@l);', 'delete', LATER('this list'))
r('values-and-a-delete', 'perl: 5.', H + 'my @l = (values(%h), delete($h{a}));\nsay scalar(@l);', 'delete', LATER('this list'))
r('worked-on-and-a-delete', 'perl: 3.', H + '$h{a} += delete($h{b});\nsay $h{a};', 'delete', LATER("'+='"))
r('element-and-a-sub-that-deletes', 'perl: 2.', H + 'sub del() { delete $h{a}; return 1 }\nsay $h{a} + del();', 'del()', LATER("'+'"), 2)
r('two-assignments-to-an-element', 'perl reads both late: 14 (T213).', H + 'say(($h{a} = 5) + ($h{a} = 7));', '= 7', LATER("'+'"))
r('element-and-a-store-in-a-list', 'perl: 55.', H + 'my @l = ($h{a}, $h{a} = 5);\nsay @l;', '= 5', LATER('this list'))
r('element-and-an-assignment-of-the-hash', 'perl: 2. An assignment to the hash is a change for D76 (D102); only a sub can hold one, since it is a statement.',
  H + 'sub clear() { %h = (); return 1 }\nmy @l = ($h{a}, clear());\nsay scalar(@l);', 'clear())', LATER('this list'))
r('said-and-deleted', 'perl: 11.', H + 'say $h{a}, delete $h{a};', 'delete', LATER("say's list"))

# (Seven tests of what waited for step 12b stood here until it was built:
# a hash in a loop's list, a slice, a hash as a parameter.)

# ---- a block that perl may take for a hash (T175, D102)
r('fat-comma-in-a-map-block', 'perl guesses a block: 1,2,3. Refused for the comma (D102).', A + 'my %g = map { $_ => 1 } @a;\nsay join(",", sort keys %g);', '=> 1', 'a comma in the block of a map, a grep or a sort: put the list in brackets, map { ($_ => 1) } ...')
r('word-and-fat-comma-in-a-map-block', 'perl guesses a hash, and does not compile it: syntax error.', A + 'my %g = map { a => $_ } @a;\nsay join(",", sort keys %g);', 'a =>', "a and a comma first in map's block: perl takes the block for an anonymous hash, and does not compile it; put the list in brackets")
r('two-fat-commas', 'perl leaves one out, and warns: Odd number of elements in hash assignment.', 'my %g = (a => 1, => 2);', '=> 2', "a comma with no value before it: perl leaves it out, in silence, where it doesn't refuse it")

# ---- what breaking the build on purpose found (T230, and two holes)
JOINED = lambda what, name: f'the {what} changes {name}, which the concatenation on the right reads: perl joins its pieces as it stores, after the {what} is worked out; take the string into a my first'
r('key-changes-what-a-concatenation-reads', 'perl joins the pieces after the key is worked out: kkv (T230).', 'my %g;\nmy $i = "a";\n$g{$i = "k"} = $i . "v";\nsay %g;', '= "k"', JOINED('key', '$i'))
r('key-changes-what-a-string-reads', 'an interpolated string is such a row: kk-v (T230).', 'my %g;\nmy $i = "a";\n$g{$i = "k"} = "$i-v";\nsay %g;', '= "k"', JOINED('key', '$i'))
r('index-changes-what-a-concatenation-reads', "an array's element too, since step 9: 2v (T230).", 'my @a;\nmy $i = 0;\n$a[$i = 2] = $i . "v";\nsay $a[2];', '= 2', JOINED('index', '$i'))
r('index-steps-what-a-concatenation-reads', 'through what perl folds away: 1v (T230).', 'my @a;\nmy $i = 0;\n$a[$i++] = 0 || $i . "v";\nsay $a[0];', '++', JOINED('index', '$i'))
r('index-calls-what-changes-what-a-concatenation-reads', 'through a sub: 2v (T230).', 'my @a;\nmy $i = 0;\nsub bump() { $i = 2; return 2 }\n$a[bump()] = $i . "v";\nsay $a[2];', 'bump()]', JOINED('index', '$i'))
r('change-in-the-key-of-exists', 'perl: 51.', H + 'my %g = (5 => 1);\nmy @l = ($h{a}, exists $g{$h{a} = 5});\nsay @l;', 'exists', LATER('this list'))
r('key-of-exists-with-a-leading-zero', 'octal, to perl: the key 8.', H + 'say exists $h{010} ? 1 : 0;', '010', '010 starts with a zero: perl reads that as octal, which the language writes 0o17')

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
