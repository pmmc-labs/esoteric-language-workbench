# Curly

Curly is a cleaned-up Perl 5 with a runtime of its own. A program it accepts is
Perl 5.42 once its annotations are erased, and prints what perl prints
unless it stops loudly first; what Perl has that the language cuts is a
compile error or a fault, never a different meaning. The compiler is
TypeScript run by Node as it is, and emits C that links with a C
runtime. The driver is `curlyc`, and a program is a `.pl` file.

## Status

**Steps 0 to 10 and 11a of [`docs/PLAN.md`](docs/PLAN.md) are done**
(2026-11-24 to 26, all by Fable 5.2). **The language** is `use
v5.42;`, then `use utf8;` and `use open ':std', ':encoding(UTF-8)';`
if wanted, then statements: `say EXPR;` and `print EXPR;` (brackets
or not), `my $x;`, `my $x = EXPR;`, an assignment, `$x++` and its
three kin, a block, `if (...) {...}` with `elsif`s and an `else`,
`unless (...) {...}`, `while (...) {...}`, `until (...) {...}`, `for
(FIRST; TEST; EACH) {...}`, a label before a loop, `last;` and
`next;` with a label or without, `STATEMENT if EXPR;` or
`unless`, `while`, `until`, and from step 8 `sub NAME(PARAMETERS)
{...}` at the top level, a call `NAME(ARGUMENTS)` as a statement or a
value, `return;` and `return EXPR;` in a sub, and `no warnings
'recursion';` with the pragmas. An
expression is a number, a string, `true`, `false`,
`undef`, a variable, brackets, unary `-` `+` `!`, `++` and `--`,
`=` and `+= -= *= /= %= **= .= x= ||= &&= //=`,
`+ - * / % **`, `.` and `x`,
the comparisons (`== != < <= > >= <=>`, `eq ne lt le gt ge cmp`),
`&& || //`, `? :`, `not and or xor`, and the builtins `length uc lc
ord chr defined` (perl's named unary operators, D41) and `substr` and
`index` (in brackets), with perlop's precedence
([`docs/LANGUAGE.md`](docs/LANGUAGE.md)). **A number is an Int (64
bits, signed) or a Num (a finite double)**, and which one an
operation gives is perl's own rule (D35): it is done on whole numbers
when both operands are *integral* (an Int, or a whole Num below 2^53)
and on doubles otherwise; `/` gives a Num, except an Int past 2^53
divided exactly; `**` gives a Num for a base that is a power of two,
an exact Int when the base's bits times the power are at most 64, and
C's `pow` otherwise; `%` cuts a Num to its whole part. **A Str is
Unicode scalar values** (D24, D42), immutable, UTF-8 inside, counted
in characters. **A string where a number is wanted** (D40) is one of
the shapes perl takes in silence, or `not a numeric string`: digits
are the Int; an exponent gives the Int if whole and below 2^53, a
fault if whole and larger, else the Num; a point gives the Num, and a
whole one below 2^53 (`"3.0"`) is *soft*: float arithmetic beside an
integral operand, and a fault if either number or the exact answer
reaches 2^53; and where a whole number is wanted, a string with a
point whose digits before it aren't its number cut down faults
(T103). **perl has two answers in those places, by what was
done with the value before, and a value here has no past**: that is
the reason for every fault that says `two answers` or `two values`,
and for D45, which amends D35: in `+ - *`, an Int of 2^53 or more
that is exactly a double faults beside a whole Num or a string (T92).
**A boolean** (D47) is a kind of its own: the Int 1 or 0 where a
number is wanted, `"1"` or `""` where a string is, in silence, as
perl has it. **undef** (D48) faults where a number or a string is
wanted, printing included; `defined`, `//`, the tests of truth and
`length` take it. **A variable** (D55, D56) is `$name`, ASCII, not
`$a`, `$b` or `$_`; declared by a `my` that begins a statement or
stands in the test of an `if`; seen from the next statement to the
end of its block; and **read when the operator it is an operand of
runs** (D14), as perl reads it: `$x + ($x = 5)` is 10. What is "the
variable itself": `$x`, `($x)`, `+$x`, an assignment, `++$x`, and
whichever operand `|| && // or and ? :` give; `$x++` and everything
else are values. **`++` and `--`** (D52) go by what the variable
holds: an Int by one or `integer overflow`; undef to 1 or -1; a
boolean to the Int; a Num as `+ 1` would (`--` always leaves a Num);
a string as its number, and then a Num; and a fault where perl has
two answers by the variable's past (a string of digits that begins
with a zero under `++`, a whole-number string at 2^53, `--` on a
whole Num reaching 2^53), and on a Num of 2^53 or more, where perl
warns `Lost precision` (T130). An undef on the
left of `+=`, `-=` and `.=` is 0 or `""`, as in perl. **A loop**
(D58 to D62) tests first, a statement under `while` or `until` too;
a `for`'s first and third parts are assignments and steps with
commas between (the only commas there are), its first a `my` too,
which is one variable for the whole loop; a `my` in a loop's block,
or in a `while`'s or `until`'s test, is new each time round (T119).
`last` and `next` are statements, taking a label, an `if` or an
`unless` and nothing else; a label is on a loop, in capitals, and a
`last` or `next` is tied to its loop as the program compiles. **A
bare block is no loop** (D59): to perl it is one that runs once, and
a `last` with no label inside one leaves only the block, so that is
refused. A fault in a loop's test or its third part names the loop's
line. **Memory** (D26, D63 to D66) is collected: a string the program
can no longer reach is freed, and nothing a program prints can tell.
`out of memory` is a fault. Every compiled program reads three
environment variables as it starts, each a whole number and 0 or
unset for off: `CURLY_GC_STRESS=N` (a collection at every Nth
allocation), `CURLY_GC_POISON=1` (a collected string's memory is
never used again), `CURLY_HEAP_CAP=BYTES`. **Comparison** (D49) is D35's question again: two
integral operands exactly, otherwise as doubles; strings character by
character, a number as it prints. Truth is perl's (false: undef,
`false`, zero, `""`, `"0"`). `&& || // and or` give an operand and
work the right one out only if it is wanted; `? :` works out one
branch. **Faults** (D13): `integer overflow`, `float overflow`, `not a
number` (D37), `division by zero`, `modulus by zero`, `modulus of a
number outside the integers`, a whole Num from 10^15 up to 2^53 made
a string (D36: `+ 0` makes the Int); `not a numeric string`, the
two-answer faults above, a minus before a string that starts with
`+`; `substr outside of string`, `negative repeat count`, `repeated
string too long`, `not a character`, `uc` or `lc` of a character past
ASCII, a whole number wanted that isn't an Int; `undef where a number
is wanted`, `undef where a string is wanted`; printing a character
past ASCII without `use open` (D39), or a noncharacter. A fault names
the line its statement starts on (D34).
**Literals**: numbers as D38 (decimal; `1.5`, `.5`, `1e3`; `0x1F`,
`0b101`, `0o17` up to 32 bits; `_` between digits); strings as D43
(`'...'`; `"..."` with `\n \t \r \f \b \a \e \0`, `\\ \" \$ \@`,
`\xHH`, `\x{...}`, octal, `\o{...}`, `\N{U+...}`, a backslash before
a punctuation mark). **Refused**: a leading zero (`017`), `1.`, a
literal too large for its kind, a number hard against a letter, digit
or dot (T62, T78); an unescaped `$` or `@` in double quotes (T34), an
escape perl warns about or that needs interpolation (T86, T95); a
character past ASCII outside a string or a comment, or on any line up
to the one that says `use utf8;` (T73); a file that isn't UTF-8; `say
(1 + 2) * 3;` (T25); `say`, one space and a bracket, unless the
brackets close on that line counted as text, one in a string too, and
`;` follows (T76, T100); `(...) x N` as the whole argument of `say`,
which is a list to perl (T101); `"ab" x3` (T57); `substr` without
brackets; `length - 5` (T94); two comparisons of one row with no
brackets, which perl chains (D50, T108); bare `undef` before anything
perl could take for its argument (T105: `undef * 2` is undef of a
glob); `and`, `or`, `xor` after `say`'s argument (T106), any word
operator bare in a list of arguments (T109), an operator that binds
tighter than `not` after `not (...)` (T107), all D51; an unbracketed
`!` on the left of a comparison, which perl 5.42 warns of (T115);
`^^`, `~~`; any
pragma or spelling of one outside D16's list; `--`,
every operator of perl's that isn't in, as the longest token perl
would take (T27); a line that starts `#!` (D33). **Refused at step
5**: a variable first after `say`, `print`, `substr(` or `index(`, a
blank, and what could begin a value, `say $x -1;` (a file handle, to
perl: T111, T125); `=` with a constant on its right, or what perl
folds to one (`0 && $y`), where a value is tested for truth, through
`!`, `not` and `+` too (D53, T112); `$x =- $y` (T127); a name past
251 characters (T126); a modifier after `say (...)` that is not on
the bracket's line (T128); `unless` with `else` or `elsif`
(D54); `${x}`, `$ x`; a second `my` in a scope, a variable with no
`my`, `my` under a modifier or where it may not be reached; a
statement that only has a value, or two joined by a word operator
(`$x = 1 and $y = 2;`); an assignment to anything but a bare
variable; a step on anything but a variable; an empty bare block
(T116); and **D57**: a concatenation in which a later
piece changes a variable an earlier piece reads, because perl joins a
row of dots as one operation and reads each piece late (`$x . "a" .
($x = 5)` is `5a5`, T117), and a `.=` whose right side is an
assignment of a concatenation, which perl 5.42 never makes (T129).
**Refused at step 6**: `last` or `next` outside a loop, with a label
no loop round it has, or with no label and a bare block nearest
(D59); either as a value, `$done and last;`, or followed by anything
but a label, `;`, `if` or `unless` (T120); a label in small letters,
with a blank before its colon, or on anything but a loop (D61);
`while ()` (T123); `do {...} while` (D58); a `for` with no
semicolons, and `foreach` (steps 9 and 10); a comma in a `for`'s
test, a part of a `for` that only has a value, a `my` in its test or
third part (D60); `redo`, `continue`.
**The compiler**: `lexer.ts` (the whole file, a line and column on
each token, every character checked there; it knows whether a value
or an operator comes next from the token before, T90), `parser.ts`
(precedence climbing over perlop's table), `ast.ts` (`int`, `num`,
`str`, `constant`, `var`, `my`, `assign`, `step`, `unary`, `binary`,
`ternary`, `apply`, `invoke`, and step 11a's `interp`; `use`, `pragma`, `call`, `do`, `block`, `if`,
`sub`, `return`,
`while`, `for`, `foreach`, `jump`; and step 9's `array`, `myarray`,
`elem`, `lastindex`, `list`, `slice`, `arrayop`, `listassign`, and step
10's `listop`, `binder` and `sort`),
`resolver.ts` (each variable to its `my`, and each `last` and `next`
to its loop, by number; it runs before the checker), `checker.ts`, `codegen.ts`, `names.ts` (the statements, the builtins
by shape, the constants, the pragmas, and all 25 rows of perlop's
table, of which fifteen are live, each operator with what the passes
need of it), `errors.ts`, and the driver `bin/curlyc.ts` (D3,
D29). **The generated C** is straight-line (D31): each operation a
statement with its result in a temporary, operands left before right,
the statement's line stored in the context first; a Num literal goes
over as its 64 bits, a string literal as a constant with its bytes
and characters counted; an operand that may not be worked out (the
right of `&&`, a branch of `? :`) is an `if` round its statements; a
variable is a C local in the C block of its scope, never copied to a
temporary, and where an operator gives one of two operands the C
keeps a pointer to it, the statement's temporaries all declared at
its top; a loop is `for (;;)` with its test inside it and its block
in a C block of its own, and `last` and `next` are each a `goto` to
a label after the loop or at the end of its block, the only jumps
there are but for `return`, which puts its value in a C local and
jumps to the one place its function closes its frame. **A sub is a C
function**, handed its context and a pointer to each argument, or
NULL; the file's variables are the first slots of the file's frame,
reached from a sub through the context (`g[n]`); the line is stored
again after every call. **Every variable and temporary is a slot of its
function's frame**, `f[n]`, the variables first, each at its depth
among those in scope, then the temporaries, which each statement
numbers again from the first (D66). **The runtime**:
the two-word value (D25),
the context first in every call (D28), every operator
checking its operands' tags. **The collector** (step 7) is a mark
over every slot of every frame and a sweep of the heap's list, in
`rt_collect`; a collection can happen only inside `str_new`, before
the string is made. **The rule the whole runtime keeps: a value
still in use is in a slot whenever a collection can happen.** So a
runtime function allocates at most once, as the last thing it does,
or opens a frame of its own (none needs to yet; lists will, at step
9); a number as a string is a scratch string on the C stack and is
never returned; and a string is read through `alive`, which stops
with `internal:` (exit 2) if it was collected, and is called again
after an allocation by the four functions that read an operand
then. **Tests**: golden 000 to 009 (step 0);
010 to 026 from `t/models/arith.py` and 030 to 038 by hand (step 1);
040 to 078 from `t/models/num.py` and 080 to 093 by hand (step 2);
100 to 169 and 180 to 191 from `t/models/str.py` (about 15,000 lines
on which the model and perl agree, and 62 programs that each fault
once), 170 to 179 by hand with perl's answers, 200 to 237 refusals
by hand (step 3); 300 to 307 and 320 to 359 from `t/models/bool.py`
(about 13,000 lines, and 40 programs that each fault once), 360 to
364 by hand with perl's answers, 380 to 407 refusals by hand (step
4); 500 to 504 and 520 to 546, 550 to 554 from `t/models/var.py`
(about 5,000 lines, and 32 programs that each fault once), 560 to 565
by hand with perl's answers, 547 to 549 faults whose line is the
point, 570 to 613 refusals by hand, and from the review 552 to 554,
566 and 614 to 624 (step 5); 700 to 703 and 720 to 732 from
`t/models/loop.py` (about 3,900 lines, and 13 programs that each
fault once), 740 to 743 by hand with perl's answers, 750 to 791
refusals by hand (step 6); 800 to 807 the cap tests, a gigabyte of
garbage each under 16 MB and the cap's own faults, and 810, a made
string in every kind of slot (step 7; no model: there is no second
derivation of what a collector frees); 116 unit tests now, the runtime's
own in C (`collect.c` drives the collector by hand) and three of the
test runner itself (`t/harness/`); 900 to 904 and 920 to 939 from
`t/models/sub.py` (about 1,100 lines, and 21 programs that each
fault once, 919 the first), 940 to 942 by hand with perl's answers, 943 to 946 the
limit on depth from both sides and two faults whose line is the
point, 947, 948 and 950 to 999 refusals by hand (step 8), and two more unit tests
in C (`deep.c`: what a frame counts for, and the stack check). **Every golden test runs with a
collection at every allocation, poison, and a cap of 256 MB** (D64,
D65; `t/knobs.sh`, which `t/run.sh` sources and `t/checks.py` reads);
a test says otherwise in its `# env:`. **The oracle
check** (`t/checks.py oracle`, D10) holds every test to perl 5.42 by
its kind, **run plain, with no switches** (D39), and has 44 tests of
its own in `t/checks/`; its seeds are eight of 64 hex digits
(`PERL_HASH_SEED=1` to `8` are nearly one seed to perl). Its reading
rule for hashes is by pattern and errs toward rejecting; step 12 will
meet it first. Green under gcc, clang, and UBSan with ASan (`make sanitize`,
which since step 7 runs the suite twice, with poison on and off). **Each
step's language was reviewed adversarially** (step 1's: nothing
found, and the compiler agrees with the reviewer's own model on
1,271,555 programs, `docs/briefs/step1-review/`). Each step's runtime
was broken on purpose until every breakage was caught: step 2's found
three holes in its own tests that way, step 3's six of 70
(`docs/briefs/step3-mutations.py`), step 4's none of 50
(`step4-mutations.py`), and step 5's, which breaks the code generator
too, one of 74 and then none of 77 (`step5-mutations.py`; one more it could not see, a
`my` not made undef again on a second entry to its block, is step
6's to test with its first loop, and was); step 6's breaks the
compiler alone, the runtime having gained nothing, 46 of 49 caught the first time and three holes closed
(`step6-mutations.py`, which runs the refused tests too); step 7's
breaks the collector, the knobs and the code generator's frames, 45
of 47 caught the first time and two tests mended that did not test
what they were written for (`step7-mutations.py`); step 8's breaks the
runtime and every pass of the compiler, 77 of 81 caught the first
time, three holes closed and one breakage that nothing in the
language can see (`step8-mutations.py`); the limit of `x` is tested from C
(`runtime/tests/limit.c`), since perl can't be asked for 2^31
characters. **A fault that never happens is
invisible to a test of what prints: every fault needs a fault test of
its own, at its edge.**

**perl 5.42 was installed and everything rerun under it**:
`docs/briefs/claims.py` holds every statement these documents make
about perl as a program, 739 of them now, and all hold under 5.42.0,
run plain as the oracle runs it. [`docs/TRAPS.md`](docs/TRAPS.md)
keeps the programs, T1 to T213, by step (T119 to T124 found proposing
step 6, T132 to T142 proposing step 8, T143 to T148 by its review, T125 to T130 by the review of step 5, T131 building step 6).
**T131 is the one to remember**: where the language faults perl may
carry on, so a loop that only the fault would end never ends under
perl; a test of that kind filled 19 GB of disk. A fault test's loop
is counted by something the fault doesn't touch, and `t/run.sh` and
`t/checks.py` now stop a program that prints past a limit. **Found at step 0**: T72 (a
line that starts `#!`, D33), T73 (`use utf8;` on a line before the
first character past ASCII), T74 (`# line N "file"` comments, step
15), T75 (`use v5.42#c`). **At step 1**: T76. **Proposing step 2**:
T77 to T82. **By the review of step 2**: T91 (a literal over 250
characters), T92 (D45), T93 (`--` on a Num, step 5). **Proposing and
building step 3**: T83 to T90 and T94 to T99, the last six each a
place where perl warns or answers with garbage that the proposal
hadn't seen (`length - 5`; `\x4 `; `substr("abcde", -8, 2)`;
`substr("abc", 0, 1e30)`, which is `ab`; `"a" x -0.5`). **By the
review of step 3**: T100 to T103; the reviewer's model and generator
are kept, `docs/briefs/step3-review/`, and the compiler agrees with
them and with perl on 54,969 of the 55,002 random statements the
model prints for, refusing the other 33 by two rules where it is the
stricter. **By the review of step 4**: T115, and nothing else new;
its search of pasts (18 million looks, by the states perl can put a
variable in) did not refute step 4's claim, the first of three to
stand. Its model is kept too, `docs/briefs/step4-review/`, and the
compiler agrees with it and perl on 36,866 of 37,103 statements,
refusing 236 where it is the stricter. T102
became D46: perl works a constant `x` out as it
compiles, so `say "before"; say "b" x 999999999999999;` prints
nothing under perl (it runs out of memory before the program starts),
where the language prints `before` and faults; a perl without the
memory for what a program asks is outside what D12 promises. No test
asks perl for a large string. What the
review of the oracle check left open is listed in `docs/TRAPS.md`,
"The checks themselves", by the step that has to close it (15: a
`dies` test that also warns; 21 and 22: files, the environment, the
clock; 16 and 19: quotes the reading rule can't pair). A test with a
sort in it breaks its ties.

**D1 to D95 are all Stevan's** (D95 defaults of the builder's at step 11a, which he confirmed) (D87 to D89 defaults of the builder's on step 10's review and its build, which he confirmed) (D81 defaults of the builder's at step 9, which he confirmed) (D73 and D74 defaults of the builder's at step 8, which he confirmed) (D57 a default of the builder's at
step 5, which he confirmed; D58 to D62 his answers to step 6, D63 to
D66 to step 7). The ones a builder meets first: the
core rule (D2); a TypeScript compiler emitting C (D3); a fault can't
be caught (D13); perl's warnings are faults (D15); loop variables are
read-only and containers freeze (D17); a sub can't see its context
(D18); `class`, and `package` only as a namespace (D19); brackets on
a program's own calls (D21); a number is integral or it isn't (D35),
and a value has no past (D36, D40, D45); the name (D32). perigrin has
agreed to the probe corpus (D11). **The review of step 5 found seven kinds of program
the compiler took and should not have** (T125 to T130, and more of
T112), all refused or faulted now: `$t .= ($u = $x . $z)`, where
perl 5.42 itself never assigns `$u` (the one that printed what perl
doesn't; D57); `++` or `--` on a Num of 2^53 or more, where perl
warns by where the Num is and not by whether the step is lost; a
tested `=` that perl folds to a constant, `$x = 0 && $y`; the
file-handle guess after `substr(` and `index(`; a name past 251
characters; `$x =- $y`; `say ("a")` with its `if` on the next line.
Its model is kept, `docs/briefs/step5-review/`, with the drivers
that hold the compiler to it and to perl (`compiler.py`,
`spacing.py`, `handles.py`, `shapes.py`). **Step 5's claim, that a
variable's past shows nowhere the language doesn't fault, stood**:
10,000 pairs of programs and 223,000 singles, nothing but the Num at
2^53. The builder's own evidence
(`docs/briefs/step5-increments.py`) had missed that one for want of
a value, and has it now. **Step 7's adversarial review** (`docs/briefs/step7-review/`, with a
prototype of the design) could not break its rule, and corrected the
proposal round it: poison must check wherever a string is read and
again after an allocation; the cap must count the poisoned dead; ten
holes in the test plan, each closed. Stevan's Mac ran `make test`
green after step 6 and again after step 7, and the tests and the
sanitizers green after step 11a (2026-11-26). **Step 9, arrays and
lists, is built** (2026-11-25; D76 to D81; `docs/PLAN.md` has the
build's own account, and `docs/LANGUAGE.md`, "Arrays and lists", the
language). **An array**, `my @a`, is a variable of its own name (`@x`
and `$x` are two): `$a[I]`, `$#a`, `scalar(@a)`, and the count
wherever one value is wanted; a read past either end is undef and
makes nothing, a store past the end makes the array longer, one
before the start is a fault. **A list** is values copied as it is
built, and flattens: `(...)`, a range, `(LIST) x N`, the slices
`@a[...]` and `(LIST)[...]`; `say` and `print` take one; an array
among a call's arguments flattens, so a sub is handed a count and a
pointer to each argument and faults for a wrong count itself. **A
list assignment is a statement** (D78): `my ($x, @rest) = ...`,
`($x, $y) = ($y, $x)`, `@a = LIST`. `push`, `pop`, `shift`,
`unshift`, `splice`. A sub that returns nothing is no value in a
list (D79). **D76: a later part of an expression or a list may not
change what an earlier part names** (an element, a slice, an array,
`$#a`, a scalar that is an item of a list), refused by one walk over
the whole program, `checkOrder`. **The orders are perl's** (D80):
`$a[I] = V` is V, then I, then the store; `$a[I] OP= V` and a step
are I, the target made, then V; a list assignment is its right side,
every target's index, then the stores; a list slice its indexes
first. **`for my $x (LIST)`, spelled `foreach` too** (9b): the list
is copied once, `$x` is a copy, new each time round and read-only; a
range alone is counted in C and builds nothing; **every array named
anywhere in the list is frozen while the loop runs**, a count on the
array, given back on every way out (the end, `last`, a jump to a
loop further out, `return`), and a store to it or a change of its
size, from the block or a sub it calls, is the fault `an array was
changed while a foreach is over it`. `$#a` names `@a`: the loop that
changes an array as it goes takes the count into a `my` first.
**D77**: a loop is refused when its block, or a sub the block calls,
can change a scalar named anywhere in its list, a range's end too
(T172; D81 says the exception is sound and not made). An element or
a slice past either end in a loop's list is a fault, through every
shape perl would make it by (T161, T169), and so is a slice in a
call's arguments, and a counted range within 512 of the smallest
integer (T166). **In the runtime** an array is a block of the
collector's with storage of its own (`realloc`, counted against the
cap, starting no collection), a list is an array in a temporary, and
a loop's list has a slot of its own, a declaration no program can
name. **Tests**: 410 to 417 and 420 to 439 from `t/models/list.py`,
450 to 453 by hand, 460 to 494 refusals (9a); 811 to 813 and 820 to
854 from `t/models/each.py`, 814 by hand, 855 to 859, 881 and 882
faults by hand, 860 to 880 and 883 to 885 refusals (9b); 691 golden
tests and 124 unit tests in all. **Broken on purpose**: 9a's 66 of
69 caught the first time, two holes closed by 453 and one test the
script had not been running; 9b's 55 all caught when it ran, five tests having been added while the list of breakages was written, for what it showed nothing would catch. **T131 came back**: a
fault test that pushes onto the array its loop is over never ends
under perl, so every change in such a loop is followed by `last`.
**Refused until step 10**: `return` of a list, `@rest` in a
signature, `for (LIST)` and the `for` modifier (both `$_`), a slice
on the left of `=`, `$#a = N`, `@a` in a string. **Step 9's
proposal** was reviewed adversarially before it was built: eleven
ways to be WRONG (T157 to T168, `briefs/step9-review/`), which is
where "named anywhere" and the written orders come from. **Next:
step 10**, list operators, `$_` and list returns: **proposed and agreed** (2026-11-25, `docs/PLAN.md`; D82 to D86, each the recommendation: perl's merge ported for `sort`, with the licence of `pp_sort.c` to account for when the repository gets one (D82); the generated code drives the sort and the runtime never calls a block (D83); `grep` and `map` are a count where one value is wanted (D84); a block always, and `$_` always written (D85); three sub-steps, 10a list returns, 10b `$_`, 10c `sort` (D86). T173 to T184 were found writing it, with 46 statements about perl). **Its adversarial review found six ways to be WRONG** (T185 to T192, `briefs/step10-review/`; the proposal is amended at its end, "What the review found", and D87 has the builder's defaults on it, for Stevan to confirm): `grep`, `sort` and `reverse` hand on the containers they were given, so they name what their list names for D76's walk, and `join`'s separator is the first item of its list; perl's in-place `@a = sort BLOCK @a` drops elements that were never stored, so an undef there is a fault; a `sort` with a block makes elements past the end, so D80's fault holds in its list; a word that is not perl's own first after `sort` is a comparator's name or a string to perl, and is refused; `map`, `grep` and `sort` take no brackets of their own. What stood: the numeric past (108,416 comparisons, every difference already a fault) and the blocks perl throws away (21,600 sorts). **10a is built** (2026-11-25; `docs/PLAN.md` has the account, `docs/LANGUAGE.md` the language under "A sub that gives back a list" and "join and reverse"): `return LIST;` and a list as a last statement, every value to a call where a list is wanted; **D18's fault**, `f returned a list where one value is wanted`, for a `return` that is list-shaped by how it is written, raised by the `return` before anything of it is worked out; `sub f($x, @rest)`, a copy, filled at its turn; `join(SEP, LIST)` and `reverse(LIST)`, with brackets or without, `reverse` refused where one value is wanted. **Which subs give a list is known as the program compiles** (`shapes.ts`: a list-shaped `return` or last statement, or a call of such a sub handed on), and decides whether a call's arguments are handed over as places, read late, or built as one list; a sub is handed its arguments' count, their places, and, when they were built as a list, where that list's values are. Tests: 1000 to 1002 and 1010 to 1047 from `t/models/ret.py`, 1003 by hand, 1048 and 1049 faults by hand, 1050 to 1071 refusals; 760 golden tests and 125 unit tests in all. Broken on purpose: 51 of 56 caught the first time. Three were holes, each a way of being list-shaped that no test reached (brackets and a comma round an array, a slice of an array by one bracketed index, the second arm of a `? :` alone), and 1072 to 1074 close them; one breakage was the builder's own mistake and changed nothing; and one nothing in the language can see: whether `join` reads its separator before or after its list is built, since D87 refuses a list that could change it. **10b is built** (2026-11-25; `docs/LANGUAGE.md`, "`$_`, map and grep"): `for (LIST) { }` and `STATEMENT for LIST;`, which are 9b's `foreach` with `$_` for its variable; `map { } LIST` and `grep { } LIST`, a `foreach` in the middle of a statement, the block generated where it stands and its value added to the list being built, so that **nothing calls anything and the runtime gained nothing**. `$_` is read-only, a declaration of its binder's seen in the block alone (not in a sub the block calls), always written (D85), never declared by a program. The list is copied, its arrays frozen, D77 for its scalars, T177's fault past the end; `grep` names what its list names for D76 and `map` nothing; where one value is wanted both are a count (D84); list-shaped after `return`. In a block: no `return`, no `last` or `next` to a loop outside it, an expression last (or a `say`, worth `true`), a word operator allowed there, and not a string or a number and a comma first, nor `{`, nor empty (T175). A block's statements have their temporaries after those of the statement it stands in, and what that statement declares has its slot after the block's. **perl 5.42 itself crashes on a `grep` whose block shifts its array** (T194): no test asks it to. Tests: 1100 to 1102 and 1110 to 1154 from `t/models/it.py`, 1103 by hand, 1155 and 1156 faults by hand, 1160 to 1195 refusals; 847 golden tests and 127 unit tests in all. Broken on purpose, the compiler alone: 37 of 41 caught the first time; one hole closed, one test mended, and a bug found by it: a `for`'s header with a block in it was read as three parts for the block's semicolon. **10c is built, and step 10 with it** (2026-11-26; `docs/LANGUAGE.md`, "sort"): `sort LIST`, by string, and `sort { } LIST`, with `$a` and `$b`, read-only and the block's alone. **Every comparison is perl's, in perl's order** (D82): `runtime/sort.c` is `pp_sort.c`'s merge (natural runs, then a binary merge), ported statement for statement, and `t/models/merge.py` the same in Python; each asks for exactly the pairs perl hands a block over 4,200 lists, one way of comparing among them being no order at all. So a block that counts, prints or is inconsistent shows what it shows under perl. **The generated code drives the sort** (D83): `rt_sort_next` runs the merge to its next comparison and returns the two values, the block is generated where it stands, `rt_sort_answer` takes its value, and `rt_sort_next` takes up where it was (the merge's variables in a struct, a `switch` on which comparison it stopped at). **The runtime still calls no generated code**, and what D68 kept open for step 29 is open. **`runtime/sort.c` is perl's code ported, under perl's terms, in a file of its own that says so: its licence is to be settled when the repository gets one** (D82, Stevan's note). The block's value is a whole number, a fault outside 32 bits; the list is copied, its arrays frozen, D77, a fault past the end; a `sort` names what its list names; refused where one value is wanted; an undef in `@a = sort { } @a` is a fault (perl sorts in place and drops what was never stored); a word or a scalar first after `sort` is refused, and so are brackets of its own; a lone value is looked at for the four blocks perl throws away. Tests: 1200 and 1201 (the comparisons, logged) and 1210 to 1235 from `t/models/sort.py`, 1202 by hand, 1236 and 1237 faults by hand, 1250 to 1269 refusals; 898 golden tests and 129 unit tests in all. Broken on purpose: 40 of 40 caught, fifteen of them breakages of the merge itself; one, the single value picked up into a long run, was caught only by the runtime's own test of the machine, so 1201 has three lists that take that path, and the golden tests catch it too. **Next: step 11a, interpolation, pulled forward from step 16 to before the census (D90, Stevan's, 2026-11-26), and then 11b, the census.** **11a is built** (2026-11-26; D91 to D94 are Stevan's answers, each the recommendation, and D95 the builder's defaults, which he confirmed; `docs/PLAN.md`, step 11a, has the proposal, its review and the build's account, and `docs/LANGUAGE.md`, "A variable in a string", the language; T196 to T212; 55 rows of `claims.py`, 737 in all). **In double quotes**: `"$x"`, `"${x}"`, `"@a"`, `"@{a}"`, `"$a[I]"`, `"@a[I, J .. K]"`, `"$#a"`, `"$#{a}"`, where **I is a whole number or a scalar variable** (D91; no leading zero, at most 2^63 - 1). An array's values are joined with one space. **Every other `$` or `@` in double quotes is refused** (D92), and so is what perl would take into a variable hard after it: `::`, `{`, a second `[`, `->` before `[ { @ $`, a character past ASCII after a bare name; after braces nothing is. Each piece is made a string as `.` makes one, an undef is D48's fault, of two faults the left one's. **The lexer does it**: a string with a variable in it is a `str` token with `pieces`; the tree's node is `interp`, which the checker's walks do not look inside; the generated C is `rt_concat` and `rt_join`, and **the runtime gained nothing**. Tests: 1300 to 1302 and 1310 to 1346 from `t/models/interp.py`, 1303 and 1349 by hand, 1350 to 1450 refusals from a table by hand (`briefs/step11a-refusals.py`); 1,041 golden tests and 131 unit tests in all. The compiler agrees with the reviewer's model on the pieces of all 805,000 strings both take, of 1,885,000 (`briefs/step11a-review/compiler.py`). Broken on purpose: 62 of 66 caught the first time, four holes closed. What perl showed: **an interpolated string is a value, made where it stands** (T196: `"$x-" . ($x = 5)` is `3-5`), so it is no piece of a row of dots and names nothing; the risk is where a name ends (`"a $ b"` is `$b`, `"$x::y"` runs, `"$#a::"` is `-1` in silence, `"@-"` and `"@_"` are silent), so a `$` or `@` begins one of a short list of shapes or is refused; and perl loses the assignment in `$t .= ($u = "$x$z")` (T198). **Its adversarial review** (`briefs/step11a-review/`, with a model of the lexing rule held to perl over 890,000 strings) found one way to be WRONG, a leading zero in an index, which is octal to perl (T211), and overturned no recommendation. **The census's first run, before 11b is proposed, found a WRONG** (T213, 2026-11-26): of 5,786 distinct probes run once beside perl by a throwaway script, eleven printed what perl does not, all one trap, step 9's: an assignment to an element, and `++$a[0]`, are the element itself to perl, read late (`($a[0] = 5) + ($a[0] = 7)` is 14), and D76's walk had not counted them as naming their array. They do now, and each is refused (1451 to 1458; `checker.ts`, `named`). The rest of that run: 4,990 refused, 718 the same as perl, 67 a fault where perl prints on. **Next: 11b, the census, which is not proposed; Stevan has said the probes are imported into `t/census/`, pvm's `conformance/mdtest` cases with them, and PerlOnJava's suite is for step 18.** `docs/PLAN.md` has what each has to decide, and for the census what was said of it on 2026-11-26 (a verdict kept for each probe; a fifth verdict where perl warns; `make census` apart from `make test`; where the probes came from, for the licence). **The session that builds 11b needs `stevan/perl5-son`, `stevan/chalk` and `stevan/pvm` attached**: this one was refused when it tried to add them. Open with the repository's licence: `runtime/sort.c` (D82) and the census's probes.
**Step 8, subs** (D67 to D73; `docs/PLAN.md` has the build's own
account). **A sub** stands at the top level, always with a
signature, and is called with brackets, before or after it is
written. Its name is not a word of perl's (`names.ts` has perl's own
keyword table, 266 words, and what `use v5.42;` brings in), not `v`
and digits, and not used twice. **A parameter** is `$p`, `$p = E`,
`$p //= E`, `$p ||= E`, or a placeholder; a copy; **a sub copies
each argument as its parameter's turn comes, a default running in
between** (perl's order, T144), so an argument that is a variable is
read late (T1) and a `//=` default is seen by the arguments after
it. **A wrong number of arguments is a fault**, after they have all
run. **`return` is a statement**, with an `if` or `unless` or
without. **A sub's value** with no `return` is its last statement's
when that is an expression with no modifier (a value alone is a
statement there and nowhere else), and `true` after a `say` (D70);
any other ending has none, and using it faults, void calls aside
(D18, T145). **Context** is perl's three, handed on by `return`, a
last statement, `? :`, the right of `|| && // and or`, brackets and
a unary plus (T146): a sub that returns nothing is undef to a
scalar and a fault where perl wants a list (D71), until step 10.
**A file variable**, a `my` at the top level, has a slot of its own,
is undef as the program starts, and its `my` stores nothing (T134,
T147): a sub written after it may be called before it. **Nothing
happens at 100 calls deep** (D67: `no warnings 'recursion';` keeps
perl as quiet, and a test that goes deep carries it). **The limit on
depth is the implementation's** (D68): the open frames count 16
bytes a slot and 1 KB a call, and past 4 MB the next call is
`recursion too deep`, about 3,700 deep for a small sub; a program
given less than 8 MB of stack stops before it starts. D68 lists what
keeps a call free to stop being a C call at step 29. **Refused at
step 8**: a sub in a block, a loop or a sub (T31), with no
signature, named for a word of perl's, named twice; a call with no
brackets, of a sub the program doesn't have, with two commas
together (T137); a minus hard against one letter, anywhere (T135:
`-e(2)` is a file test); a blank between a name and its bracket
first after `say` or `print`, through any brackets (T136); `return`
as a value, after `and`, in a default, outside a sub, with a `while`,
with a word operator after its value (T139); a required parameter
after an optional one, a parameter named twice, a `my` of a
parameter's name (T141); `(...) x N` as an argument, after `return`
or as a last statement (T143); a value alone that is not a sub's
last statement or has a modifier; **a row of dots in which a later
piece calls a sub that can change a variable an earlier piece reads,
worked out over the whole program** (D69, T132; the left of `.=` is
the first piece). **Its adversarial review found four ways to be
WRONG and three shapes perl refuses** before anything was built
(T143 to T148, `briefs/step8-review/`); D73 has what was done about each. **What the build
found**: step 5 had every statement end in a semicolon, the last in
a block too, so `sub f($x) { $x * 2 }` was refused; **D75, his: the
last statement of a block may leave it out** (not the file's last;
905, 906, and 604 is a `same` test now). T132 to T142 were found proposing
the step, and `briefs/step8-names.py` and `step8-stack.c` are its
evidence for names and for the limit. **What step 8 hands step 9**:
a list-shaped `return` and D71's fault wait for lists; a runtime
function that holds more than one value opens a frame, which counts
against the limit on depth like any other; step 10's `sort` with a
block is the first thing that will want the runtime to call
generated code, and D68 says it has to say how. `docs/briefs/step4-comparisons.py`
holds step 4's rule for comparing to perl under every past of each
operand: 57,376 comparisons, no new fault needed. **What every step
must ask again**: whether a value's past shows anywhere the
rules don't fault. The claim was refuted once (T92), by a review,
after the builder's own search had passed it. The evidence is kept:
`docs/briefs/step2-perl-numbers.py` (D35 against perl, 129,801
operations), `step2-history.pl`, `step2-literals.py` (perl reads and
prints floats as C does; run it on a new machine), and
`step3-strings-as-numbers.py` (D40 and D45 under every past of every
operand: 41,594 operations, perl having more than one answer for
9,596, the rule never giving a value perl doesn't). One risk to watch
on the Mac: `**` with a fractional operand is the C library's `pow`.
**Roles come up at step 17, not 27**: Stevan wants them a key part of
the object system, and step 17's proposal takes them up; `PLAN.md`,
step 17, names the two repositories to read first
(`stevan/p5-roles-algebra`, `stevan/p5-core-role-tests`). Nothing
about them is decided.
Not agreed: what the decisions leave to steps, listed at the end of
[`docs/DESIGN.md`](docs/DESIGN.md).

## Read first, in this order

1. [`docs/LANGUAGE.md`](docs/LANGUAGE.md): the language as it is, for
   someone writing programs in it.
2. [`docs/DESIGN.md`](docs/DESIGN.md): the language and implementation
   as agreed. **(open)** marks a later proposal that hasn't been
   confirmed; there are none yet.
3. [`docs/SURFACE.md`](docs/SURFACE.md): Perl, construct by construct:
   in, a fault, later, or cut.
4. [`docs/PLAN.md`](docs/PLAN.md): the build order.
   [`docs/TRAPS.md`](docs/TRAPS.md): for the step in hand, the
   programs where the obvious implementation is WRONG.
5. [`docs/DECISIONS.md`](docs/DECISIONS.md): why, and what was turned
   down. Check it before "improving" something; it may have been
   decided against.
6. [`docs/BACKGROUND.md`](docs/BACKGROUND.md): the five projects this
   learned from, and what is parked. Optional.

The process is the workbench's: `docs/PROCESS.md` and `docs/MODELS.md`
in `pmmc-labs/esoteric-language-workbench`.

## Working rules

- **The core rule (D2) is the design.** Before accepting a construct,
  ask what perl does with it. If the language would do anything else,
  it refuses or faults. A change that gives a Perl program a new
  meaning is a proposal that says so in its first line.
- **Never WRONG.** A program that runs, doesn't fault, and prints what
  perl doesn't is a bug, whatever else is true. Fix it by agreeing
  with perl, or faulting, or refusing, in that order of preference. A
  refusal has a message that names what was refused.
- **Aggressively simple.** When a feature needs machinery, say so and
  offer to cut it. Cutting is always allowed here.
- **Propose before building** any change to semantics, a construct
  moved between In, Fault, Later and Cut in `SURFACE.md`, a builtin,
  or anything marked (open). Give options and a recommendation. Record
  the outcome in `docs/DECISIONS.md` (who decided, why, what was
  rejected) and update `docs/DESIGN.md` and `docs/SURFACE.md`.
- **perl is the oracle, and memory isn't.** Never write what perl does
  from memory, in a test, a decision or a document: run perl 5.42 and
  paste. (perl5-son recorded being wrong from memory twice in one fix;
  this design's first draft had `2 ** 62` as an exact integer, and
  perl prints `4.61168601842739e+18`.)
- **A proposal for a large step is reviewed adversarially before
  it's built**: a reader who didn't write it, given the proposal and
  perl, asked to find a program that would run, not fault, and differ.
  What it finds goes into `docs/TRAPS.md` with the program and perl's
  output, and into the step as a test.
- **Expected output never comes from the compiler** (D7). A `same`
  test's comes from perl; a `fault` or `refused` test's is worked out
  by hand; a model writes the edges. When a model's output moves,
  rerun the model; don't patch the file.
- **Make a check fail on purpose before trusting it.** A new check,
  a new kind of test, a new script: break what it guards and see it
  go red. (perl5-son's harness once reported 986 of 986 clean when
  857 were, because a loop ate its own input.)
- **Tests run programs.** A check that reads the tree or the C and
  never runs the binary proves nothing about what a program prints.
- Keep a working compiler with passing tests at the end of every step
  (Ghuloum). Each step adds golden tests.
- **Examples bend to the language** (D8). A port of a Perl program
  will want something that was cut; change the port.
- When a construct or builtin is added or changes, update
  `docs/LANGUAGE.md` (no tables there) and its row in
  `docs/SURFACE.md`.
- When editing with scripts, assert that each replacement matched.
- Test timing uses a virtual clock; real time is never used in tests.
- Update the Status section above as steps land. It is the only
  handoff: there is no `docs/plans/`, and a plan that isn't a step in
  `PLAN.md` or a `Dn` doesn't exist.
- A commit that touches the implementation names its decision or plan
  step in the subject (D9; `make hooks` installs the check).
- At the start of a step, compare the step's **Size** line with your
  own model, by the workbench's `docs/MODELS.md`, and say so if they
  don't match.

## Code style

- TypeScript that Node runs as it is: only erasable syntax (no enums,
  no parameter properties, no namespaces).
- The compiler is plain functions over plain data: tree nodes are
  objects with a `kind`, lists are arrays, and nothing is mutated
  after the pass that made it. One file per pass. No class
  hierarchies. (If the compiler is ever ported to the language, this
  is the shape that ports; nothing depends on that.)
- **One table of names** (`compiler/src/names.ts`): keywords, builtins,
  their argument shapes and contexts. No pass switches on a source
  string that isn't in it.
- An error is a diagnostic with a position, raised where it's found.
  It is never a node in the tree.
- The generated C is one statement per operation, each result in a
  temporary (D31). C doesn't order a call's arguments: never pass a
  variable and a call that sets it in the same argument list, and
  never two arguments that can fault. A C compiler takes more than
  proportionally longer over one long function (gcc at `-O1`, 36
  seconds for ten thousand statements): the driver compiles the
  program's C at `-O0` and the runtime at `-O1`, and a model keeps a
  program to about three thousand statements. The cloud machine's `cc` is gcc
  and the Mac's is clang: run the suite under both, and `make
  sanitize`, before calling a runtime change done. A left shift of a
  negative value is undefined before C23. (All three are the
  workbench's findings, each from a bug.)
- The runtime has no global state: one context, first argument of
  everything (D28).
- Every runtime operator checks its operands' tags and faults by name.
  No operator trusts the compiler until types (step 26) give it a
  reason to.
- The passes walk the tree by recursion, so an expression some
  thousands of terms long or brackets deep stops the compiler (exit 2,
  with a message). A pass that must take more becomes a loop.
- Comments explain why, not what.

## Toolchain

- Node 22.18 or later, and a C compiler as `cc`; clang as well.
- **perl 5.42**, as `CURLY_PERL` (default `perl`). The checks fail
  without it; they don't skip, and `make doctor` says what is wrong.
  The cloud machine's own perl is 5.38.2. 5.42 comes from the
  environment's setup script, built from cpan.org's source (reachable;
  no network change needed) into `/opt/perl-5.42`, with
  `CURLY_PERL=/opt/perl-5.42/bin/perl` set on the environment:

      if [ ! -x /opt/perl-5.42/bin/perl ]; then
        cd /tmp
        curl -fsSLO https://www.cpan.org/src/5.0/perl-5.42.0.tar.gz
        echo "e093ef184d7f9a1b9797e2465296f55510adb6dab8842b0c3ed53329663096dc  perl-5.42.0.tar.gz" | sha256sum -c -
        tar xzf perl-5.42.0.tar.gz
        cd perl-5.42.0
        ./Configure -des -Dprefix=/opt/perl-5.42 -Dman1dir=none -Dman3dir=none
        make -j"$(nproc)"
        make install
      fi

  It runs at the start of a session, and step 0 found it done: the
  download at 17:42:29, `Configure` finished by 17:42:59, perl built
  by 17:43:25 and installed by 17:44:05, so about a minute and forty
  seconds on four cores before the session can work. `perl -V:ivsize
  -V:nvsize` gives 8 and 8. The same script installs
  `libclang-rt-18-dev`, clang's sanitizer runtime, for `make
  sanitize`. On a Mac, any perl 5.42 will do (perlbrew, plenv, or the
  script above with another prefix), named by `CURLY_PERL`.
- Python 3 for `t/checks.py` and the models.
- `make doctor` checks the setup, and `t/run.sh t/000-say.pl` should
  end `1 tests, 0 failed`.

## Layout

| Path | |
|---|---|
| `bin/curlyc.ts` | The driver: `curlyc -o out file.pl` |
| `compiler/src/` | One file per pass: `lexer.ts`, `parser.ts`, `resolver.ts`, `checker.ts`, `codegen.ts`; `ast.ts`, the tree; `shapes.ts`, what is list-shaped and which subs give a list (D18), shared by three passes; `names.ts`, the one table of names: statements, builtins, pragmas, operators (D29); `errors.ts` |
| `compiler/tests/` | Unit tests, per pass |
| `runtime/` | `rt.h`, `rt.c`; `sort.c`, perl's merge sort ported, a file of its own for its origin and its licence (D82), which rt.c includes; `tests/`, C programs that call the runtime directly, each run by `rt.test.ts` (`collect.c` is the collector's, `deep.c` the limit on recursion's, `arrays.c` arrays, the freeze and a foreach's own, `sortm.c` the sort machine, held to perl) |
| `t/` | Golden tests `NNN-name.pl` and `.expected`; `run.sh`; `knobs.sh`, what every test assumes of the runtime; `checks.py`; `checks/`, the oracle check's own tests; `harness/`, the test runner's own; `models/` (`arith`, `num`, `str`, `bool`, `var`, `loop`, `sub`, `list`, `each`, `ret`, `it`, `sort`, `interp`, and `merge`, perl's merge sort as a generator, which holds itself to perl) |
| `docs/` | The documents above; `PROCESS.md`, `MODELS.md` and `REPORT.md`, the workbench's; `briefs/`, with `claims.py` (every statement about perl, as a program), `step1-review/` (a reviewer's model of step 1's language, and the scripts that ran the compiler against it), `step2-*`, `step3-strings-as-numbers.py`, `step4-comparisons.py` and `step5-increments.py` (the evidence for those steps' rules), `step3-mutations.py` to `step8-mutations.py`, `step9a-mutations.py`, `step9b-mutations.py`, `step10a-mutations.py`, `step10b-mutations.py`, `step10c-mutations.py` and `step11a-mutations.py` (the runtime, and from step 5 the compiler, broken on purpose; each is a record of its step and stops at a piece of text a later step has changed), `step8-names.py` and `step8-stack.c` (step 8's evidence for which names a sub may have, and for the limit on recursion), `step3-review/`, `step4-review/` and `step5-review/` (each reviewer's model, and the scripts that ran the compiler against it), `step7-review/` (the reviewer's prototype of the collector), `step8-review/`, `step9-review/` and `step10-review/` (the findings of those steps' reviews, with their programs), `step11a-review/` (the reviewer's model of where a variable in a string ends, the scripts that held it to perl, and `compiler.py`, which holds the compiler to both), and `step11a-refusals.py` (the table step 11a's refusal tests are written from: the program, the place and the message, by hand) |
| `exp/`, `tools/decisions/` | The workbench's: its experiments (`MODELS.md` cites them) and the decision-log browser |
| `build/` | Output (ignored) |

`docs/PLAN.md` has what is still to come: `lib/`, `examples/`,
`t/census/`.

## Commands

- `make test`: the unit tests, the golden tests, then the mechanical
  checks (`t/checks.py`), which ask perl. About two minutes, most of
  it the oracle running perl eight times over each test.
- `make unit`, `make golden`, `make checks`: one at a time.
  `t/run.sh t/000-say.pl` runs one golden test; `JOBS=1` runs them one
  at a time.
- `make oracle`: writes each `same` and `dies` test's `.expected` from
  perl. That is how such a file is made; never by hand, and never from
  the compiler. It writes nothing for a test perl warns on or whose
  output moves with the hash seed.
- `make doctor`: each tool's version, and a failure for a perl that
  isn't 5.42 with 64-bit integers and doubles.
- `make golden-clang`: the golden tests with clang as the C compiler.
  `make sanitize`: with UBSan and ASan, every finding fatal. Neither
  is part of `make test`. `CURLY_CC=clang make unit` does the same for
  the runtime's own tests.
- `make models` reruns every model and writes its files;
  `make commits` checks the subjects since origin/main; `make hooks`
  installs the commit-msg hook.
- `make check`: `tsc --noEmit` (`npm install` once, for it).
- `python3 docs/briefs/claims.py`: every statement the documents make
  about perl, rerun. Not part of `make test`.
- `make decisions`: `build/decisions-curly.html`, a browser of the
  decision log.
- `node bin/curlyc.ts -o out file.pl`: compile and link. It writes
  `out.c` and `out.rt.o` (the runtime, compiled) next to `out`. Exit codes: 0 ok; 1 a refusal, `FILE:LINE:COL:
  message` on stderr and no binary; 2 usage, the toolchain, or a file
  it can't read or write; a fault in the compiler itself is `curlyc:
  internal error: ...` with Node's stack, and 2.
- `make census` comes with step 11b.
- Environment: `CURLY_PERL`, the oracle (default `perl`); `CURLY_CC`,
  the C compiler (default `cc`); `TIMEOUT`, the seconds a golden test
  may run (default 60); `JOBS`. A compiled program reads three, the
  collector's knobs: `CURLY_GC_STRESS`, `CURLY_GC_POISON` and
  `CURLY_HEAP_CAP` (D63), which `t/knobs.sh` sets for every test.

A compiled program prints to stdout and exits 0. A fault is `fault:
MESSAGE at FILE line N.` on stderr and exit 1, after whatever stdout
had. An uncaught `die` is its message on stderr and exit 255. The
golden tests check stdout and stderr together, plus `exit: N` when the
status isn't 0.
