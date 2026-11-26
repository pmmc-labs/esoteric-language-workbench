# Review of step 12's proposal: hashes

**Two ways to be WRONG, both about a word that is not a string once a
line end stands beside it. Four places where the rules as written take
what perl refuses, three left to guess, and three findings about the
oracle check. No recommendation overturned: Q2a and Q3a were held to perl
and stand (Q2a with one more refusal); what stood is at the end.**

A reader who did not write it, with the proposal (`docs/PLAN.md`, section
12, each question as its recommendation (a)) and perl 5.42.0, run plain.
Nothing of the step is built, so "the rules give" below is what the
proposal's sentences say a straightforward build would print. Everything
about perl was run: about 80,000 programs through the scripts here and
some 250 by hand. `outputs.txt` has perl's output for every `.pl` here
(`sh run-all.sh` writes it). `claims.py` was rerun whole: 765 claims, 0
differ, the 26 rows T214 to T222 among them.

## 1. WRONG

### W1. One word alone in the braces is a string only on one line (`w1.pl`)

    my %h;
    $h{
        true
    } = "a";
    $h{ true } = "b";
    $h{false   # the flag
    } = "c";
    $h{
        v65 } = "d";
    $h{ v65 } = "e";
    say join ",", map { "[$_]=$h{$_}" } sort keys %h;

perl:

    []=c,[1]=a,[A]=d,[true]=b,[v65]=e

The proposal: "**One word alone in the braces is that string**,
`$h{name}`, whatever the word", and T221 has "blanks allowed". By that,
the five stores make three keys, `true`, `false` and `v65`. perl quotes
the word only when nothing but blanks and tabs stands between each brace
and the word, **on one line**. With a line end or a comment on either
side the word is code: `true` is the key `1`, `false` the key `""`,
`v65` the key `A`, `__LINE__` the line's number, `time` the clock.

`words.py` asked for all 328 words (perl's 266, what `use v5.42` brings,
and some shapes) in 28 places, 8,885 programs. On one line, with blanks
or without, every word is its own text in every place the proposal
names. With a line end (`elem-lines`) or a comment (`elem-comment`)
inside the braces: 46 words are another key in silence, 53 warn (`undef`,
`shift`, `length`, and `print`, which prints), and the other 229, every
word that is not perl's own among them, do not compile (`Bareword "name"
not allowed`). So this is WRONG for perl's words and "takes what perl
refuses" for every other.

In a string the same holds (`"$h{\n a \n}"` does not compile; a tab is a
blank), which `strings.py` found for every word it tried.

What I would do: **refuse** a word alone in braces unless the word and
both braces are on one line with only blanks and tabs between (no
comment). Agreeing with perl would mean calling `true` there, which
nobody means.

### W2. `v` and digits before `=>` on the next line is a version string (`w2.pl`)

    my %h = (
        v65 => 1,
        v66
            => 2,
        v67    # a comment
            => 3,
    );
    say join ",", sort keys %h;

perl:

    B,C,v65

The proposal: "**`=>` quotes across the end of a line and a comment**
(T214)" and "a comma that makes a string of the word before it, whatever
the word"; T214's row has `v65 => 8` as the key `v65`, which is right on
one line. Across a line end perl reads the version string first: `v66` is
`chr(66)`. By the rules the keys are `v65,v66,v67`.

Of the 328 words, across a line end or a comment (`arrow-line`,
`arrow-comment`): `v1`, `v1_0` and `v65` are another key in silence, and
three do not compile at all: `dump` (`dump() must be written as
CORE::dump()`), `__END__` and `__DATA__` (the program's text ends there):
`p4.pl`. Every other word is quoted across the line, a sub's own name
too (`f\n=> 1` beside `sub f` is the key `f`).

What I would do: **refuse** `v` and digits (`isVersionString` in
`names.ts` already knows the shape) before `=>` unless the `=>` is on the
word's line; and refuse `dump`, `__END__` and `__DATA__` before a `=>` on
a later line. Cheaper and as safe: refuse a version-shaped word as a key
anywhere, since step 8 already refuses it as a sub's name.

## 2. Takes what perl refuses or warns about

### P1. `keys` and `values` are named unary operators too (`p1.pl`)

    my %h = (a => 1, b => 2);
    say keys %h + 1;

perl:

    Experimental keys on scalar is now forbidden at p1.pl line 6.
    Type of arg 1 to keys must be hash or array (not addition (+)) at p1.pl line 6, near "1;"

The proposal has T220's refusal for `exists` and `delete` only ("`exists`
and `delete` before an operator that binds tighter are refused without
brackets"), and "`keys %h`, `values %h`: ... where one value is wanted,
the count", so `keys %h + 1` reads as 3. `ops.py` ran 50 operators and
endings after each of the four with no brackets (700 programs, five kin
of theirs included): for all four, `+ - * / % ** . x` do not compile,
and every looser operator (`== < eq cmp && || // ? : and or .. ,`) is as
with brackets, in silence. T220's rule is right, for four words and not
two. `keys(%h) + 1` is 3.

