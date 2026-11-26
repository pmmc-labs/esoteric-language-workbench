# Review of step 11a's proposal: interpolation

**One WRONG: an index with a leading zero, which perl reads as octal (`"$a[010]"` is element 8), and the same rule takes `"$a[08]"`, which perl does not compile.**
**One place left to guess where the readings differ: how large the number in an index may be (from 2^63 perl wraps round, in silence, to an element).**
**Everything else stood: where a variable ends (about 890,000 strings the model accepts, run under perl, no difference but the leading zero), a string as a value made where it stands (80,000 random programs, and T198's refusal is enough), and `"$x"` against `$x . ""` (69 kinds of value, nothing a later operation can tell). No recommendation overturned.**

A reader who did not write it, with the proposal (`docs/PLAN.md`, "11a.
Interpolation", Q1 to Q4 each taken as its recommendation (a)) and perl
5.42.0. Nothing of the step is built and today's compiler refuses every
`$` and `@` in double quotes, so "the proposal gives" below is what its
sentences say; where a sentence can be read two ways, both are given.
Everything about perl was run. `outputs.txt` has perl's output for every
`.pl` here (`sh run-all.sh` rewrites it).

## 1. WRONG

### W1. A leading zero in an index is octal to perl (`w1.pl`, `w1b.pl`)

    use v5.42;
    my @a = (0 .. 20);
    say "$a[010]";
    say "$a[-010]";
    say "$a[017] $a[0010]";
    say "@a[010, 011]";
    say "@a[07 .. 010]";

perl 5.42, nothing on stderr, exit 0:

    8
    13
    15 8
    8 9
    7 8

The proposal, Q1(a): "a whole number or a scalar variable ... **The number
is decimal digits with a minus or without**". `010` is decimal digits, and
read as that it is ten: `10`, `11`, `17 10`, `10 11`, `7 8 9 10`. Accepted,
no fault, and not what perl prints.

T202 has the leading zero in its list (`$x[01]`, "element 1 for the first
three") and it is true of `01`: octal 1 is 1. Every index from `00` to `07`
is the same either way, which is why one probe did not show it.

The same sentence takes what perl refuses (`w1b.pl`):

    my @a = (0 .. 20);
    say "$a[08]";

    Illegal octal digit '8' at w1b.pl line 4, within string
    Execution of w1b.pl aborted due to compilation errors.          (exit 255)

Outside a string the language already refuses both: today's compiler says
of `$a[010]`, `010 starts with a zero: perl reads that as octal, which the
language writes 0o17`. The rule for a string was written fresh and lost it.

**What I would do: refuse.** The number in an index is the language's own
whole-number literal, as D38 has it outside a string: `0`, or digits that
do not begin with a zero, a minus before it or not. `-0` is in (element 0
to perl). No `_`, as the proposal has it (T202: `1_0` is ten to perl, and
"decimal digits" already leaves it out). `python3 fuzz.py index` finds this
by itself: 74 of the 4,718 index bodies the model takes as written differ,
every one a leading zero (`fuzz-index.diff`); with `--zero`, which is this
amendment, none of 2,469 differ.

## 2. Takes what perl refuses or warns about

Only W1's second half, `"$a[08]"` and `"$a[09]"` (and in a slice, `"@a[0 ..
09]"`), which the amendment above closes. Nothing else: in every run below
"accepted" means perl exits 0 and its stderr is empty, and that held.

## 3. Left to guess

### G1. How large the number in an index may be (`g1.pl`, `g1b.pl`)

    my @a = (10 .. 14);
    say "$a[18446744073709551615]";
    say "$a[18446744073709551614]";
    say "$a[18446744073709551616]";
    say "$a[99999999999999999999]";
    say "@a[0, 18446744073709551615]";

perl, in silence:

    14
    13
    14
    14
    10 14

From 2^63 up perl does not read past the end: 2^64 - 1 is the last element,
2^64 - 2 the one before, and anything from 2^64 on is the last again. At
2^63 - 1 and below (and for every negative number, however large) it reads
past the end and warns, which is the language's fault (`g1b.pl`). T202 has
"twenty nines is the **last** element" and the proposal repeats it under
"An index is code", but Q1(a) says only "decimal digits", with no bound.

Two readings: the number is a literal of the language's (then
`18446744073709551615 is past the largest integer` is a refusal, as it is
outside a string today), or the digits are carried to the runtime as they
are (and whatever turns them into an index decides: a fault if it is read
as past the end, an element if it wraps, and something else if a double
rounds it). The first is safe and is one more clause of W1's amendment:
**at most 9223372036854775807, or refused.**

### Left open, and both readings are safe

Not findings: recorded so the builder does not have to rediscover them.

- **A blank between the minus and its digits**, `"$a[- 1]"`: perl takes it
  (`- 1` is -1). The model allows it and agrees; refusing it is as good.
- **A slice that ends in a comma**, `"@a[1,]"`: the proposal says both "a
  slice in a string has a comma or a range" (T206) and "two or more of
  those with commas between". perl is quiet and gives one element; outside
  a string today's compiler refuses `@a[1,]` as a slice by one index and
  takes `@a[0,1,]`. `python3 fuzz.py index --zero --comma` takes the
  generous reading: 3,101 run, none differ.
- **What may follow `$#{a}`**: Q2(a) says "after `${x}` and `@{a}` nothing"
  is refused and does not name `$#{a}`; Q3(a) says `::`, `[` and `{` after
  "it" are refused. To perl everything after `$#{a}` is text (`"$#{a}[0]"`
  is `2[0]`, `"$#{a}::"`, `"$#{a}{x}"`, `"$#{a}->[0]"` likewise). The model
  refuses nothing after `$#{a}` and agrees with perl on every suffix tried.
- **`...` for `..`** in a slice: perl takes three dots as a range; the
  proposal names `..` only, and outside a string `...` is refused today.

## 4. Notes for the build (nothing here is a hole in the rules)

### N1. T198's refusal has to see through what perl folds, as T129's does (`n1-*.pl`)

T198 holds exactly as written, and `.=` is the only place perl loses the
assignment: 54 shapes in `n1-lost-assignment.pl`, 30 in `-b`, 19 in
`-folded`, 8 in `-pieces`. What the row does not show and a test should:

    $t .= ($u = (1 ? "$x$z" : 0));    # taz u    lost, behind a fold
    $t .= ($u = (0 || "$x$z"));       # taz u
    $t .= ($u = +"$x$z");             # taz u
    $t .= ($u = ("$x$z"));            # taz u
    $t .= $u = "$x$z";                # taz u    no brackets
    $b[0] .= ($u = "$x$z");           # paz u    an element on the left
    $t .= ($t = "$x$z");              # taz      the same variable: not "azaz"
    $t .= ($u = "$x$z") for 1, 2;     # tazaz u
    $t .= ($u = "$x\n");              # one variable and text is two pieces: lost
    $t .= ($u = "$x$z$x");            # taza u   three pieces: lost

The last is where a string is not T129's concatenation: T129 records that
`$u = $x . $z . $x`, three pieces, IS assigned, and a string of three, four
or more pieces is not (`n1-lost-assignment-pieces.pl`). So the proposal's
"unless the string is one variable, one array or one element and nothing
else" is the right line, and T129's exception for three must not be carried
over to strings. `checker.ts` already asks `wholes(w.value).some(...)` for
T129, which goes through folds; the string's node has to be asked the same
way, not only when it is the assignment's right side itself. Assigned, and
refused only by the rule's width: a string that is one slice or one `$#a`
(`"@a[0, 1]"`, `"$#a"`). Not lost, as the proposal says: `$t = $t . ($u =
"$x$z")`, `$t .= "-" . ($u = "$x$z")`, `($u .= "$x$z")`, `($u ||= ...)`, a
call, `? :` with a variable for its test, `scalar(...)`.

### N2. What in today's compiler stands on a string being a plain token (`n2.pl`, `n2b.pl`)

Five places test `kind === 'str'`. An interpolated string is a new token
and a new node, and each of these has to learn it:

- `lexer.ts`, `afterValue`: an operator comes after a string. `say "$x"
  -1;` is 4 to perl, `say "$x" .5;` is `55`, `say "$x"x 3;` is `555`.
- `parser.ts`, T175: `map { "$_", 1 } @a` does not compile under perl
  (`n2b.pl`). The proposal says so; this is where.
- `parser.ts`, what may follow a bare `undef` (T105).
- `checker.ts`, the index that is a string and no number, refused as the
  program compiles (`$a["x"]`): with `$a["${y}x"]` perl warns as it runs,
  which is the runtime's fault already.
- `checker.ts`, a pragma's arguments: `use open ":std", ":encoding($x)"`
  must stay refused.

`refusals.py` looks for more by rewriting every `refused` test that perl
itself objects to (33 have a string) with an interpolated string: perl
still objects to 31, and takes two in silence, both D53's (`if ($x =
"a")`), which the proposal has.

### N3. The walks the proposal does not name

"The checker's walks for D57, D69, D76 and D77, the freeze and D80's fault
past the end treat it as a value and do not look inside." The new node's
pieces are `array` and `slice` nodes, and three more walks care what those
are: `shapes.ts` (what is list-shaped, D18 and D71), the rule that an array
is a count where one value is wanted (D84's kin), and 10a's choice between
arguments as places and arguments built as a list. To perl (`n2.pl`):

    sub f() { return "@a" }      # one value: my $s = f(); is "1 2", no list
    sub g() { "@a[0, 1]" }       # the same as a last statement
    say scalar("@a"), "|", "@a" . @a, "|", length "@a";      # 1 2|1 22|3

A walk that goes into the node's children by default would call `f`
list-shaped and fault `my $s = f();`, or count the array.

## What stood

Each line is a claim of the proposal, how it was pressed, and the result.

- **Where a variable in a string ends** (Q2(a), Q3(a), and the list of what
  is refused after a shape). `model.py` is the proposal's rule and nothing
  else; `fuzz.py` runs every string the model accepts under perl and wants
  the same stdout, exit 0 and an empty stderr. No difference in any of:
  - `exhaustive`: 16 shapes, every suffix of 0 to 2 printable characters,
    every one-character prefix, 28 longer endings (`->[0]`, `->@*`, `->$#*`,
    `::y`, `\->[0]`, a new line and `[0]`, ...): 286,224 strings, 196,773
    accepted and run.
  - `arrow`: every shape, `->` and every two printable characters; eight
    shapes and every three characters of a 40-character nasty alphabet:
    504,544 strings, 412,125 run.
  - `random 400000 1`: up to nine tokens from that alphabet and 30
    fragments (`$a[`, `${`, `..`, `$#`, a new line): 161,912 run.
  - `index`: every index and slice body of up to four of 35 tokens:
    680,072 bodies, 4,718 accepted as written (74 differ: W1), 2,469 with
    `--zero` (none differ).
  - `binder for`, `binder sort`: `$_` in a `for` block, `$a` and `$b` in a
    `sort` block (`"$a[0]"`, `"$a[$a]"`, `"${a}"`; `"$b[0]"` with no `@b`,
    `"$_["`, `"@{_}"` and `"$#_"` refused): 37,994 and 70,203 run.

  So after a name, an element, a slice or `$#a` the refused list (`::`,
  `{`, `[`, `->` before `[ { @ $`) is complete over those alphabets, and
  after `${x}`, `@{a}` and `$#{a}` everything is text.
