# The review of step 9's proposal, arrays and lists

2026-11-25, by a reader who didn't write the proposal (`docs/PLAN.md`,
"9. Arrays and lists"), before anything was built. The question was
the rule for a large step: a program the proposal accepts (with Q1(a),
Q2(a), Q3(a), Q4(a)) that runs without a fault and prints what perl
5.42.0 doesn't; or one it accepts that perl refuses or warns about.

Everything below about perl was run under `/opt/perl-5.42/bin/perl`
(5.42.0), plain, from a file that begins `use v5.42;`. The programs
cited are in this directory, named by finding, and `outputs.txt` has
perl's stdout, stderr and exit status for every one. Nothing of step 9
exists, so "the build would" is a reading of the proposal's text and
of the obvious build: a list is a row of values copied as it is built,
left to right; an element is read where it stands; a foreach walks a
copy with the arrays its list names frozen.

**Eleven ways to be WRONG (A1 to A11), five kinds of program the
wording accepts that perl refuses or warns about (B1 to B5), eight
sentences about perl that are false or true only for their example
(C1 to C8), and twelve holes in the test plan (D1 to D12).** What
held is in E: counts in 29 positions, 60 ranges, 53 `splice` calls,
Q4(a) in 14 positions, T155, T156, and "a value has no past" on
443,205 comparisons.

One line covers A1 to A4, A7 and A8: **the proposal's rule is stated
for elements and for `foreach`, and perl's lists hold every container:
scalar variables, whole arrays, slices, `$#a`, and the targets of an
assignment.** Q1's walk and the freeze are the right two tools; each
needs its list of shapes widened, and the order of evaluation written
down per form, because three forms don't run left to right.

## A. WRONG under the proposal as written

### A1. A scalar variable in a list is read when the list is used

`A1-scalar-in-list.pl` (perl: stdout below, stderr empty, exit 0):

```perl
my $x = 1;
sub bump() { $x = 9; return 5 }
my @b = ($x, bump());          # 9 5
say $x, bump();                # 95
push @a, $x, bump();           # 9 5
my ($p, $q) = ($x, bump());    # 9 5
for my $y ($x, bump()) { say $y; }   # 9, 5
@b = ($i, $i++);               # 2 1   ($i was 1)
@b = ($i, ++$i);               # 3 3
@b = ($i, $i = 7);             # 7 7
@b = (($x) x 2, bump());       # 9 9 5
@b = (($x, 0)[0, 1], bump());  # 9 0 5
@b = ((1 ? $x : 0), bump());   # 9 5
```

The proposal: "A list is a row of values, copied as it is built." Built
left to right and copied, every line above has 1 where perl has 9 (and
`1 1`, `2 3`, `3 7` for the three `$i` lines). No fault, no refusal:
Q1 is about "an element", Q2 about a foreach whose "block, or a sub
the block calls, can assign a variable named in its list", and the
assignment here is in the list itself. D14 already reads `$x + bump()`
late and D73 reads `f($x, bump())` late; a list is the same thing
again, and it goes through a list repeat, a list slice and `? :`.

**Reading:** WRONG under the reading the text most easily gives. (If
"scalar variables are read when their operator runs" is meant to carry
over, with the list's user as the operator, then the text has to say
so, and say it for `x`, a list slice and a nested list too, where a
build will naturally copy.)

Way out, in order: agree (a list item that is a variable itself, in
D14's sense, is carried as a place and read when the list is consumed:
what D73 does for arguments); or refuse, by Q1's walk, a list in which
a later item can assign a scalar variable an earlier item names (D57's
rule for a row of dots, said for a row of commas). The second is one
rule for A1 and A2.

### A2. A whole array or a slice in a list is its elements, read late

`A2-array-in-list.pl` (stderr empty, exit 0):

```perl
my @a = (1, 2, 3);
sub chg() { $a[0] = 50; return 5 }
my @b = (@a, chg());            # 50 2 3 5
say @a, chg();                  # 50235
@b = (@a[0, 1], chg());         # 50 2 5
@b = ($a[0], chg());            # 50 5
say $a[0], chg();               # 505
for my $x (@a, chg()) { say $x; }   # 50 2 3 5
```

