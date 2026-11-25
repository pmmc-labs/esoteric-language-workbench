# Review of step 10's proposal: list operators, `$_`, list returns

A reader who did not write it, with the proposal (`docs/PLAN.md`, section
10, each question taken as its recommendation (a)) and perl 5.42.0. The
step is not built, so "the proposal prints" below is what its rules say a
straightforward build would print; where that reading is uncertain it
says so. Everything about perl was run: about 330 programs by hand, and
two harnesses, `E-past.py` and `E-sort-matrix.py`, which also run today's
compiler. `outputs.txt` has perl's output for every `.pl` here.

**One line covers the three largest findings: `grep`, `sort` and
`reverse` hand on the containers they were given, as a list does; a
`sort` with a block treats its list as `map` and `grep` do; and what
perl does for `sort` depends on whether it could throw the block away.**
The proposal checked the second and third only with `{ $a <=> $b }`,
which is one of the four blocks perl throws away.

## 1. WRONG

### W1. `grep`, `sort` and `reverse` give back the containers, and D76 does not look inside them (`w1.pl`)

    my @a = (1, 2, 3);
    sub chg() { $a[0] = 50; return 7 }
    my @r = (reverse(@a), chg());            say "@r";

perl:

    reverse: 3 2 50 7
    grep:    50 2 3 7          ((grep { 1 } @a), chg())
    sort:    50 2 3 7          ((sort { $a <=> $b } @a), chg())
    sort2:   50 2 3 7          ((sort @a), chg())
    map:     1 2 3 7           map copies; join gives a value at once
    scalar:  9 5               ((grep { 1 } $v), bump())
    scalar2: 0 9 5             (reverse($v, 0), bump())
    slice:   57                (reverse(@a))[2] + chg()
    slice2:  14                (grep { 1 } $v)[0] + bump()
    say:     32507             say reverse(@a), chg();
    join:    3-2-50-7          join("-", reverse(@a), chg())
    32507 :foreach             for my $x (reverse(@a), chg())
    inner:   3 2 50 7          map { $_ } (reverse(@a), chg())
    default: 5/9               f(undef, grep { 1 } $v) with f($p //= bump(), $q = 0)
    default2: 5/9              f(undef, reverse($v))

The proposal: a list is values copied as it is built, so `reverse(@a)`
is `3 2 1` before `chg` runs, and every line but `map:` differs. What
lets it through: D76 refuses a later part that changes what an earlier
part *names*, and "names" is by shape (`named` in `checker.ts`: an
element, a slice, an array, `$#a`, a scalar that is an item, through
brackets, `? :`, `||`, a list repeated and a slice of a list). The
proposal's only word on D76 is that it "goes through a block", which is
about what a block *changes*. Nothing says a `grep`, a `sort` or a
`reverse` names what its list names. The freeze and D77 do not help:
they are about the binder's own block, and here the change comes after
the binder has finished, from a later part of the enclosing list,
operator or argument list.

Amendment (refuse, with D76's message): **what a `grep`, a `sort` or a
`reverse` names is everything its list names, scalars as items of a
list** (`scalars = true`); `map` and `join` name nothing (perl's `map`
copies, `join` gives a value), though naming through `map` as well is
one rule fewer and costs only programs nobody writes. It has to hold
through a slice of the result, in a call's arguments against the
callee's defaults, in a `foreach`'s list, and nested.

### W2. `join`'s separator is read when `join` runs (`w2.pl`)

    my $sep = "-";
    sub chs() { $sep = "+"; return 1 }
    say join($sep, chs(), 2, 3);

perl: `1+2+3`, and `1;2;3` for a separator that is an element stored to
by a later item. The proposal: "SEP is one value", worked out first, so
`1-2-3`. Amendment: for D76's walk the separator is the first item of
`join`'s list, with scalars as items (refused when a later item can
change it).

### W3. `@a = sort BLOCK @a` drops every element that was never stored (`w3.pl`)

    my @d = (3); $d[3] = 1;
    @d = sort { ($a // 0) <=> ($b // 0) } @d;
    say scalar(@d), ": ", join(",", map { $_ // "u" } @d);

perl:

    2: 1,3
    4: u,u,1,3      the same four values, each stored: (3, undef, undef, 1)
    4               my @copy = sort ... @f       (not in place)
    4               @g = reverse sort ... @g     (not in place)
    4               after `my @m = grep { 1 } @h;`
    2               after `for my $x (@i) { }`
    1               my @j; $j[2] = 5; @j = sort { 0 } @j;

The proposal: an element between is undef (D80), the block takes undef,
nothing is frozen that matters, so four elements, `u,u,1,3`. perl sorts
in place when the statement is exactly `@a = sort ... @a` (also `(@a)`
on the right, or brackets round the `sort`), and its in-place sort
weeds out the slots that hold nothing (`pp_sort.c`, "Weed out nulls").
Whether a slot holds nothing is a past of the array's: a store past the
end leaves the slots between empty, and `map`, `grep`, a call `f(@a)`,
a not-in-place `sort BLOCK @a`, `@a = @a` fill them, while `foreach`,
`reverse`, a copy and a read do not (26 routes tried). That is perl
having two answers by a past, which the language answers with a fault
everywhere else.

Amendment (fault; agreeing needs the runtime to track empty slots
through every one of those routes): **an undef element in an array
sorted in place is a fault**, raised before any comparison: `an undef
in an array sorted in place: perl drops an element that was never
stored`. In place means the three shapes above. With no block and with
`{ $a <=> $b }` and its kin the comparison would have faulted on the
undef anyway; the new fault is only for blocks that take undef. The
cost: `@a = sort { ($a // 0) <=> ($b // 0) } @a` with a stored undef,
which perl sorts; `my @s = sort ...; @a = @s;` says it.

### W4. A `sort` with a block makes an element past the end; the proposal says it makes nothing (`w4.pl`)

    my @a = (1);
    my @r = sort { ($a // 0) <=> ($b // 0) } @a[0 .. 3];
    say scalar(@a);

perl:

    slice, a block:      4
    element, a block:    6     sort { ... } $a[5], 1
    one element:         6     sort { 0 } $a[5]
    through ? ::         6     sort { 0 } (1 ? $a[5] : 0), 2
    reverse sort:        6
    in a foreach:        6     for my $x (sort { 0 } $a[5], 1)
    { $a <=> $b }:       1
    no block:            1
    reverse, join:       1

The proposal ("Past the end (T177): D80's fault ... not of a `sort`, a
`join` or a `reverse`, where perl makes nothing") prints 1 for all of
them. `claims.py`'s row `T177-sort` tried only `sort { $a <=> $b }
$a[9], 1`. perl makes nothing for exactly the blocks it optimises away:
`$a <=> $b`, `$b <=> $a`, `$a cmp $b`, `$b cmp $a`, each through
brackets, a unary plus or a stray `;`, and for no block. `{ 1; $a <=>
$b }`, `{ return $a <=> $b }`, `{ $a <=> $b || 0 }`, `{ $a - $b }` and
every other block make the element (33 blocks tried).

Amendment (fault): **D80's fault for an element or a slice past either
end in the list of a `sort` too**, through T169's shapes, whatever the
block. For the optimised blocks and no block the undef would have
faulted in the comparison (or by S1 below, for one element), so one
rule for every `sort` costs nothing.

### W5. `sort true, false`: the word first after `sort` is a name to perl (`w5.pl`)

    my @r = sort true, false;
    say join("|", @r);

perl:

    |true
    true            sort true;
    2|3|false       sort false, 3, 2;
    a|truex         sort true . "x", "a";
    true|           reverse sort true, false;
    |1              sort { $a cmp $b } true, false;
    |1              sort +true, false;

No warning. The proposal: `sort LIST`, and `true` is the boolean, so
`|1`, `1`, `|2|3`. perl's lexer forces a word after `sort` to be a
bareword (it may be a sub's name), and `true` and `false` are not
keywords to it; a keyword (`undef`, `scalar`, `reverse`, `map`, `uc`
...) is itself. `sort(true, false)` is `|true` too, with `Unquoted
string "true" may clash with future reserved word`; `sort true , 2`,
with a blank before the comma, does not compile (`No comma allowed
after subroutine name`).

Amendment (refuse): see W6, one rule for both.

### W6. `sort NAME(...)`: the sub is the comparator (`w6.pl`)

    sub k() { return 5 }
    my @r = sort k(), 3, 1;
    say "@r";

perl:

    1 3             sort k(), 3, 1        (k compares; the list is (), 3, 1)
    3 1             reverse sort k(), 3, 1
    1 3             sort k (3, 1)
    1 3 5           sort(k(), 3, 1)       in sort's own brackets it is a call
    1 3 5           sort +k(), 3, 1
    1 3 5           sort { $a <=> $b } k(), 3, 1
    3 1 2           sort zero(@a) for @a of (3, 1, 2): zero compares, @a is the list

No warning. A sub with required parameters dies there (`Too few
arguments for subroutine 'main::two' (got 0; expected 2)`). The
proposal: `sort LIST` whose first value is a call, so `1 3 5` and, for
the last, `0`. **This one I could not fully settle on the proposal's
side**: it refuses "`sort NAME LIST`", and a builder who knows why may
refuse a call there as well; but a call with its brackets is a value
everywhere else in the language (D21), and nothing in the text says it
is not one after `sort`.

Amendment for W5 and W6 (refuse): **the token after `sort`, and after
`sort(` or `sort (`, may not be a word that is not one of perl's own
keywords**: not a sub's name, with brackets or without, and not `true`
or `false`. `sort +k(), ...`, `sort (k()), ...` (see S2 for the blank)
and a block say what was meant.

## 2. Shapes perl refuses or warns on that the proposal accepts

- **S1. A `sort` of one value, with no block or with a block perl
  optimises away, warns for that value** (`s1.pl`): `my @z = ("abc");
  my @r = sort { $a <=> $b } @z;` gives `Argument "abc" isn't numeric
  in sort`; `my @u = (undef); @r = sort @u;` gives `Use of
  uninitialized value $u[0] in sort`, and so do `{ $b <=> $a }`, `{ $a
  cmp $b }`, `{ $b cmp $a }`. perl turns every element to a number or
  a string before it sorts, and a merge that calls the block for each
  comparison never looks at a lone value. Any other block is silent,
  as the port would be. Amendment: for those five forms a list of one
  value is checked as a comparison would check it (compare it with
  itself and drop the answer: the forms have no effects to show).
  With two values or more every value is compared at least once, and
  the fault comes anyway.
- **S2. `sort (...)` with more after the bracket**: `my @r = (sort
  (@a), 9);` and `say sort (@a), 9;` warn `sort (...) interpreted as
  function`. Not `sort(@a), 9`, not `sort (@a);` alone, and not
  `reverse (` or `join (`. Refuse as T76 does for `say`.
- **S3. A bare block first in a `map`, `grep` or `sort` block** is an
  anonymous hash to perl: `map { { print "x"; } $_ } @a` is a syntax
  error, and `map { { 5 } } 1` gives a hash with `Odd number of
  elements in anonymous hash`. A bare block after another statement
  is a block. Refuse `{` as a block's first token.
- **S4. `for () { }`** does not compile (T155's kin); `say "x" for ();`
  does, and runs nothing.
- **S5. Two modifiers**: `$n += $_ for 1 .. 3 if 1;` and `say "x" if 1
  for 1, 2;` are syntax errors.
- **S6. `join(undef, "a")`, `join($u)`** warn `Use of uninitialized
  value in join or string` though the separator is never used. The
  separator is made a string whatever the list holds.
- **S7. `say $_ -1`, `say $a -1`, `print $a +1`, `say $_ (1)`** in a
  block die, `Can't use string ("5") as a symbol ref`: T111's refusal
  has to know `$_`, `$a` and `$b`. `$_[0]` is an element of `@_` and
  `$_{1}` of `%_`, each compiled in silence at the top level; `$a[0]`
  in a `sort` block is `@a`'s element.
- **S8. `[` after a builtin's own brackets**: `sort (@x)[0, 1]` and
  `reverse (@x)[0, 1]` are syntax errors (T168's kin). `sort { ... }
  (@x)[0, 1]` and `map { ... } (@x)[0, 1]` are slices.
- **S9. No list**: `map { $_ };`, `grep { $_ };`, `sort { $a <=> $b
  };`, `sort;`, `sort ();`, `join();` do not compile. `reverse;` and
  `reverse();` are the empty list, and `join(",")` is `""`.
- **S10. Where nothing is wanted**: `sort @a;`, `reverse @a;` and
  `join(",", @a);` as statements warn `Useless use of ... in void
  context`; `map { ... } @a;` and `grep { ... } @a;` do not.
- **S11.** `sort { $a <=> $b, 0 }` and `sort { ($a, $b) }` warn
  (`Useless use ... in void context`); `grep { () } @a` is false in
  silence; `sort { "abc" }` and `sort { undef }` warn. The proposal's
  rules (one value, a whole number) already refuse or fault each.

## 3. Holes in the proposal's text

- **`last`, `next` and `return` under a `for` modifier** (`s2.pl`).
  "The statement is what may stand before `if` today" takes in `last`,
  `next` and `return`. perl: `for my $i (1 .. 3) { last for 1, 2; print
  $i; }` prints `123`: the modifier is the loop that `last` leaves. A
  build that ties it to the loop round it prints nothing, which would
  be WRONG. Say that `last` and `next` keep T120's rule (no `for`
  after them). `return $_ for 4, 5;` gives 4.
- **When a slurpy parameter is filled** (`s2.pl`): `f(1, $v, bump())`
  with `sub f($x, @rest)` is `1|9 5`, and `g(1, undef, $v)` with `sub
  g($x, $y //= bump(), @rest)` is `1|5|9`. So `@rest` is copied from
  the argument pointers when its turn comes, after every default, and
  not built by the caller as the arguments are worked out. "A new
  array of copies" does not say which; the second would be WRONG.
- **Which `$_` a binder's own list sees**: the outer one. `for (1, 2)
  { my @r = map { $_ * 10 } ($_, 5); }` gives `10 50` and `20 50`;
  `for (1 .. $_)` inside a `for`. The inner binding starts at the
  block.
- **`$_` in a `sort` block inside a `map` block** is the `map`'s; and
  `$a` in a `map` block inside a `sort` block is the `sort`'s. "Seen
  in the block alone" should mean through blocks that do not bind the
  same name.
- **`return` at any depth in a block**, in a loop or an `if` inside
  it, is still the block's `return` (T174). **`last` and `next` to a
  loop that is itself inside the block** are fine in perl (`map { for
  my $i (1, 2, 3) { next if $i == 2; last if $i == 3; ... } ... }`);
  "to any loop" reads as refusing those too.
- **Brackets**: `map({ $_ * 2 } @a)`, `grep({ ... } @a)`, `sort({ $b
  <=> $a } @a)` compile and mean the same. In or refused?
- **T143's refusals were "until step 10"**: `return ("a") x 3`, `(LIST)
  x N` as an argument and as a last statement, and now `map { ($_) x
  2 } @a`. The proposal does not say they are lifted.
- **A sort block's value that is a word-operator pair**: `sort { $a
  <=> $b or $a cmp $b }` is the everyday two-key sort. Step 5 refuses
  two values joined by a word operator as a statement; as a block's
  last statement it has to be a value.
- **A block's last statement that is a `my`**: `map { my $q = $_ }` is
  the value in perl; `map { my @q = ($_, 1) }` and `map { my ($p, $q)
  = (5, 6) }` are the lists (D78 gives them no value here).
- **Block or hash, the exact rule**: perl looks at a quoted string, or
  a run of word characters (so `1_0`, `0x10`, `1e3`, and a lowercase
  word), then blanks on the same line, then `,` (not after a lowercase
  word) or `=>`. `map { "a" => 1 }`, `map { true => 1 }`, `map { x =>
  $_ }`, `map { 10 => 6 }` are syntax errors: `=>` counts as the
  comma, after a lowercase word too. `map { "a" . $_, 1 }`, `map { .5,
  1 }`, `map { 1e+3, 1 }`, `map { lc("A"), $_ }`, `map { undef, $_ }`
  are blocks; the proposal's rule refuses some of these, which is only
  stricter. The same guess is made for a `sort` block and a `grep`
  block (`sort { 0, 1 } ...` and `grep { "a", } @a` do not compile).
- **`@a = sort ... @a` and the freeze**: the array is frozen until the
  sort ends and stored to after, in the one statement; the same for
  `@a = grep { ... } @a` and `@a = map { ... } @a` (each as perl has
  it: 23 list assignments from a `grep`, `sort` or `reverse` of their
  own targets all agreed with a copy).
- **D77 for the modifier**: the statement of `STATEMENT for LIST` is
  the block, for D77 and the freeze.
- **The freeze names `$#a`**, so `$a[$_] *= 2 for 0 .. $#a;` faults
  (D81). Worth a sentence beside the modifier, since `$_ *= 2 for @a`
  is refused too.

## 4. Too strict

- `$a[$_] *= 2 for 0 .. $#a;` and `for (0 .. $#a) { $a[$_] = ... }`:
  the fault (D81's freeze by name). `my $n = @a;` first, or `@a = map
  { $_ * 2 } @a`.
- `last` and `next` for a loop written inside a `map`, `grep` or
  `sort` block, if "to any loop" is taken as written.
- `map { ($_) x 2 } @a`, `return (0) x $n;` if T143 stays.
- `sort { $a <=> $b or $a cmp $b }` if the word operator stays refused
  there (`||` works: perl gives the operand).
- Q4(a) refuses `grep { defined } @a`, `print for @a`, `map lc, @a`;
  known, and each has a spelling.
- With the amendments here: an in-place sort of an array that holds a
  stored undef (W3); a slice past the end in a `sort`'s list (W4);
  `sort k(), ...` wants a `+` or brackets (W6).

## 5. What stood

- **The numeric past, through every binder**: 108,416 comparisons of
  perl with perl (`E-past.py`: 77 values; 32 routes, among them a
  numeric `sort` of one and of two values, `$b <=> $a`, in place,
  `reverse sort`, a block perl does not optimise, a string `sort`,
  `grep` by number, by string and by truth, `join`, three `map`s,
  `reverse`, `for` and the `for` modifier, on the original and on the
  result; 44 uses after). 1,106 differ, and **today's compiler faults
  on the fresh value in every one**: the differences are all a past
  the language already answers with a fault (`++` on a string, a
  whole Num at 10^15 printed, an integer at 2^53 beside a float).
  perl's numeric `sort` does turn its strings to numbers in place, and
  for one element too; it shows nowhere new.
- **The optimised sorts make the decisions the block would**:
  `E-sort-matrix.py` takes today's compiler's own answer for every
  pair of 45 values under `<=>` and under `cmp` (Ints and Nums on both
  sides of 2^53, the top of the integers, numeric strings of every
  shape D40 takes, booleans), runs perl's merge with those answers as
  the block, and compares with perl's `sort { $a <=> $b }`, `{ $b <=>
  $a }`, `reverse sort`, in place, `{ $a cmp $b }`, `{ $b cmp $a }`,
  `sort` and `reverse sort` with no block: 9,600 numeric and 12,000
  string sorts of 2 to 20 values, repeats among them, none different.
  (Broken on purpose, by swapping one pair's answer, it reports at
  once. `1e15` is left out of the lists: perl prints it two ways by
  its past, D36, and the first run counted that as an order. The
  values that fault against themselves, six under `<=>` and one under
  `cmp`, are left out too, and no other pair faults.)
- **The order of comparisons does not depend on the form**: the pairs
  logged by a block are the same for `my @b = sort`, `@a = sort ...
  @a`, `reverse sort` and `@a = reverse sort ... @a`, over 3,000
  arrays of 2 to 41 values with many equal keys. The array read from
  inside the block of an in-place sort is unchanged throughout (12
  elements).
- **`sort` of none and of one value never calls the block**; nested
  sorts, a sort in a sub called from a sort block, a `map` in a sort
  block and a sort in a `map` block give `$a`, `$b` and `$_` back.
- **`map` copies what its block gives**: `map { $y++; $y }`, `map {
  $z += $_; ($z, $z) }`, an element stepped in the block, an array
  pushed to in the block (4 programs).
- **Context is syntax** (about 75 calls recorded with `wantarray`):
  the last statement of a `map` block is called for a list, of a
  `grep` and a `sort` block for one value; `join`'s separator for one,
  its list for a list; `reverse`'s and a `for`'s list for a list; the
  modifier's statement for none; `return map` and a last-statement
  `map` are lists whatever the sub was called for. D18's shapes: 47
  `return`s tried, and every one that gives a scalar call something
  other than its one value is on the list (a comma list, a slice of
  two, `(@a)`, `@a ? @a : ()`, `+(1, 2)`, `((1, 2))`, `(c())[0, 0]`);
  `(LIST)[N]`, `(c())`, `(7,)`, `@a || 0`, `scalar(...)` are one value
  either way.
- **`$_` as a bound copy** (about 30 programs): nested binders, the
  outer `$_` after an inner one, as an operand on both sides of an
  inner `map`, in a sub called from a block that runs its own `for`,
  in a default, under a modifier inside a block.
- **A call's values are copies**: `(ret(), push(@a, 9))`, `for my $x
  (ret())` with the loop changing the file's array, a last-statement
  `@a` and `$v`, an array handed to a slurpy and changed by the sub.
- **Where one value is wanted** (Q3): the count of `grep` and `map`
  under `if`, `.`, `!`, `+`, and with a list of calls.
- **Parsing**, about 130 shapes: `sort map`, `sort reverse`, `sort
  grep`, `reverse sort`, `sort { } (@x)[0 .. 1]`, a list operator
  taking everything to the end of its list, `join ",", map { } grep {
  } ...`, `say for reverse 1 .. 3`, the modifier's bare list, a
  trailing comma. Nothing beyond sections 1 to 3.

## Not settled

- W6, and the `last for` and slurpy holes: whether the proposal's
  words already refuse or settle them is the builder's reading, not
  something perl can answer.
- W3's amendment: I did not look for a third route by which an empty
  slot shows (`exists` and `delete` are not in the language; `reverse`
  in place, `join`, `for`, a copy and a slurpy do not show one).
- Not attacked: perl's merge itself against a port (there is no port),
  the 32-bit cut of a block's value beyond the proposal's own rows,
  and strings past ASCII under `sort` with no block.