- **A name perl has a meaning for is only a name** (`words.py`): all 299
  words of `names.ts` (perl's 266 keywords and the 33 others: `s`, `y`,
  `q`, `qq`, `qw`, `tr`, `m`, `x`, `sub`, `__PACKAGE__`, `BEGIN`, `ARGV`,
  `ENV`, `INC`, `STDIN`, ...), as a scalar and an array, in 21 positions
  each (`$w`, `${w}`, `@w`, `@{w}`, `$w[0]`, `$w[$i]`, `@w[0, 1]`, `$#w`,
  `$#{w}`, before text, as an index): none differs, none warns. A sub of
  the same name as a variable in braces changes nothing either.
- **Names of 251 characters** work in all eight shapes; 252 is `Identifier
  too long` at the `my`.
- **A string is a value, worked out where it stands** (T196). `values.py`:
  80,000 programs of up to 12 statements (assignments and `.=` to scalars
  and elements, `say` with a list, two subs, one of which changes `$x`,
  `join`, `? :`, `x`), each operand an interpolated string, a bare variable
  or a bracketed assignment, nested three deep, kept inside D57, D76 and
  T198. The model makes every string where it stands; perl agreed on every
  one. Taking T198's refusal out of the generator turns 31 of 1,500 red, so
  the harness sees what it is for. By hand as well: `"$x" . ($x = 5)` is
  `35` for every one-piece string (`"$x"`, `"${x}"`, `"@a"`, `"$a[0]"`,
  `"$#a"`, a slice); a default that runs between two arguments (`d(undef,
  "$x")`) sees the old value; a string in a `for`'s list, in `grep`,
  `sort` and `reverse` (which hand on containers: step 10's W1) is a
  copy; `join("$x", 1, $x = 9, 3)` uses the old separator.
- **A string longer than perl's one operation takes** (`long-strings.py`):
  2 to 200 pieces, six kinds of piece, eight statements each: 48 programs,
  none differs.
- **A string made by one operation run twice is two strings**
  (`s-made-once.pl`, 38 lines): a sub called twice in a list, `map` round
  `grep`, `reverse` and `sort` of a string, recursion. perl copies each.
- **`"$x"` is `$x . ""`** (`same-as-dot.pl`): 69 values (Ints at every
  edge, Nums that print with an exponent, `-0.0`, both booleans, strings
  that are and are not numbers, a number that has been a string and the
  reverse), each written as `"$x"`, `"${x}"`, `"$a[0]"`, `"@a"`, `"@{a}"`,
  a slice and a doubled string, against `.` and `join`: 18 things a later
  operation can see (`is_bool`, `created_as_number`, `++`, `--`, `+ 0`,
  minus, `==`, `<=>`, as an index, as a count, in `substr`, the warnings).
  0 differ; held against the bare value instead, 36 do.
- **An interpolated string where a plain one stood does not change how perl
  reads the statement** (`reparse.py`): all 136 `same` tests, their 7,285
  double-quoted strings each rewritten three ways (`"${Zq}TEXT"`,
  `"TEXT${Zq}"`, `"@{Zq}TEXT$Zq[0]"`): perl prints the same for every one.
  By hand: after `say`, `print`, `sort`, `reverse`, `join`, `uc`, `length`,
  `defined`, `ord`; before `x`, `.`, a modifier; first in a `map`, `grep`
  and `sort` block; as a `? :` branch (`$c ? "$x:$y" : "$y:$x"`).
- **A string that interpolates is no constant** for D53: ten tested `=`,
  no warning.
- **Escapes beside a variable** (`s-escapes.pl`): a backslash always ends
  the name and always gives text: `"$x\x41"`, `"$x\::y"`, `"$x\->[0]"`,
  `"$x\[0]"`, `"$x\{a}"`, `"\\$x"`, `"\\\$x"`, `"$x\@a"`, a new line or a
  tab before `[`, `->` or `::`.
- **Past ASCII** (`s-past-ascii.pl`, and 13 strings by hand): after `${x}`,
  `@{a}` and `$#{a}` any character is text; a letter, digit or mark after
  `$x`, `@a` or `$#a` goes on with the name (refused); after an element or
  a slice it is text to perl, which the proposal refuses anyway.
- **An index that is a scalar** holding `"1"`, `1.9`, `true`, `false`,
  `-0.0`, `"-1"`, `" 1 "`, `"1.0"`, `"1e0"`, `"01"`, `"010"` (ten: a string
  is decimal where a literal is octal) is silent in perl and the element
  the language's rule for an index gives (`s-assignments-and-indexes.pl`).
- **The proposal's own claims**: `python3 docs/briefs/claims.py T196 ...
  T210-brace`, all 50 rows, as said.

## What I did not cover

- Q1(b) and Q1(c). Only the recommended (a) was modelled.
- The proposal's counts over the census's probes (4,915 `$name`, 5,061 of
  6,152 files): the probe corpus is not in this repository.
- Which line a fault names for a string that runs over several lines.
- Anything built: there is no compiler for this to run, so nothing here
  holds a build to the rules. The model and the scripts are meant to be
  turned on it (each takes `CURLY_PERL`; `model.py`'s `lex` is the oracle
  for refused-or-pieces).
- `values.py` has no loops, no `map`, `grep` or `sort` blocks, and no
  `||=`, `//=`, `x=`; those were tried by hand only (about 60 statements).
- Characters past ASCII were tried by hand, not generated.
- The random strings are thin on subscripts (the `index` mode is where
  those are dense), and no generated string has more than three characters
  after its shape except the 28 listed endings.
- Whether the language's own faults for an index held in a scalar (a
  string that is no number, a Num too large) are the ones perl warns at:
  taken from `LANGUAGE.md`, "Elements", not run through a compiler.

## Running it

Work files go to `$REVIEW_TMP` (default `./tmp`); perl is `$CURLY_PERL`
(default `/opt/perl-5.42/bin/perl`).

    sh run-all.sh                        every .pl here, into outputs.txt
    python3 fuzz.py exhaustive           286,224 strings, 2.5 minutes on four cores
    python3 fuzz.py arrow                504,544 strings, 4 minutes
    python3 fuzz.py random 400000 1
    python3 fuzz.py index                680,072 bodies; 74 differ (W1), in fuzz-index.diff
    python3 fuzz.py index --zero         none differ
    python3 fuzz.py index --zero --comma
    python3 fuzz.py binder for
    python3 fuzz.py binder sort
    python3 words.py                     299 words
    python3 values.py 80000 1000         80,000 programs, one minute
    python3 long-strings.py              48 programs
    /opt/perl-5.42/bin/perl same-as-dot.pl      69 values
    python3 reparse.py                   136 tests, 7,285 strings, three ways
    python3 refusals.py                  33 refused tests perl objects to

Only `index` has indexes with leading zeros, so `--zero` matters there
alone.