Q1(a) refuses "an element used in an expression whose later part can
change its array", and lists what a later part is: "the other operand,
a later argument, a default of the sub being called, a later piece of
a row of dots". Not named: a later item of a list (an array's, a
`push`'s, `say`'s, a list assignment's right side, a foreach's), and
not named as the thing read: a whole array or a slice. The foreach is
the sharpest: `chg` runs while the list is being built, before the
freeze, so the freeze doesn't see it either. The build prints 1 where
perl prints 50, six times.

(`(@a, grow())` with a `push` in `grow` is the old count in perl too:
the last line of the file. A store shows; a resize doesn't; `@a = ()`
in the later item prints freed values and `Attempt to free
unreferenced scalar`.)

**Reading:** the most easily given. Way out: Q1's refusal, with "an
element" made "an element, a slice or an array", and "a later part"
made "anything the expression or list works out after it".

### A3. `=` runs the target's index after the right side, and reads the right side after that

`A3-store-order.pl` (stderr empty, exit 0):

```perl
$a[$i] = ($i = 2);                    # stores at 2:      1 2 2
$a[$i++] = $i;                        # @a = (7,7,7):     1 7 7
sub ix() { $g = 8; return 1 }
$a[ix()] = $g;                        # $g was 7:         1 8 3
sub bump() { $a[0] = 99; return 1 }
$a[bump()] = $a[0];                   #                   99 99 3
($a[ix()], $q) = ($g, 1);             #                   1 8 3
($a[bump()], $q) = ($a[0], 0);        #                   99 99 3
($i, $a[$i]) = (1, 5);                # $i was 0:         5 2 3 1
```

The proposal: "An assignment needs nothing new: its right side runs
first, as now", and for a list assignment "The right side is finished
first." It isn't finished: its calls have run, but a variable or an
element it names is read when the store happens, after the left
side's index expressions. An index is the first thing a program can
put *between* the right side and the store, so nothing before step 9
could see this.

- `$a[bump()] = $a[0]`: Q1(a) reads the element where it stands, 1,
  and refuses nothing (the index of the target is not one of its
  "later parts"). The build stores 1; perl stores 99. **WRONG under
  any reading.**
- `$a[$i++] = $i` and `$a[ix()] = $g`: right if the build keeps the
  right side as a place until the store (D14), WRONG (0 and 7) if
  "runs first" is built as "its value is taken first".
- `($i, $a[$i]) = (1, 5)`: perl works out every target's index before
  it stores anything. A build that stores target by target puts 5 in
  `$a[1]`. WRONG under the easiest reading of "one array last, which
  takes the rest" and nothing said about when indexes run.

Also the "Break it on purpose" list has "its index worked out after
the right side" as a breakage. For `=` that is perl's order (first
line above); see C3.

Way out: agree on the order (right side's calls, then every target's
index left to right, then the reads and the stores), and put the
target's index expressions among Q1's "later parts" and A1's.

### A4. A compound assignment works its index out first, and its target is the container

`A4-compound-order.pl` (stderr empty, exit 0):

```perl
$a[$i] += ($i = 2);        # @a = (1,2,3), $i = 0:   3 2 3   (index 0)
$a[$i] .= ($i = 2);        #                         12 2 3
$a[$i] ||= ($i = 2);       # @a = (0,2,3):           2 2 3
$a[0] += shift(@a);        # @a = (1,2,3):           two left: 2 3
$a[$#a] += pop(@a);        #                         two left: 1 2
$a[5] //= push(@a, 1);     # @a = ():                seven: $a[5] is 7, $a[6] is 1
$a[0] .= clr();            # clr empties @a:         none left
```

All eleven operators were run (`+= -= *= /= %= **= .= x= ||= &&=
//=`): the index is worked out before the right side, the opposite of
`=`. The proposal has one sentence for both: "An element is assigned,
stepped and worked on as a variable is", and "its right side runs
first". Built that way `$a[$i] += ($i = 2)` adds to `$a[2]`: `1 2 5`.