Refuse, as T220.

### P2. `%` alone still dies for an odd count (`p2.pl`)

    sub f($x, %) { return "ok $x" }
    say f(1);
    say f(1, 2, 3);
    say f(1, 2);

perl:

    ok 1
    ok 1
    Odd name/value argument for subroutine 'main::f' at p2.pl line 6.

The proposal: "an odd number left is a fault ... `%` alone takes and
names nothing." A build that takes "names nothing" as "checks nothing",
which is what `@` alone is, prints three lines. The fault is `%`'s too.

### P3. What follows a hash's element in a string (`p3.pl`)

    my %h = (a => 1);
    say "$h{a}[0]";

perl:

    Can't use string ("1") as an ARRAY ref while "strict refs" in use at p3.pl line 8.

and the same death for `"$h{a}->[0]"`, `"$h{a}->{b}"`, `"$h{a}->@*"` and
`"$h{a}->$*"`; `"$h{a}["` does not compile. The proposal refuses
`"$h{a}{b}"` and says nothing else of what follows the brace; step 11a's
list for what follows a variable is "`::`, `{`, a second `[`, `->` before
`[ { @ $`", and after `$h{a}` the *first* `[` is already an index into
the value. A build that carries 11a's list over as it stands prints
`1[0]`.

What is text after the closing brace, in silence (`strings.py --tails`,
361 tails): `->` alone, `->%*`, `->x`, `::`, `(`, `.`, `-`, `'`. So the
rule for a hash's element is: refuse `[`, `{`, and `->` before `[ { @ $`.
With that, `strings.py`'s model of Q2a (a word between blanks and tabs,
or one scalar variable, and nothing else) agrees with perl on all 1,629
strings it takes out of 67,483.

Outside a string, `$h{a}[0]` and `$h{a}->[0]` die the same way; the
proposal names only `$h{a}{b}`.

### P4. A word alone in braces, or before `=>`, that perl does not compile

The other face of W1 and W2, counted here: `$h{\n name \n}` for any word
that is not perl's own (229 of the 328) does not compile; `dump`,
`__END__`, `__DATA__` before a `=>` on the next line do not (`p4.pl`).
The rules as written take all of them.

## 3. Left to guess

