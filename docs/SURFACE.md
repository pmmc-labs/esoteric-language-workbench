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

Nothing is built, so "In" is a plan and not a fact.
[`TRAPS.md`](TRAPS.md) has the programs that show why a row says
what it does.

"Chalk" in the last column says what Chalk's declared subset does, for
comparison: *in*, *out*, or *n/a*.

## Program and declarations

| Construct | Here | Step | Chalk | Note |
|---|---|---|---|---|
| `use v5.42;` first | In, required | 0 | in | D16 |
| `use utf8`, `use experimental '...'` | In | 3, 17 | in | D16 |
| `use Module;` of the program's own | Later | 18 | in | Compile time only |
| `use Module qw(names)`, `Exporter` | Later | 18 | in | To be proposed |
| `no strict`, `no warnings`, `use integer`, `use bytes` | Cut | | | D16 |
| `use open ':std', ':encoding(UTF-8)';` | Later | 3 | | The file would then say what the oracle's `-CSDA` says: plain `perl` prints `é` as one byte |
| `use constant`, `List::Util`, `Scalar::Util`, `POSIX`, other core modules | Later | 18, 23 | | D16: refused until proposed |
| `require`, `do FILE` at run time | Cut | | out | D20 |
| `package Name;` naming a file's subs | In | 18 | out | D19: a namespace and nothing more |
| `Name::f($x)`, a sub of another package | In | 18 | in | |
| `package Name { }`, `__PACKAGE__`, imports | Later | 18 | | |
| `BEGIN`, `END`, `INIT`, `CHECK`, `UNITCHECK` | Cut | | in | D20; `BEGIN` as evaluation is parked |
| `__DATA__`, `__END__`, POD | Cut; POD later | 16 | out | POD is a comment, when someone wants it |
| `my $x`, `my @a`, `my %h`, `my (...)` | In | 5, 9, 12 | in | |
| `my` under a statement modifier, or right of `&&`, `\|\|`, `//` | Cut | | | D21: perl keeps the old value |
| A second `my` of a name in one scope | Cut | | | D15: perl warns |
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
| Signature placeholders `$`, `@`, `%`; defaults with `//=` and `\|\|=`; a default that reads an earlier parameter | In | 8 | | |
| `my $x = $x`: the right side sees the outer `$x` | In | 5 | | T58 |
| `my` in a condition, `if ((my $n = f()) > 3)` | In | 5 | | |
| `my (undef, $x) = ...` | In | 9 | | |
| `my $a`, `my $b` | Cut | | | T61: perl warns, and `sort` then misbehaves |
| `\my $x`, `foreach \my %h (...)` | Cut | | | Not in the `use v5.42` bundle |
| Attributes other than the class ones | Cut | | | `:lvalue` among them |

## Statements and control

