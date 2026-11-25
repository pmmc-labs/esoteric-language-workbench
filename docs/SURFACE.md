# The surface

Perl 5.42, construct by construct, and what this language does with
each. It starts from Chalk's declared subset (D4:
`docs/chalk-grammar-spec.md` in `stevan/chalk`), adds what perl5-son's
audits and Allium's triage say about cost, and applies the four ideas
of [`DESIGN.md`](DESIGN.md). Where a row cites a decision, the
decision is made; the rest is the plan's reading of the decisions, and
each step confirms its own rows when it's proposed. This file is then
kept true, as the map of what's in.

What a row can say:

- **In**: part of the design. It will be accepted, and agree with
  perl (D2), from the step named; until that step it is refused.
- **Fault**: accepted, and stops at run time where perl would have
  warned, guessed, or done something D17 to D22 cut.
- **Later**: not designed yet. Refused until the step named proposes
  what it means here, or whether it's wanted.
- **Cut**: refused, and not planned. Reopening one is a proposal.
- **New**: perl doesn't have it; an exception to D2.

Steps 0 to 5 are built, 6 is being built, and nothing after them, so "In" is a plan and
not a fact; [`LANGUAGE.md`](LANGUAGE.md) is what works.
[`TRAPS.md`](TRAPS.md) has the programs that show why a row says
what it does.

"Chalk" in the last column says what Chalk's declared subset does, for
comparison: *in*, *out*, or *n/a*.

## Program and declarations