### G1. When an odd `%opts` stops the program (`g1.pl`)

    sub t() { say "default"; return 1 }
    sub f($x //= t(), %o) { return 1 }
    say "before";
    f(undef, "k");

perl:

    before
    Odd name/value argument for subroutine 'main::f' at g1.pl line 8.

perl checks the count as the sub is entered, before any default runs. The
language fills `@rest` "when its turn comes, after the defaults before it
have run", and a `%opts` built the same way finds the odd count then,
after `default` has been printed. Both stop; what was printed first
differs. The odd count belongs with the fault for a wrong number of
arguments, at entry.

(Filling, as opposed to counting, is late, as `@rest`'s is: with a
default that changes `$x`, `f(undef, a => $x)` has the new `$x`. D76's
walk already refuses that for arrays: today's compiler refuses the array
form, which I ran.)

### G2. `delete`, and an assignment to the whole hash, are changes for D76 (`g2.pl`)

The proposal says a later part "may not change" a hash an earlier part
names, and lists what names. Step 9's list of what changes is "assigning
it, storing to it, or changing its size". For a hash that has to say
`delete`, `%h = LIST`, a slice assigned, and a new key, because here perl
does not read late, it reads what has been freed:

    my %h = (a => 1);
    sub del() { delete $h{a}; return 0 }
    sub clr() { %h = (); return 0 }
    my @l = (%h, del());                 # a 0 0
    @l = ($h{a}, del());                 # 0 0
    @l = (values(%h), clr());            # 0 0
    say $h{a} + clr();                   # 0
    $h{a} += delete $h{a};               # the hash is left empty
    @l = ($h{a}, delete $h{a});          # 1 1

(perl's output beside each; `$h{a} .= (%h = (b => 2)) ? "x" : "y"` is a
segmentation fault in perl 5.42.) Every one must be refused; none can be
a `same` test. `delete` itself gives a value that names nothing:
`(delete $h{a}, $h{a} = 5)` is `1 5`, and `exists` likewise.

### G3. A slice on the left with too few values (`g3.pl`)

    my %h; my @a; my @b;
    @h{"a", "b"} = (1);   say exists $h{b} ? "made" : "not made";   # made
    @a[1, 2] = (5);       say scalar(@a);                           # 3
    @b[2, 1] = ();        say scalar(@b);                           # 3

"When the values run out the rest of the targets are undef": for a slice
that is a store of undef, which makes the key and lengthens the array. A
build that stops storing when the values run out prints `not made`, 2
and 0.

The rest of Q3a held: the right side first, then every index and key,
then the stores, for slices alone and among other targets, with keys
that have effects and with a right side that reads the same hash or
array through `reverse`, `sort`, `grep`, `values` and slices (perl copies
there, as the language does); a key twice keeps the last value; too many
values are dropped; an undef key warns (D48's fault); `@a[-2, 0] = ...`
on an array of one dies (the fault for a store before the start).

### Smaller guesses, each safe whichever way it falls if it is refused

- **A hash that is not the last target**: `my (%h, $x) = (a => 1, b =>
  2);` is silent in perl (`$x` undef). Arrays say "last"; say it of a
  hash.
- **A slice of one on the left**: `@h{"a"} = (1);` and `@a[1] = (5);`
  are silent in perl (the warning is only for reading). The array rule
  refuses a slice of one; keep it for both sides.
- **`return %h;`, `return keys %h;`** reached for one value give the
  count in perl (7 shapes run). If a hash is list-shaped for D18, as an
  array is, that is a fault, which is the safe side; it has to be
  list-shaped for the call where a list is wanted to be right.
- **`map { $_ => 1 } @list`**: today's compiler refuses a bare comma as
  a block's last statement, so with `=>` a comma this idiom is refused
  and `map { ($_ => 1) } @list` is the spelling. If it is opened,
  `mapblock.py` (71 blocks) has what perl takes for a hash in braces and
  so does not compile: a word, a string in either quotes (an
  interpolated one too) or a whole number, then `=>` or a comma.
  `lc($_) => 1`, `$_ => 1`, `"$_" . "x" => 1`, `1.5 => 1` and `-1 => 1`
  are blocks.
- **`sub f(%o, @r)`, `sub f(@r, %o)`, `sub f(%o = (...))`, `sub f(%o,
  $x)`** do not compile; an undef key among the arguments warns
  (`Use of uninitialized value in subroutine argument`).
- **`$h{$k, }`** (a trailing comma) is the key `$k` in silence; `$h{1,
  2}` does not compile under `use v5.42` (`Multidimensional hash lookup
  is disabled`). Refuse both.
- **`@h{'a','b'} += 1;`** compiles and does nothing, in silence. Refuse.

## 4. The oracle check

### C1. An order shown, the reading rule satisfied, the eight seeds agreeing (`reading.py`)

The reading rule passes a `keys` or `values` that has `sort` before it,
through `map`, `grep` and `reverse` and through one bracket. Three shapes
of this step's language show an order under a sort:

    say sort { $a cmp $b } (keys %h)[0];                  # one key is sorted: the first, in perl's order
    my @s = sort grep { say $_; 1 } keys %h;              # the block speaks before the sort
    my @s = sort { say "$a $b"; $a cmp $b } keys %h;      # the comparator shows what it was handed

`reading.py` calls `hash_order_shown` and `perl_says` themselves and
searches key names until both are satisfied. It needs under a hundred
pairs each time (two keys agree under eight seeds one time in 128):

    my %h = (three => 1, pear => 2); my @s = sort grep { say $_; 1 } keys %h;
    the eight seeds all print 'pear\nthree\n'; seeds 9 to 40 print both orders

That is a `same` test by the check, with `pear` first for its expected
output, and D27 prints `three` first: a red test where the compiler is
right. `reading.out` has six. The comparator that logs is the one step
10's own tests are written like (1200, 1201).

What I would do: reject, in a `same` test, a block of `map`, `grep` or
`sort` with a `say`, `print`, `push` or assignment in it when the block's
list has a hash in it; and stop taking a bracket followed by `[` for
sorted. And a test of this step uses five or more keys wherever a sort
could tie or a block could speak: then eight seeds agree by luck about
once in 10^14.

### C2. No order shown, and the reading rule rejects

`reading.py`, part 2. Rejected as "a whole hash without sort" or "keys
without sort": `if (%h)`, `my $n = %h;`, `%h + 0` (T219's count, which
only `scalar(%h)` can test as the rule stands), `my %g = %h;` (T222's
copy), `sub f($x, %o)` and `f(%h)` (every `%opts` test), `keys %h == 2`,
a sum over `values %h`, `delete` in a loop over `keys %h`, a hash made by
`map` over `keys`. The rule errs toward rejecting, as it says; this is
the list the step's tests will meet on the first day.

### C3. A fair program on which D27 differs (`c3.pl`, `order.py`)

D27 says "perl's order changes with every run, so any order agrees with
perl". Some things about perl's order do not change with the run:

    my @p = sort { 0 } keys %h;                 # 20 keys
    say $p[0] eq "k0" && $p[19] eq "k19" ? "same" : "differ";
    for my $i (1 .. 100) { $h{"n" . $i} = 0; }
    my @q = grep { substr($_, 0, 1) eq "k" } sort { 0 } keys %h;
    say join(",", @p) eq join(",", @q) ? "same" : "differ";
    delete $h{k7}; $h{k7} = 7;
    my @r = sort { 0 } keys %h;
    say $r[119] eq "k7" ? "same" : "differ";

perl prints `differ` three times under 200 seeds of 200; the order of
first storing prints `same` three times. The reading rule passes it
(every `keys` is under a sort; `sort { 0 }` is its known hole) and the
eight seeds agree, so by D10 it is a `same` test, and the language can
never pass it. `order.py` has seventeen such questions under 40 seeds:
perl answers `differ` every time for a copy (`my %g = %h` does not keep
`%h`'s order), for `%h = %h`, for a `%opts` filled from a hash, for the
old keys after a hundred new ones; and `same` every time for `keys`
twice, `keys` beside `values`, the rest after a `delete`, and a store to
an old key, which D27 agrees with.

This does not touch D27 (D14 puts the order outside the agreement). It
is one more reason the check has to refuse `sort { 0 }` by reading: a
comparator that does not name `$a` and `$b` settles nothing.

### C4. Two things the step's tests should know

- **perl crashes or prints what was freed on the freeze's own fault
  tests** (T194's kin). `for my $v (values %h) { delete ...; $h{new} =
  ...; say $v }` prints `2`, then `new`, then dies with `Use of freed
  value in iteration`; `grep { delete $h{a}; ... } values %h` and `sort {
  %h = (); ... } values %h` are segmentation faults (exit 139); `map {
  %h = (); ... } values %h` prints `x1 x xx1` with `Attempt to free
  unreferenced scalar`. The freeze makes each a fault; no test can ask
  perl for them, and a fault test's loop must still end under perl.
- **With one seed, perl's order still moves** with the names in the
  environment and with the file's own path: under one `PERL_HASH_SEED`,
  a five-key hash printed four different orders for me as I added `B=2`
  to the environment, copied the file to another name, or ran it by its
  full path. `run_perl` fixes the environment, so the check is
  repeatable; but a test's `# env:` line, or renaming a test, is a new
  draw of all eight seeds.

## 5. What stood

- **A word is a string, on one line** (`words.py`, 8,885 programs): all
  328 words, in `$h{W}`, `$h{ W }`, `(W => 1)`, `(W=>1)`, first and
  second in a list, as an argument, after `return`, `push`, `join` and
  `say`, in `"$h{W}"` and `"$h{ W }"`, under `exists` and `delete`, and
  beside a sub of that name. `q`, `s`, `y`, `tr`, `m`, `qw`, `x`, `if`,
  `__PACKAGE__`, `STDERR` included. `say STDERR => 1;` prints `STDERR1`.
  After a value, `"k" x W => 2` is `x` and then the word as a string
  (a warning: not a number); `"k" x => 2` does not compile.
- **A key is the string `.` makes** (`keys.py`, 1,356 programs): 113
  values (Ints to 2^64, Nums, `-0.0`, `1e15`, `1e21`, booleans, numeric
  strings, computed values), each as a literal in braces, in brackets,
  in a variable, through a sub, after use as a number and as a string,
  interpolated, before `=>`, as a slice's key, under `exists` and
  `delete`, and in `"$h{$v}"`. The only differences are the bare words
  `true` and `false`, which T215 has. No past shows in a key.
- **A hash is an array whose indexes are strings** (`made.py`, 166
  programs): in 45 places a value can stand, perl makes a hash's missing
  element or slice exactly where it makes an array's. D80's orders are
  the array's for `=`, `OP=`, `++`, `//=` chains, list assignment and
  slices (by a sub that logs). `$h{$k} + ($k = "b")` reads the key early
  and the value late, as `$a[$i]` does. The count (`%h`, `keys %h`,
  `values %h`, `scalar` of each) is a value, read where it stands:
  `f(scalar(%h), add(), scalar(keys %h))` sees 10, then 11. `%h = (%h, c
  => 3)`, `%h = %h`, `%h = (a => $h{b}, b => $h{a})`, `($h{a}, %h) = (9,
  c => $h{a})` are what copying gives. `$h{@a}` is the count of `@a`,
  `$h{%g}` and `$h{keys %g}` counts.
- **The count** in some 60 positions (every kind of operator, an index,
  a key, a range's end, a sub's `return`): no warning but for `length
  %h`, and no compile for `defined %h`, both of which the array rule
  already refuses.
- **T220** for `exists` and `delete` (`ops.py`); the bracketed forms;
  `delete` of a slice; `delete` and `exists` of what is not an element
  do not compile.
- **Q2a** with P3's amendment (`strings.py`): 67,483 strings, 1,629 the
  model takes, none differ. `"${h}{a}"` is `$h` and text; `"${h{a}}"` is
  the element (refused by D92 already); `"@h{a}"` warns.
- **Q3a**, as under G3.
- **`%opts`**: defaults before it, after an optional parameter, a hash
  and more, a flattened odd array (dies), a key twice (the last), `%`
  alone, the four shapes that do not compile.

## 6. Not covered

Nothing was built, so nothing here ran the compiler on a hash; the array
forms were run through today's compiler only to learn which rule was
meant (about fifteen programs). D36's fault for a Num as a key and D48's
for an undef were not held to anything beyond perl's warning. Q4 (`each`,
the loop of two variables) has nothing to test, and Q1 is not a question
about perl. Keys past ASCII, a word past ASCII before `=>`, and hashes
large enough to matter to the runtime's table were not tried.
`strings.py` is exhaustive over 40 pieces to three deep, not random;
nothing longer was run. The 638 waiting probes of the census were not
read. The freeze was checked only as far as T217 and the crashes in C4:
no matrix of every binder against every change.

## 7. The scripts

Each is run from anywhere as `python3 docs/briefs/step12-review/NAME.py`
and needs perl 5.42 as `CURLY_PERL` (default `/opt/perl-5.42/bin/perl`);
`REVIEW_TMP` names a directory for temporary files. Each has its output
of this review beside it as `NAME.out`.

| Script | What it asks | Programs |
|---|---|---|
| `words.py` | 328 words in 28 places: is the word its own text, in silence? | 8,885 |
| `keys.py` | 113 values in 12 places: is the key what `.` gives? | 1,356 |
| `ops.py` | 50 operators and endings after `exists`, `delete`, `keys`, `values` and five kin | 700 |
| `made.py` | 45 places, hash and array, element and slice: is it made? | 166 |
| `strings.py` | `"$h{CONTENT}TAIL"` against a model of Q2a; `--tails` lists the tails | 67,483 strings, 1,629 run, and 361 tails |
| `mapblock.py` | 71 ways a `map`'s block can begin: a block, or a hash to perl? | 71 |
| `order.py` | 17 questions about two orders, under 40 seeds | 680 |
| `reading.py` | the reading rule and the eight seeds, by `t/checks.py`'s own functions | about 3,000 |
| `run-all.sh` | every `.pl` here under perl, into `outputs.txt` | 10 |
| `common.py` | perl with a timeout, the keyword table from `names.ts` | |