| Construct | Here | Step | Chalk | Note |
|---|---|---|---|---|
| `if`, `elsif`, `else`, `unless` | In | 5 | in | |
| `EXPR if COND`, `unless` | In | 5 | in | |
| `while`, `until`, postfix forms | In | 6 | in | |
| `for (init; cond; step)` | In | 6 | in | |
| `foreach my $x (LIST)` | In | 9 | in | `$x` is read-only; every container that can reach the list is frozen (D17) |
| `foreach $x (LIST)` with a variable that isn't `my` | Cut | | in | T14 |
| `foreach` with no variable, postfix `for` | In | 10 | in | `$_`, read-only, and only inside the block that binds it |
| `foreach` over `($p, $q)` naming variables | Later | 9 | in | D17: perl aliases them |
| A closure over, or `\` of, a loop variable or `$_` | Later | 14 | in | D17: perl keeps the alias after the loop |
| `foreach my ($k, $v) (%h)` | Later | 12 | | 5.36's; to be proposed |
| `last`, `next`, labels | In | 6 | in | Only inside a loop of the same sub, as written |
| `last` or `next` reaching a loop from a called sub, or from a `map`, `grep` or `sort` block | Cut | | | T59, T60: perl leaves the outer loop |
| `redo`, `goto`, `continue` blocks | Cut | | out, `redo` in | |
| Bare blocks | In | 5 | in | A loop that runs once, for `last` and `next` (step 6); a label on one: cut |
| `return`, `return LIST` | In | 8, 10 | in | D18 |
| Ending a sub in `if`, `unless`, a loop, a block or `try`, and using its value | Fault | 8 | | D18: perl returns the condition, or the `try`'s value |
| `wantarray` | Cut | | in | D18 |
| `die`, `try`, `catch` | In | 15 | in | |
| `finally`, `defer` | Later | 15 | out | Experimental in 5.42; to be proposed |
| `eval BLOCK`, `$@` | Cut | | out | D20: `try` |
| `eval STRING` | Cut | | out | D20 |
| `do BLOCK` | Later | 5 | | Small; when wanted |
| `do BLOCK while COND` | Later | 6 | | Runs the block first, and `last` doesn't work in it (T64) |
| `...` as a statement | Later | 15 | | It is a `die` |
| `given`, `when`, smartmatch | Cut | | | Not on under `use v5.42` either |
| `exit` | In | 21 | | |
| `say;`, `print;` with no argument | In | 10 | | They print `$_` |
| `print STDERR ...`, `say STDERR ...` | In | 15 | | With `warn` |
| `1;` ending a module | In | 18 | | Not needed under `use v5.42`; harmless |

## Operators

Precedence and associativity are `perlop`'s. Chalk's
`PrecedenceTable.pm` is a tested reading of it.

| Construct | Here | Step | Note |
|---|---|---|---|
| `+ - *`, unary `-`, `%` | In | 1 | Int overflow faults (D23); `%` on a Num truncates, step 2; unary `-` on a string that isn't a number faults |
| `/`, `**`, float literals | In | 2 | Int or Num as perl has it; one part unfinished (D23) |
| `.`, `x` on a string | In | 3 | |
| `== != < <= > >= <=>` | In | 4 | A non-number faults (D15); an Int and a Num compare as floats, as in perl |
| `eq ne lt le gt ge cmp` | In | 4 | undef faults (D15) |
| `! && \|\| //`, `not and or xor` | In | 4 | Truth is perl's: undef, `""`, `0`, `"0"` are false |
| `?:` | In | 4 | Not as an lvalue |
| `= += -= *= /= %= **= .= x= &&= \|\|= //= &= \|= ^= <<= >>=` | In | 5 | On undef, `+=`, `-=`, `.=`, `\|\|=`, `//=` and `++` are perl's, silently; `*=`, `/=`, `**=`, `%=`, `x=` fault (perl warns) |
| `++ --` | In | 5 | On a non-numeric string: fault (perl's string increment is cut; its `--` gives -1 in silence) |
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
| Int, Num, their literals: hex, binary, octal as `0o17` and `017`, `_`, `.5`, `1.`, `1e3` | In | 1, 2 | D23. A hex float (`0x1p3`): Later |
| v-strings; a number with two dots | Cut | | `say 65.66.67` prints `ABC` (T62) |
| An identifier past ASCII, with `use utf8` | In | 3 | |
| `'...'`, `"..."` with escapes | In | 3 | |
| Interpolation of `$x`, `${x}`, `@a`, elements, `->` chains | In | 16 | The shapes perl has to guess at are refused |
| `q`, `qq`, `qw`, heredocs | In | 16 | Chalk left heredocs out; a hand-written lexer needn't |
| `true`, `false`, `undef`, `defined` | In | 4 | |
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
| `length`, `uc`, `lc`, `ucfirst`, `lcfirst`, `index`, `rindex`, `substr` (reading, and 4 arguments), `chr`, `ord`, `reverse` of a string, `sprintf`, `printf`, `join`, `chomp` and `chop` of a variable | In | 3, 16 |
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