| Construct | Here | Step | Chalk | Note |
|---|---|---|---|---|
| `use v5.42;` first | In, required | 0 | in | D16 |
| `use utf8`, `use experimental '...'` | In | 3, 17 | in | D16. On a line before the first character past ASCII, a comment's included (T73) |
| A line that starts `#!`, the first or any other | Cut | | | D33: perl takes switches from it when it is line 1, and a `# line 1` comment makes any line that (T72). After code on its line: a comment |
| A version literal hard against a comment, `use v5.42#c` | Cut | | | perl then asks for a module called `v5` (T75) |
| A comment that is a line directive, `# line 100 "file"` | Later | 15 | | T74: it changes the line and file a `die` reports |
| A carriage return, a form feed, any other control character; ^D or ^Z | Cut | | | perl takes the first two for white space, and ends the program at either of the last. Windows line endings are converted first |
| `use Module;` of the program's own | Later | 18 | in | Compile time only |
| `use Module qw(names)`, `Exporter` | Later | 18 | in | To be proposed |
| `no strict`, `no warnings`, `use integer`, `use bytes` | Cut | | | D16 |
| `use open ':std', ':encoding(UTF-8)';` | In | 3 | | D39: needed to print a character past ASCII, which faults without it (plain `perl` prints `é` as one byte). That one spelling, at the top |
| `use open qw(:std :encoding(UTF-8))`, `':utf8'`, any other layers | Cut | | | D39: one spelling. `qw` itself is step 16 |
| `use constant`, `List::Util`, `Scalar::Util`, `POSIX`, other core modules | Later | 18, 23 | | D16: refused until proposed |
| `require`, `do FILE` at run time | Cut | | out | D20 |
| `package Name;` naming a file's subs | In | 18 | out | D19: a namespace and nothing more |
| `Name::f($x)`, a sub of another package | In | 18 | in | |
| `package Name { }`, `__PACKAGE__`, imports | Later | 18 | | |
| `BEGIN`, `END`, `INIT`, `CHECK`, `UNITCHECK` | Cut | | in | D20; `BEGIN` as evaluation is parked |
| `__DATA__`, `__END__`, POD | Cut; POD later | 16 | out | POD is a comment, when someone wants it |
| `my $x`, `my @a`, `my %h`, `my (...)` | In | 5, 9, 12 | in | D56: `my $x` at the head of a statement, or in the test of an `if`; a name is ASCII (D55) |
| `my` under a statement modifier, right of `&&`, `\|\|`, `//`, in a branch of `? :`, or anywhere else inside an expression | Cut | | | D21, D56: perl keeps the old value, or may not reach it (T30) |
| A second `my` of a name in one scope | Cut | | | D15: perl warns |
| A variable with no `my` in sight | Cut | | | perl doesn't compile it, under `use v5.42` |
| `${name}`, `$ name` | Cut | | | D55: perl warns of the first where it could be a block (T114) |
| A variable first after `say`, `print`, `substr(` or `index(`, a blank, and what could begin a value: `say $x -1;` | Cut | | | D56, T111, T125: a file handle, to perl, which dies or doesn't compile |
| `$x =- $y`: a sign hard after `=`, and a blank after the sign | Cut | | | D56, T127: perl warns `Reversed -= operator` |
| A name of more than 251 characters | Cut | | | D55, T126: `Identifier too long` |
| A statement that only has a value, `$x + 1;`; two joined by a word operator, `$x = 1 and $y = 2;` | Cut | | | D56: perl warns of each (T114) |
| `state` | In | 14 | in | |
| `our`, package variables, `$Pkg::x` | Cut | | in | D19 |
| `local` | Cut | | in | D17; parked |
| `sub name (signature) { }` | In | 8 | in | A signature is required; at the top of the file; not named for anything perl knows (D21) |
| A sub without a signature, `@_`, `shift` on it | Cut | | out | D17 |
| Defaults in a signature, slurpy `@rest`, `%opts` | In | 8, 10, 12 | in | |
| Prototypes, `&` calls, `goto &sub` | Cut | | out | D21 |
| `my sub`, anonymous `sub`, closures | In | 14 | in | |
| `__SUB__` | In | 14 | | |
| `__FILE__`, `__LINE__` | In | 16 | | |
| `sub f;`, a forward declaration | Cut | | | Nothing needs one (D21) |
| `no warnings 'recursion';`, with the pragmas | In | 8 | | D67: without it the 100th open call of one sub is a fault |
| Recursion past the implementation's limit | Fault | 8 | | D68: `recursion too deep`; perl has no limit |
| A sub that ends in `say` or `print`, and its value used | In | 8 | | D70: `true`, as perl |
| A sub that returns nothing, as an argument or `say`'s | Fault | 8 | | D71, until step 10: perl passes no argument |
| A row of dots in which a later piece calls a sub that can change a variable an earlier piece reads | Cut | | | D69, T132 |
| Signature placeholders `$`, `@`, `%`; defaults with `//=` and `\|\|=`; a default that reads an earlier parameter | In | 8 | | |
| `my $x = $x`: the right side sees the outer `$x` | In | 5 | | T58 |
| `my` in a condition, `if ((my $n = f()) > 3)` | In | 5 | | |
| `my (undef, $x) = ...` | In | 9 | | |
| `my $a`, `my $b`; `$a`, `$b` and `$_` as names | Cut | | | D55, T61: perl warns, and `sort` then misbehaves; and perl lets them by without a `my` |
| `\my $x`, `foreach \my %h (...)` | Cut | | | Not in the `use v5.42` bundle |
| Attributes other than the class ones | Cut | | | `:lvalue` among them |

## Statements and control