And the target is the element perl found *before* the right side ran,
so when the right side resizes the array perl stores into an element
that has left it: `$a[0] += shift(@a)` leaves `2 3` (the sum went to
the element that was shifted off), where a build that reads the
element after the right side has `3 3`; `$a[$#a] += pop(@a)` leaves
`1 2` where the build has `1 5` or `1 2 3`. Q1(a) refuses none of these: "An assignment
needs nothing new". `$a[0] ||= pop(@a)` also warns at run time,
`Useless assignment to a temporary` (`A4b-compound-warns.pl`), and
leaves the array empty where a build leaves one element.

**Reading:** the order is WRONG under the reading the text most easily
gives; the resizing right side is WRONG under any.

Way out: agree on the order (index, then right side, then read, work,
store); and Q1's refusal for a compound assignment, `||=`, `&&=`,
`//=` or a step whose target is an element and whose right side can
resize or assign that array. (A store by the right side, `$a[0] +=
chg()`, is 51 in perl and in a build that reads the element after the
right side: that one can be agreed with.)

### A5. `&&=` past the end makes the array longer; before the start it dies; and the target is checked before the right side runs

`A5-andand-makes.pl`: `my @a; $a[5] &&= 1; say scalar(@a);` prints
`6`, stderr empty, exit 0.

`A5b-andand-dies.pl`: `my @e; $e[-1] &&= 5; say "after";` prints
nothing; stderr `Modification of non-creatable array value attempted,
subscript -1 at ... line 3.`; exit 255.

`A5c-fault-order.pl`: `$a[-9] += p(5);` where `p` prints its argument:
stdout empty, the same death, exit 255. (`$a[-9] = p(5)` prints 5 and
then dies.)

The proposal: "Reading past either end is undef, in silence, and the
array is not made longer", "Storing before the start is a fault", and
`$a[5] //= 7` as an element "worked on as a variable is". `&&=` on an
undef reads and doesn't store, so the build prints `0`, then `after`:
WRONG twice, under any reading. And under A4's order the build runs
`p` and prints `5` before its fault, so its stdout is not a prefix of
perl's.

Way out: a compound assignment or a step makes its target first, as
perl does: past the end the array grows to hold it (undef), before
the start it faults, both before the right side runs.

### A6. An element or slice past the end is made by a foreach, and a slice by a call

`A6-foreach-makes.pl` (stderr empty, exit 0):

```perl
my @a;
for my $x ($a[5]) { say scalar(@a); }   # 6
say scalar(@a);                         # 6
for my $x (@b[5, 6]) { }
say scalar(@b);                         # 7
f($c[5]);      say scalar(@c);          # 0
f(@c[5, 6]);   say scalar(@c);          # 7
my $r = $d[5] // 0; my @t = @d[5, 6];
say scalar(@d), " ", scalar(@t);        # 0 2
```

`A6b-foreach-dies.pl`: `my @a; for my $x ($a[-5]) { say "in"; } say
"after";` prints nothing and dies, `Modification of non-creatable
array value attempted, subscript -5`, exit 255.

The proposal: "Reading past either end is undef, in silence, and the
array is not made longer", and a foreach is over "the array, a slice
or an element of it". The build prints 0, 0, 0, 0, 0 for the 6, 6, 7,
0, 7, and runs the loop over `$a[-5]`. WRONG under any reading. (An
element as an argument doesn't grow the array; a slice as an argument
does; a plain read, `//`, `defined`, `push`'s list, a list
assignment's right side and a list repeat don't: 8 shapes run.)