| Construct | Here | Step | Chalk | Note |
|---|---|---|---|---|
| `if`, `elsif`, `else`, `unless` | In | 5 | in | Braces always; a fault in a test names the line of its `if` or `elsif` |
| `unless` with `else` or `elsif` | Cut | | | D54 |
| `EXPR if COND`, `unless` | In | 5 | in | The statement is `say`, `print`, an assignment or a step; a fault in the test names the statement's line (T118) |
| `=` with a constant on its right, where a value is tested for truth: `if ($x = 5)`, `if ($x = 0 && $y)` | Cut | | | D53, T112: perl warns that `==` was meant; through `!`, `not` and `+` too, and for what it folds to a constant |
| `while`, `until`, postfix forms | In | 6 | in | D62. A `my` in the block or the test is new each time round; `while ()` is refused (T123) |
| `for (init; cond; step)` | In | 6 | in | D60, D62. A comma in the first and third parts only; `my` in the first only |
| `foreach my $x (LIST)` | In | 9 | in | `$x` is read-only; every container that can reach the list is frozen (D17) |
| `foreach $x (LIST)` with a variable that isn't `my` | Cut | | in | T14 |
| `foreach` with no variable, postfix `for` | In | 10 | in | `$_`, read-only, and only inside the block that binds it |
| `foreach` over `($p, $q)` naming variables | Later | 9 | in | D17: perl aliases them |
| A closure over, or `\` of, a loop variable or `$_` | Later | 14 | in | D17: perl keeps the alias after the loop |
| `foreach my ($k, $v) (%h)` | Later | 12 | | 5.36's; to be proposed |
| `last`, `next`, labels | In | 6 | in | D61, D62. Statements, not expressions (T120); only inside a loop of the same sub, as written; a label is on a loop, in capitals, and is checked as the program compiles |
| `last` or `next` with no label, straight inside a bare block | Cut | | | D59, T32: it leaves only the block, to perl |
| `last` or `next` reaching a loop from a called sub, or from a `map`, `grep` or `sort` block | Cut | | | T59, T60: perl leaves the outer loop |
| `redo`, `goto`, `continue` blocks | Cut | | out, `redo` in | |
| Bare blocks | In | 5 | in | A scope. To perl it is also a loop that runs once, which D59 cuts; a label on one: cut. An empty one is an anonymous hash to perl, and refused (T116) |
| `return`, `return LIST` | In | 8, 10 | in | D18 |
| Ending a sub in `if`, `unless`, a loop, a block or `try`, and using its value | Fault | 8 | | D18: perl returns the condition, or the `try`'s value |
| `wantarray` | Cut | | in | D18 |
| `die`, `try`, `catch` | In | 15 | in | |
| `finally`, `defer` | Later | 15 | out | Experimental in 5.42; to be proposed |
| `eval BLOCK`, `$@` | Cut | | out | D20: `try` |
| `eval STRING` | Cut | | out | D20 |
| `do BLOCK` | Later | 5 | | Small; when wanted |
| `do BLOCK while COND` | Later | | | D58: left out at step 6, for the step that takes `do BLOCK`. It runs the block first, and is not a loop to perl: `last` in it leaves the loop round it (T64) |
| `...` as a statement | Later | 15 | | It is a `die` |
| `given`, `when`, smartmatch | Cut | | | Not on under `use v5.42` either |
| `exit` | In | 21 | | |
| `say;`, `print;` with no argument | In | 10 | | They print `$_` |
| A builtin's brackets and then an operator, `say (1 + 2) * 3;` | Cut | | | D21, T25: perl prints 3 |
| `say (...)` after one space, not ending on its line, or with a bracket in a string or a comment that perl's count of them trips on | Cut | | | T76, T100: perl warns. `say(...)`, hard against, may run over lines |
| `(...) x N` as the whole argument of `say` or `print` | Later | 9 | | T101: perl repeats a list there. Refused until lists |
| `print STDERR ...`, `say STDERR ...` | In | 15 | | With `warn` |
| `1;` ending a module | In | 18 | | Not needed under `use v5.42`; harmless |

## Operators

Precedence and associativity are `perlop`'s. Chalk's
`PrecedenceTable.pm` is a tested reading of it.

| Construct | Here | Step | Note |
|---|---|---|---|
| `+ - *`, unary `-`, `%` | In | 1 | Int overflow faults (D23); `%` on a Num truncates, step 2; unary `-` on a string that isn't a number faults |
| `/`, `**`, float literals | In | 2 | Int or Num as perl has it (D35); a whole Num from 10^15 up to 2^53 faults when printed (D36); no infinity or NaN (D37) |
| `.`, `x` on a string | In | 3 | D44. After a value a dot joins, whatever follows (T90); `x` is a word of its own (T57), its count cut to a whole number; a count below zero faults, and a result of 2^31 characters or more |
| A string where a number is wanted | In | 3 | D40: perl's silent shapes, anything else faults. An Int or a Num by how it is written; a fault where perl has two answers by the string's past (`"1e16"`, `"3.0"` in arithmetic past 2^53, `"1.99999999999999999"` as a position) |
| Unary `-` on a string | In | 3 | D40: the Num, negated; a string that starts with `+`, or isn't a number, faults (T47, T85) |
| `+ - *` with an Int of 2^53 or more that is exactly a double, beside a whole Num or a string | Fault | 3 | D45: perl has two answers, by the Int's past (T92) |
| `== != < <= > >= <=>` | In | 4 | D49. A non-number faults (D15); two integral operands compare exactly, and otherwise as floats, as in perl (T39) |
| `eq ne lt le gt ge cmp` | In | 4 | D49. A number is compared as it prints; undef faults (D15) |
| `! && \|\| //`, `not and or xor` | In | 4 | D49. Truth is perl's: undef, `""`, `0`, `"0"` are false. `&& \|\| // and or` give an operand, and don't work the right one out unless it is needed |
| An unbracketed `!` on the left of a comparison, `!$x == $y` | Cut | | D50, T115: perl 5.42 warns of a precedence problem |
| `and`, `or`, `xor` after `say`'s argument; a word operator bare in a list of arguments; an operator that binds tighter than `not` after `not (...)` | Cut | | D51: perl reads each another way (T106, T107, T109) |
| `?:` | In | 4 | Not as an lvalue |
| `= += -= *= /= %= **= .= x= &&= \|\|= //=` | In | 5 | D56. The left side is a variable, bare. On undef, `+=`, `-=`, `.=`, `\|\|=`, `//=` and `++` are perl's, silently; `*=`, `/=`, `**=`, `%=`, `x=` fault (perl warns). `&= \|= ^= <<= >>=` come with their operators |
| An assignment to anything but a variable: `($x) = 5`, `($x = 5) = 7`, `(1 ? $x : $y) = 8` | Cut | | D17, D56: values flow, places don't; the first is a list assignment (step 9) |
| `++ --` | In | 5 | D52: by what the variable holds. A string is stepped as its number and is then a Num; one that isn't a number faults (perl's string increment is cut; its `--` gives -1 in silence); a fault where perl has two answers (T113), and on a Num of 2^53 or more, where perl warns `Lost precision` (T130) |
| A variable changed in the statement that reads it: `$x + ($x = 5)` | In | 5 | D14: read when its operator runs, as in perl (T110) |
| A concatenation whose later piece changes a variable an earlier piece reads: `$x . "a" . ($x = 5)` | Cut | | D57, T117: perl joins a row of dots as one operation and reads each piece late |
| `.=` whose right side is an assignment of a concatenation: `$t .= ($u = $x . $z)` | Cut | | D57, T129: perl 5.42 never makes the assignment |
| Chained comparisons, `1 < $x < 10`, `$a == $b == $c`, `"a" lt $s lt "c"` | Later | 4 | In perl since 5.32; refused, never read left to right (T33) |
| Mixing the non-associative operators, `1 <=> 2 == -1`, `1 .. 2 .. 3`, `0 < $o isa P` | Cut | | perl refuses each; the parser must too (T51, T52) |
| Unary `+` | In | 1 | `say +(1 + 2) * 3` is 9: perl's own way round T25. `+{` is always a hash |
| The comma operator in scalar position, `my $x = (4, 5, 6)` | Cut | | perl warns (D15). In the slots of a C-style `for`: In, step 6 |
| `-bareword` | Cut | | perl gives the string `-foo`, even under strict (T69) |
| `^^`, `^^=` | Later | 4 | New in perl 5.40 and 5.42 |
| `..` in list context | In | 9 | On numbers; a string as either end faults (perl's string ranges are string increment) |
| `..` and `...` in scalar context (flip-flop) | Cut | | |
| `x` on a list, `(1, 2) x 3` | Later | 10 | |
| `& \| ^ ~ << >>` | In | 22 | Numeric, as under `use v5.42`; a non-number faults |
| `&. \|. ^. ~.`, the string bit operators | Cut | | |
| `isa` | In | 17 | |
| `=~`, `!~` | In | 19 | |
| `\` on a variable, `[ ]`, `{ }`, `sub { }` | In | 13, 14 | |
| `\` on an element, a slice or a list | Cut | | D17 |
| `->[ ]`, `->{ }`, `->( )`, `->@*`, `->%*`, `->$*`, `->$#*` | In | 13 | |
| `@{ }`, `%{ }`, `${ }` circumfix | In | 13 | Postfix is preferred; both are perl |
| `@$x`, `%$x`, `$$x`, `$$x[0]`, `$#$x`: dereference without braces | Later | 13 | Stevan's own style guide forbids them; step 13 proposes cutting them |
| Arrows left out between subscripts, `$a[1][0]`, `$f->()()` | In | 13 | |
| A list slice `(LIST)[i]`; postfix slices `->@[...]`, `->@{...}`, `->%[...]` | In | 13 | |
| `\&name`, `defined &name` | Later | 14 | |
| `->&name(...)`, how a lexical method is called | Later | 17 | New in 5.42; not one of the `&` calls D21 cuts |
| `&$f()`, `&{$f}()`, `->&*` | Cut | | D21 |
| A string as a name (symbolic reference) | Cut | | strict refs: perl dies too |
| File tests, `-e` and the rest | Later | 21 | |
| `==` and `!=` between two references | In | 13 | Identity |
| `< <= > >= <=>` on a reference; `==` between a reference and a number | Fault | 13 | The order of two addresses (D14) |
| A reference as a string | Fault | 13 | D14 |

## Data

| Construct | Here | Step | Note |
|---|---|---|---|
| Int, Num, their literals: hex, binary, octal as `0o17`, `_` between digits, `.5`, `1e3` | In | 1, 2 | D23, D38. Hex, binary and octal up to 32 bits (perl warns past that). A hex float (`0x1p3`): Later |
| Octal by a leading zero, `017`; a point with nothing after it, `1.` | Cut | | D38: `010` is 8 (T24), and `0o17` says it; a dot after a number is concatenation (T78) |
| Infinity and NaN, `9**9**9`, `"inf"`, the builtins `inf` and `nan` | Cut | | D37: a Num is finite. `float overflow`, `not a number` |
| v-strings; a number with two dots | Cut | | `say 65.66.67` prints `ABC` (T62) |
| An identifier past ASCII, with `use utf8` | In | 5 | Until there are names: a character past ASCII outside a string or a comment is refused |
| `'...'`, `"..."` with escapes | In | 3 | D43. `\n \t \r \f \b \a \e \0`, `\\ \" \$ \@`, `\xHH`, `\x{...}`, octal, `\o{...}`, `\N{U+...}`, a backslash before a punctuation mark. A character is a Unicode scalar value (D42) |
| `\q` and other unknown escapes; `\x` with fewer than two digits; `\x{}`; an octal escape cut short by `8` or `9`; a backslash before a tab or a newline | Cut | | D43: perl warns, or makes a NUL in silence (T86, T95) |
| `\c`, `\N{name}`, `\U \L \u \l \Q \E \F` | Later | 16 | D43: with interpolation |
| An unescaped `$` or `@` in double quotes | Later | 16 | T34: refused until interpolation |
| Interpolation of `$x`, `${x}`, `@a`, elements, `->` chains | In | 16 | The shapes perl has to guess at are refused |
| `q`, `qq`, `qw`, heredocs | In | 16 | Chalk left heredocs out; a hand-written lexer needn't |
| `true`, `false`, `undef`, `defined` | In | 4 | D47: a boolean is 1 or 0 as a number, `"1"` or `""` as a string. D48: an undef where a number or a string is wanted faults; bare `undef` only where perl can't take what follows for its argument (T105) |
| Arrays: literals, `$a[i]`, negative index, `$#a`, `scalar(@a)` | In | 9 | |
| List assignment, `my ($p, $q) = @x`, swaps | In | 9 | The right side is finished first |
| `my $n = () = ...`, a list assignment's count as a number | Cut | | |
| A list assignment as a condition, `if (my @r = f())` | Later | 9 | It is the count, tested |
| An array in a scalar operand, `"x" . @a`, `-@a` | In | 9 | Its count, as in perl |
| Assigning to `$#a` | Cut | | |
| Slices `@a[...]`, `@h{...}`, `%h{...}`, `%a[...]` | In | 9, 12 | As values; on the left of `=`: Later |
| Hashes: literals, `$h{k}`, `exists`, `delete`, `keys`, `values` | In | 12 | Insertion order (D27) |
| `each`, the iterator | Cut | | D22 |
| A hash in list context | In | 12 | In its own order |
| Nested data through references | In | 13 | |
| Writing through undef (`$h{a}{b} = 1`, `push $h{k}->@*, 1`) | In | 13 | perl's, silently |
| Reading through undef or a missing key (`$h->{a}{b}`), in an expression, a `foreach`, a `map` or `keys` | Fault | 13 | perl creates `$h->{a}`; to be proposed |
| `ref`, `reftype`, `blessed`, `refaddr` | In | 13, 17 | The last three are imported by `use v5.42`; `refaddr`'s number is unspecified |
| `weaken`, `unweaken`, `is_weak`, `is_tainted` | Cut | | D26; all imported by `use v5.42`, so the names are still taken (D21) |
| Typeglobs, `*name`, filehandles as barewords | Cut | | Except `STDIN`, `STDOUT`, `STDERR` |
| `=>` quoting the word on its left, `q`, `y`, `s` and `time` included | In | 12 | The lexer looks for `=>` before taking `q` as a quote operator |
| A number as a hash key, `(010 => "a")` | In | 12 | The key is the number as a string, `8` (T63) |
| `qw` with commas in it | Cut | | perl warns (D15) |
| `keys`, `values`, `exists`, `delete` on an array | Later | 9 | |
| `$\|`, `$?`, `$.`, `$^O`, `$0` | Later | 21 | `$\|` first; the rest when wanted |
| `%SIG`, `@INC`, `%INC`, `$^W`, `` $` ``, `$'`, `@-`, `@+` | Cut | | |

## Builtins

The table of builtins (D29) is this section made exact. Types are in
Opal's notation, `docs/BUILTINS.md`.

| Family | Here | Step |
|---|---|---|
| `say`, `print` to stdout | In | 0, 3 |
| `length`, `uc`, `lc`, `ord`, `chr`, with brackets or as named unary operators (D41); `substr` (reading, 2 or 3 arguments) and `index` (2 or 3), in brackets | In | 3 |
| `ucfirst`, `lcfirst`, `rindex`, `substr` with 4 arguments, `reverse` of a string, `sprintf`, `printf`, `join`, `chomp` and `chop` of a variable | In | 16 |
| `uc`, `lc` of a character past ASCII (T45, until perl's tables are in) | Fault | 3 |
| `chr` of a surrogate, of a number past U+10FFFF or below zero; printing a noncharacter | Fault | 3 |
| `substr` and `index` without brackets; a sign after a named unary operator that perl calls ambiguous, `length - 5` | Cut | |
| `substr` on the left of `=`, `vec`, `pos`, `lc` and friends without an argument | Cut | |
| `push`, `pop`, `shift`, `unshift`, `splice`, `reverse`, `sort`, `map`, `grep`, `join`, `scalar` | In | 9, 10 |
| `sort` with `$a` and `$b` | In | 10 |
| `any`, `all` (experimental in 5.42, and not in the bundle) | Later | 10 |
| `map EXPR, LIST`, `grep EXPR, LIST` | In | 10 |
| `ceil`, `floor`, `trim`, `indexed` (imported by `use v5.42`), `fc` | Later | 16, 22 |
| `abs`, `int`, `sqrt`, `sin`, `cos`, `atan2`, `exp`, `log`, `hex`, `oct` | In | 22 |
| `rand`, `srand`, `time`, `localtime`, `gmtime`, `sleep` | Later | 22 |
| `split`, `m//`, `s///`, `tr///`, `qr//`, `quotemeta` | In | 19, 20 |
| `die`, `warn` | In | 15 |
| `open` with three arguments, `close`, `readline` and `<$fh>`, `eof`, `print {$fh}`, `binmode`, `opendir` and the directory calls, `unlink`, `rename`, `mkdir`, `stat` | Later | 21 |
| `@ARGV`, `%ENV`, `$0`, `$!` in a message | Later | 21 |
| `system`, backticks, `exec`, `fork`, `wait`, `kill` | Later | a library, when proposed |
| Sockets, `getpw*` and the system databases, `select` on handles, `ioctl`, `fcntl` | Later | a library, if ever |
| `pack`, `unpack` | Later | with bytes |
| `caller` | Cut | |
| `local $_`, `$,`, `$\`, `$/`, `$;`, `$"`, `$[`, `$0` assignment | Cut | |
| `tie`, `tied`, `untie`, `dbmopen`, formats, `write`, `reset`, `dump`, `lock`, `study`, System V IPC | Cut | |

## Regexes

Perl 5's syntax and matching order, a subset, compiled by the compiler
(steps 19 and 20). A pattern is known at compile time or built from
`qr` objects that are; a construct outside the subset is a refusal
that names it.

| Construct | Here | Step |
|---|---|---|
| Literals, classes, `.`, anchors (`^ $ \A \z \Z \b`), `\d \w \s`, `* + ? {n,m}` greedy and lazy, groups, `(?:...)`, alternation, captures, backreferences | In | 19 |
| `\d` and `\w` match Unicode digits and letters; `$` matches before a final newline | In | 19 |
| `m{...}`, `s{...}{...}` and other delimiters | In | 19, 20 |
| The empty pattern, `$s =~ //` | Cut | |
| Lookaround, possessive quantifiers, POSIX classes, `(?i)`, the flags `/a /u /n /p` | Later | 19 |
| `/i /m /s /x /g` | In | 19, 20 |
| A match in list context returning its captures | In | 19 |
| Named captures, `%+` | Later | 20 |
| `$1`, `$2`, `$&` | Later | 19; their dynamic scope is the cost |
| `s///`, `s///g`, `s///r`, `tr///`, `split` | In | 20 |
| `qr//` and interpolating one into a pattern | Later | 20 |
| A string interpolated as a pattern | Cut | |
| `while ($s =~ /x/g)`, a `/g` match in scalar position | Later | 20 |
| `s///e`, `(?{ })`, `pos`, `\G`, recursion, backtracking verbs | Cut | |
| Unicode properties, `\p{...}` | Later | when proposed |

## Classes

`feature 'class'` as perl 5.42 has it (D19).

| Construct | Here | Step |
|---|---|---|
| `class Name { }`, `class Name;` | In | 17 |
| `field $x`, `field @a`, `field %h`, defaults | In | 17 |
| `:param`, `:reader` | In | 17 |
| `:writer` | Later | 17 |
| `method name (signature) { }`, `$self`, lexical methods | In | 17 |
| `ADJUST` | In | 17 |
| `:isa(Parent)` | In | 17 |
| `Name->new(k => v)`, `$obj->method(...)` | In | 17 |
| `$obj->$name(...)`, a method chosen by a string; a class named by a string | Later | 17 |
| `$obj->m` and `Name->new` without brackets | In | 17 |
| A method named for a builtin, `method keys` | In | 17 |
| `$self->SUPER::m()` | In | 17 |
| `method name { }` without a signature; a parent's field read in a subclass; `:isa` of a class the program doesn't define | Cut | |
| `class Name VERSION`, `:param(name)`, `:reader(name)`, `sub` inside a class, `my method` | Later | 17 |
| `__CLASS__`, `isa`, `ref($obj)` | In | 17 |
| `DESTROY`, `AUTOLOAD`, `can` to fetch code, `bless`, `@ISA`, overloading | Cut | |
| `role`, `:does` | New | 27 |
| A metaobject protocol | New | 28 |

## What the erasure removes

Nothing yet. From step 25: type annotations.