Way out: fault, `an element past the end in a foreach's list` and the
same for a slice in a foreach or a call when an index is past either
end (the array's length is known when the list is built). Agreeing
means growing a frozen array.

### A7. Lists that "freeze nothing" and walk the array

`A7-freeze-misses.pl` (stderr empty, exit 0). In each, the block
stores 9 and the loop variable shows it:

```perl
for my $x ((@a) x 2)     { $a[0] = 9; say $x; }   # 9 2 3 9 2 3
for my $x ((@a)[0, 1])   { $a[0] = 9; say $x; }   # 9 2
for my $x ((@a, 5)[0])   { $a[0] = 9; say $x; }   # 9
for my $x (@a && @b)     { $b[0] = 9; say $x; }   # 9
for my $x ($a[0] = 5, ++$a[1], $a[2] .= "x") { $a[0] = 9; $a[1] = 9; $a[2] = 9; say $x; }   # 9 9 9
for my $x ($#a)          { push @a, 7; say $x; }  # 3
```

`A7b-substr-foreach.pl`: `for my $x (substr($s, 0, 1)) { $s = "zzz";
say $x; }` prints `z`; and `for my $x ($p = 5, $p += 1, ++$p, $p++) {
say $x; $p = 100; }` prints 8, 100, 100, 7.

`A7c-last-index-argument.pl`: `f($#a, grow())`, where `f` returns its
first parameter and `grow` pushes, is `3` for an array of three;
`f(scalar(@a), grow())`, `$#a + grow()` and `($#a, grow())` are the
value before.

The proposal: "an array is frozen while a `foreach` is over a list
that names it: the array, a slice or an element of it, through
brackets, `? :` and `||`. A range, a call and any other value freeze
nothing." A list repeat, a list slice, the right of `&&`, an
assignment to an element and `$#a` are "any other value": the build
copies, the store is allowed, and it prints 1 2 3 1 2 3, 1 2, 1, 4,
5 3 3x, 2. And "An array's count is a value at once" is true of `@a`
and `scalar(@a)` and not of `$#a` where perl wants a place (an
argument, a foreach's list): the build hands `f` 2.

**Reading:** `(@a) x 2`, `&&`, the assignments and `$#a` are WRONG
under any reading; `(@a)[0, 1]` under the reading that "a slice of
it" means `@a[...]`.

Way out: freeze by **every array named anywhere in the foreach's
list**, whatever it stands in (it costs only loops that were going to
fault or be WRONG, and it is one sentence); the same for Q2, "a
scalar variable named anywhere in the list", which `substr($s, 0, 1)`
needs. For `$#a` as an argument: Q1's refusal, with `$#a` read as an
element is.

### A8. A list slice works its indexes out before its list

`A8-list-slice-order.pl` (stderr empty, exit 0):

```perl
sub p($v) { print "<", $v, ">"; return $v }
say((p(10), p(20))[p(1)]);        # <1><10><20>20
my $i = 0;
say(($i, 5)[$i++]);               # 1
my @a = (1, 2, 3);
sub sh() { shift(@a); return 0 }
say((@a)[sh()]);                  # 2
```

Nothing in the proposal gives an order for `(LIST)[LIST]`, and the
generated C is "operands left before right": `<10><20><1>20`, `0`,
`1`. WRONG under any reading. Every other new form was run with the
same printing sub and is left to right as written: `(LIST) x N`, a
range, `splice`'s arguments, `push`'s, `@a[LIST]` (indexes, then the
array), `$a[I] = V` (V, then I: A3), `$a[I] += V` (I, then V: A4), a
list assignment (the right side, then the targets' indexes).

Way out: agree; the indexes first.

### A9. A slice of an empty list is empty

`A9-empty-list-slice.pl` (stderr empty, exit 0):

```perl
my @e;
my @b = (@e)[0, 1];   say scalar(@b);   # 0
@b = (@e)[0];         say scalar(@b);   # 0
@b = (1, 2, 3)[5, 6]; say scalar(@b);   # 2
@b = (1, 2, 3)[5];    say scalar(@b);   # 1
sub f($x = "d", $y = "d") { return $x . $y }
say f((@e)[0]);                         # dd   (no argument at all)
sub first() { return (@e)[0] }
my @c = first();      say scalar(@c);   # 0
@c = (first(), first(), 5); say scalar(@c);   # 1
my $v = first();      say defined($v) ? 1 : 0;   # 0
```

The proposal: "A slice ... of a list, `(LIST)[LIST]`: the elements at
those indexes, as values", and "`(LIST)[N]` with one index is that
element". An index past the end of a list that has values is undef;
any index into a list with none is nothing. So `(@e)[0]`, the natural
"first, if any", is one undef to the build and no value to perl: a
count is off by one, `f` gets an argument it shouldn't (`d` and a
fault for undef, or WRONG where the parameter is only counted), and
`return (@e)[0]` gives a list one value. WRONG under any reading.

Way out: agree (an empty list sliced is empty, in a list; it is undef
where one value is wanted, as now).

### A10. `splice` with an offset or a length too large for a whole number

`A10-splice-wraps.pl` (stderr empty, exit 0), each on `(1, 2, 3, 4,
5)`, printing how many came out and how many are left:

```perl
splice(@a, 0, 1e30);                   # 4 1
splice(@a, 1e30);                      # 1 4
splice(@a, 0, 9223372036854775807);    # 5 0
splice(@a, 0, -1e30);                  # 0 5
```

T153 again: a Num past the integers wraps to -1. The proposal's
faults are "an index ... too large to be one (T153)" for an element
and "`splice` past the end (perl warns) or before the start" for
`splice`; a length past the end is legal and common (`splice(@a, 1,
99)`), so a build clamps `1e30` and takes all five. WRONG under the
easiest reading.

Way out: fault; `splice`'s offset and length each go by the index
rule (a whole number by `substr`'s rule, not undef, not too large).

### A11. A foreach over one range is not the range as a list

`A11-foreach-range-low.pl`:

```perl
my $lo = -9223372036854775807 - 1;
my @r = ($lo .. $lo + 1);
say $r[0], " ", $r[1];
for my $i (0, $lo .. $lo + 1) { say $i; }
for my $i ($lo .. $lo + 1) { say $i; }
say "not reached";
```

stdout:

```
-9223372036854775808 -9223372036854775807
0
-9223372036854775808
-9223372036854775807
```

stderr `Range iterator outside integer range at ... line 7.`, exit 255.

The proposal: "a `foreach` over one range counts and builds nothing",
the same values as the list. perl's foreach checks its ends as
doubles: an Int end from -2^63 to -2^63 + 512 dies
(`A11b-foreach-range-edge.pl`: -2^63 + 513 is walked, -2^63 + 512
dies), though the same range as a list, or beside another item in the
foreach's list, is fine. And `for my $i (5 .. -1e19)` dies where `(5
.. -1e19)` is an empty list (`A11d`; the proposal faults both, which
is right). The build walks two values and prints `not reached`. WRONG
under any reading, at one edge.

The other edge holds and is a trap for the counter
(`A11c-foreach-range-high.pl`): `9223372036854775805 ..
9223372036854775807` is three values and the loop ends; `i <= hi;
i++` in C never ends there, or is undefined.

Way out: fault, in a foreach over one range, on an end below -2^63 +
513; a fault test at each edge; and the top edge as a `same` test.

## B. Accepted by the proposal; perl refuses or warns

(The files `B4` to `B8` are cited by name under B4 below; the file
numbers are not the finding numbers.)

### B1. A slice with one index warns, by a rule on its spelling

`B1-slice-of-one.pl`: `@a[0]`, `@a[-1]`, `@a[$j]`, `@a[$j + 1]`,
`@a[$#a]`, `@a["0"]`, `@a[true]`, `@a[ 0 ]` each warn as the program
compiles, `Scalar value @a[0] better written as $a[0]` (or `@a[...]`);
exit 0. `B1b-slice-of-one-silent.pl`: `@a[0,]`, `@a[(0)]`, `@a[$j *
1]`, `@a[$j ** 1]`, `@a[$a[0] - 4]`, `@a[f()]`, `@a[@b]`, `@a[0 ..
0]`, `@a[0.5]`, `@a[!$j]`, an index on a line of its own, and
`(@a)[0]` don't. 55 spellings were run: perl warns when the text
between the brackets is only letters, digits, `_`, blanks, tabs and
`$ # + - ' "`, and what it holds isn't a list.

The proposal: "A slice, `@a[LIST]`", with no refusal for one index.
Way out: refuse `@a[...]` when the index list is one item that is not
an array, a slice, a range, a call or in brackets of its own, with
"write `$a[...]`" (wider than perl's rule, and sayable); or perl's
rule on the characters, exactly.

### B2. `length(@a)` warns and `defined(@a)` doesn't compile

`B2-length-of-array.pl`: `say length(@a);` warns `length() used on @a
(did you mean "scalar(@a)"?)` and prints 1. `B2b-defined-array.pl`:
`Can't use 'defined(@array)' (Maybe you should just omit the
defined()?)`, exit 255.

The proposal: "an array wherever one value is wanted" is its count.
`uc`, `lc`, `ord`, `chr`, `substr`, `index`, `x`, `!`, `-`, `//` and
the arithmetic and comparison operators do take the count in silence
(`E-counts.pl`). Way out: refuse an array as the argument of `length`
and `defined`, by name.

### B3. A comma after an array assignment is perl's comma operator

`B3-comma-statement.pl`: `my @a = 1, 2, 3;` is one element and two
warnings (`Useless use of a constant (2) in void context`); `my ($x)
= 4, 5;` the same. The proposal's `LIST` on the right of `=` is not
said to need its brackets (`push @a, 1, 2` doesn't). Way out: refuse a
comma at the end of an assignment's right side; `my @a = 5;`, `my @a
= @b;` and `my @a = f();` are silent in perl and may stay.

### B4. Shapes that are syntax errors, and a parser of `(LIST)[LIST]` may take

`B6-bracket-after-call.pl`: `say(1, 2)[1];`. `B6b`: `say (@x)[1];`.
`B6c`: `shift(@a)[0]`. All `syntax error ... near ")["`, exit 255
(`f(1)[0]`, `pop(@a)[0]` and `scalar(@a)[0]` the same). Today `[` is
"not in the language yet", which is what refuses them. Once a
bracketed list may be followed by `[`, each call's own brackets and
`say`'s must not be. `say((1, 2)[0]);` and `say +(@x)[1];` are fine.
`$a[0][0]` and `(1, 2)[0][0]` compile and die for strict refs: refuse.

Also: `my ($x, $x) = (1, 2);` warns (`B4-my-twice.pl`), as T141 has it
for parameters; `(1, 2) x -1` warns `Negative repeat count does
nothing` (`B5`), as the string `x` does; `push @a;` and `unshift(@a);`
warn `Useless use of push with no values` (`B8`: the proposal refuses
them; `push @a, ();` is silent and is a value to add); `$#{x}` warns
and `$# x` is fatal (`B7`); `@a++`, `@a += 1`, `@a ||= (1)`, `@a x=
2` don't compile.

### B5. `$a[0] ||= pop(@a)` warns as it runs

In A4: `Useless assignment to a temporary`. Refused by A4's way out.

## C. Statements about perl in the proposal that are false or imprecise

- **C1. "Reading past either end is undef, in silence, and the array
  is not made longer."** True of a plain read. False in a foreach's
  list, for a slice in a call, and for `&&=` (A5, A6); and before the
  start, in a foreach or under a compound assignment, perl dies.
- **C2. "The right side is finished first." / "its right side runs
  first, as now."** Its calls run first. What it names is read after
  the targets' indexes have run (A3). For a compound assignment the
  target comes first (A4).
- **C3. Break it on purpose: "its index worked out after the right
  side".** For `=` that is perl: `$a[$i] = ($i = 2)` stores at 2. It
  is a breakage only for the compound assignments.
- **C4. "`splice` past the end (perl warns)".** Only when a length is
  given. `C1-splice-past-end.pl`: `splice(@a, 6)` and `splice(@a,
  2147483648)` on five elements are silent and remove nothing;
  `splice(@a, 6, 0)` and `splice(@a, 6, 0, 7)` warn. The fault is
  right for both (the silent one is a no-op perl thinks worth a
  warning elsewhere), but the reason given isn't.
- **C5. "An array's count is a value at once."** `@a` and
  `scalar(@a)`, yes, in 7 positions. `$#a` is a value at once as an
  operand and in a list, and a place as an argument or in a foreach
  (A7).
- **C6. "through brackets, `? :` and `||`."** Through `||` the loop is
  over the *count* of the left array (`C2-or-in-foreach.pl`: `for my
  $x (@a || @b)` runs once, with 3) and over the right one itself.
  `&&`, `//`, `and`, `or` are the same shape and aren't named.
- **C7. "A range, a call and any other value freeze nothing."** A7.
- **C8. "`(LIST)[N]` with one index is that element."** Not when the
  list is empty and a list is wanted (A9).

T155 (`for my $x ()` doesn't compile) is so; `for my $x (())` compiles
and runs no times, so the refusal is of the empty brackets, not of an
empty list.

## D. Holes in the test plan

- **D1. Order of evaluation, per form.** A printing sub in each
  operand of every new form: the list slice (A8), `=` against the
  compound assignments (A3, A4), a list assignment's targets, `splice`,
  `x`, a range. Nothing in "The build" asks for one.
- **D2. A list repeat where one value is wanted.**
  `D1-repeat-in-scalar.pl`: `(1, 2) x 2 x 2` in a list is one value,
  `2222` (the inner repeat is scalar: its last value, repeated);
  `((1, 2) x 2) x 2` is eight; `-(1) x 3` is one, `-1-1-1`; `($n + 1)
  x 3` is three. "A comma list refused where one value is wanted" has
  to reach the left of an `x` that is itself not in a list.
- **D3. A list assignment that ends a sub.** `D2-last-statement.pl`:
  `sub f1() { @g = (7, 8, 9) }` is 3 to a scalar and three values to a
  list; `sub f3() { ($p, $q) = (4, 5, 6) }` is 3 and *two*. Step 8
  gives a scalar assignment that ends a sub its value. Q3(a) says a
  list assignment "is a statement": say that it has no value as a last
  statement (D18's fault), and test it. The same for `return` with
  anything list-shaped behind `? :`, `||` or brackets: `return $c ?
  @a : 0`, `return (@a)[0]` (A9), `return ()`.
- **D4. Targets.** `D3-targets.pl`: perl takes `(($x), $y)`, `(($x,
  $y), @a)`, `(+$x, $y)`, `($x ? $x : $y, $a[0])`, `($x, $#a)`, `my
  ($m, @b, $z)` and `my (@c, @d)` in silence. Each needs a refusal
  test, or to be agreed with; "one array last" covers two.
- **D5. T156 for each shape of `my`.** `D4-file-arrays.pl`: `my ($n,
  @b);` stores nothing (2 after a sub filled it); `my ($m, @c) =
  (5);` empties `@c`; `my ($s, $t) = (1);` stores undef in `$t`.
- **D6. Lexing.** `D5-lexing.pl`: `$#x# comment` is `$#x` and a
  comment; `$#x -1` is a subtraction; `1..3` is a range, and today's
  lexer says "1..3 is not a number in the language" (the proposal's
  own picture writes `5..7`); `1...3` is the same list to perl, and
  `1.5..3` starts at 1; `$x [1]` is an element of `@x` even when
  there is a `$x`, after `say` too.
- **D7. The freeze: more than "six things that change an array".**
  `=` to an element, eleven compound assignments, four steps, an
  element as a list-assignment target, the array as one, `@a = LIST`,
  `push`, `unshift`, `pop`, `shift`, `splice` (and a `splice` that
  changes nothing), and the growing reads of A5 and A6. Each from the
  block and from a sub, and each in the loop's own list (A2).
- **D8. The freeze given back** through two foreach loops by `next
  OUTER`, `last OUTER` and `return`, and in a sub that recurses over a
  file's array (ran in perl: no surprise; the plan names one loop).
- **D9. Indexes at the edge of the integers.**
  `$x[-9223372036854775807 - 1]`, `$x[9223372036854775807]` and
  `$x[2 ** 31]` read as undef in silence in perl: a build that negates
  or adds the length must not overflow. Nums from 2^63 to 2^64 read
  undef; 2^64 and up wrap (T153).
- **D10. A list repeat's count**: negative (B4), undef (warns),
  fractional (cut), a string, a boolean: the string `x`'s rule, tested
  again for a list.
- **D11. `say` and `print` with a list**: an undef element (perl
  warns: a fault), `say (@x);`, `say(@x);`, `say @x if @x;`, `say @x
  -1;` (the count less one), `say $x[0] -1;` (not a file handle).
- **D12. A1's and A2's rows** in every consumer: array assignment,
  list assignment, `push`, `unshift`, `splice`'s list, `say`, `print`,
  a call, a foreach, a slice's indexes, a range's ends (`$a[0] ..
  chg()` reads the end late; 30 operators and builtins with an element
  first and a store after it were run, and none reads early).

## E. What held

- **Counts** (`E-counts.pl`, 29 lines): an array is its count under
  brackets, unary plus and minus, `!`, `uc`, `ord`, `substr`, `index`,
  either side of `x`, `.`, `==`, `**`, `//`, as an index, as a range's
  end, on the left of `||` and `&&`, and in both arms of `? :` to a
  scalar; `my ($m) = @a` is the first element; `(@a) x 2` to a scalar
  is `33`. T150 and T21 as written.
- **Ranges** (`E-range-table.pl`, 60 rows, perl against the proposal's
  rule): ends cut toward zero, booleans 1 and 0, `-0.0` is 0, empty
  when FROM is past TO, both edges of the integers as a list, `(1 ..
  3) x 2`; every string end is either another thing or a warning, so
  the fault is right. A range is fixed when the loop starts, at both
  ends.
- **`splice`** (`E-splice-table.pl`, 53 rows): every sign of offset
  and length; a negative length past the start removes nothing in
  silence; a replacement list that names the array (`splice(@a, 0, 1,
  @a)`, `splice(@a, 0, 2, $a[1], $a[0])`) is as a copy; undef and
  non-numeric strings warn. Only A10 and C4 came of it.
- **`push`, `unshift`, `pop`, `shift`**: counts returned, undef from
  empty in a list too (one value), `pop(@a) - pop(@a)` left to right,
  `push @a, @a`, `unshift @a, @a`, the rotations. T152: 16 shapes of
  `pop @a OP` and `shift @a OP`; each either doesn't compile or reads
  as `pop(@a) OP`, so "brackets unless nothing follows" refuses
  nothing that differs.
- **List assignment**: about 25 shapes with the right side naming
  what the left changes (`($x, $y) = ($y, $x)`, `($a[0], $a[1]) = ($a[1],
  $a[0])`, `($x, @a) = (@a, $x)`, `@a = (@a, @a)`, `@a = @a[1, 0]`,
  `($a[0], @a) = (9, 8, 7)`, `($x, $x) = (1, 2)`): all as a copy of
  the right side would give, but for A3.
- **Q4(a)** (`E-none.pl`, 14 positions): as the proposal says.
  `(1, none())[1]` is one undef; `1 .. none()`, `$a[none()]`, `(5) x
  none()` and `splice(@a, none())` warn, and are undef faults.
- **T155, T156**, a sub's own array across recursion, a `my @t` in a
  loop's block: as written.
- **Names**: `@x`, `@s`, `@y`, `@q`, `@m`, `@tr` are plain arrays and
  `$s[0]` an element; `my @_` and `my @1` don't compile; `my @ARGV`
  and `my @INC` are lexicals.
- **A value has no past** (`E-past.py`, step 8's with 23 routes
  through an element, a list, `push`/`pop`, `unshift`/`shift`, both
  slices, a list assignment, a swap, `splice` both ways, a foreach, a
  list repeat, a flattened argument): 443,205 comparisons, 0 differ.
- **What the freeze costs** (`E-freeze-costs.pl`, LOUD, perl prints
  what a copy would): doubling in place by an index kept beside the
  loop (`$a[$i] = $x * 2; $i++`); `push` and then `last`; emptying the
  array and then `last`; `pop` on the last round; storing what is
  already there. The first is the common one. Also LOUD and worth
  knowing: `$a[$n / 2]` faults when `$n` is odd, where perl cuts.
