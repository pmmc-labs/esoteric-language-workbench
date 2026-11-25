# Background

What was read before the design, what was borrowed, and what is parked.
Five repositories, read on 2026-11-24 as shallow clones; the paths
below are into them, so a claim can be checked. Four were read before
the design was written; Crayon after it was decided, against it.

| Repository | At | What it is |
|---|---|---|
| `stevan/chalk` | 93c01e4 | perigrin's compiler for a Perl subset, written in Perl |
| `stevan/perl5-son` | 40e86a6 | Its current front end: perl's optree to a Sea of Nodes graph |
| `stevan/pp` | 438994d | Opal, Stevan's TypeScript interpreter for a Perl, 2025 |
| `stevan/Allium` | 59291d6 | Stevan's model of perl's opcodes and optrees, 2024 |
| `stevan/p5-Crayon` | 58c87d6 | A parser front end for a Perl 5.42 subset, one day in March 2026 |

The process is `pmmc-labs/esoteric-language-workbench` at af8e3a3, and
its `interpreter` branch.

## Chalk

**What it is now.** The README and `ARCHITECTURE.md` describe an
Earley parser with semirings feeding a Sea of Nodes graph. That
pipeline is paused. Since June 2026 the graph comes from perl's own
parser, through perl5-son, and the parser is called "untrusted,
paused" (`docs/plans/2026-06-06-three-axis-codegen-and-typed-ir-contract.md`).
The live path is perl, then B::SoN, a JSON wire, a loader, a typing
pass, and LLVM IR run by `lli`, with its output compared to perl's.

**The subset** (borrowed: D4). `docs/chalk-grammar-spec.md` is a real
specification of a Perl subset, with what is in and what is out, and
`docs/chalk-bootstrap.bnf` is its grammar. `SURFACE.md` here starts
from it. Two cautions. The subset Chalk's code is held to is the
declared one, by `t/grammar-conformance.t`; the rules in its
`CLAUDE.md` (all classes, no `@_`, no outside modules) are not yet
true of its own `lib/`. And the live pipeline accepts far more than
the declared subset, since perl does the parsing.

**The parser** (not borrowed: D6). A flat, deliberately ambiguous
grammar, with precedence, builtin arity and block-or-hash left to
filters.

- Speed: 7 seconds for 2.6 KB, 126 seconds and 609 MB for 15 KB
  (`docs/plans/2026-04-30-parser-performance-investigation.md`).
- List operators without brackets were rolled back after needing
  eight special cases; the lesson recorded is "precedence levels are
  for operator binding, not for parser state"
  (`docs/plans/2026-05-12-list-operators-as-predeclared.md`). D21 is
  the answer taken here.
- `lib/Chalk/Grammar/Perl/PrecedenceTable.pm` is a correct, tested
  reading of `perlop`'s table, with the named unary operators and the
  list operators placed. Worth reading when the parser is written.

**The backend.**

- A value is a tag and a 64-bit payload, unboxed where types prove it
  (`lib/Chalk/Target/LLVM/Runtime.pm`). D25 is the same shape.
- Strings are bytes; `chr` above 255 stops at run time. D24 goes the
  other way.
- A hash is an array of pairs searched in a line; its order isn't
  perl's and the corpus is normalised for it.
- Nothing is ever freed, and `DESTROY` is refused.
- `die` is a global flag tested after every call.
- The C and XS backends were dropped; the runtime is 7,800 lines of
  LLVM IR in a Perl string.

**Self-hosting.** Chalk's grammar recognises its own source. Compiled
natively, of 288 of its own test files, 2 run as perl runs them and
281 are refused (`docs/plans/2026-11-17-test-chalk-measured.md`).

**Findings borrowed.**

- perl decides between integer and float by the value
  (`docs/plans/2026-09-04-perl-decides-repr-by-value-not-type.md`):
  D23.
- The lattice of types, `Int <: Num <: Str <: Scalar`, with Boolean,
  Undef and the references under Scalar and not under Str
  (`lib/Chalk/Grammar/Perl/TypeLibrary.pm`, and
  `docs/architecture/perl-type-system-formal.md`). `Maybe[T]` as the
  one union Perl makes. For step 25.
- The verdicts: SAME, REFUSED, LOUD, and never WRONG; "a GAP is a
  compilation failure, not a resting state". D2, D11.
- strict and warnings built in, not switchable: D16.
- "IV, UV and NV are perl5's implementation, not Perl the language."

**Process lessons borrowed.** A migration was declared final at a
third done; a staleness audit of 21 plan documents found 9 with false
claims; acceptance checks passed because the command they ran didn't
exist. The workbench's answer, one Status paragraph and decisions
with numbers, is the one used here; there is no `docs/plans/`.

## perl5-son

**What it is now.** The README is stale. It is a 25,000-line
translator from perl's optree to a graph of 109 kinds of node, with a
memory model, a verifier and a wire format; `docs/son-ir-and-wire.md`
is the current description. `docs/memory/` is the agent's memory, 309
notes, not a specification.

**The memory model, and what it cost** (the evidence for D6). One
goal, "make the memory model mechanical and checked", took a plan of
81 KB, ten stages, four audits and about 2,150 probes. The last audit
(`docs/research/2026-11-24-memory-model-final-audit.md`): "The gates
hold. The goal's first sentence does not." 1,451 gated probes with no
wrong answer; 847 fresh ones with 111, on graphs the verifier passed.
Its own diagnosis: "In LLVM, MemorySSA is derived from ordered
instructions and can be verified against them. Here it is the only
order and the optree is gone. So the verifier proves the wire
well-formed, never that it is the program."

**The expensive semantics, ranked** (the evidence for D14, D17, D18).
From the audits' classes of wrong answer, with what this language does:

| Perl 5 behaviour | Example, and what perl prints | Here |
|---|---|---|
| Implicit aliasing: `@_`, `foreach`, `$_`, `map` | `for my $x (@a) { $x *= 2 }` rewrites `@a` | Refused or frozen (D17) |
| `local` and unwinding | A restore on every way out of a scope, a `die` included | Refused (D17) |
| Everything is an lvalue | `($x = 5) += 2` is 7; `($c ? $a : $b) = 9` | Refused (D17) |
| List assignment and context | `sub a { return @a }` gives a count to a scalar | Syntax only; faults through a call (D18) |
| Autovivification by reading | `$h->{a}{b}` read makes `$h->{a}` | Faults (step 13) |
| Operands read late | `say f(1), $r->[0], f(0), $r->[0]` prints `1000` | Followed (D14) |
| Regex captures' dynamic scope | `$1` restored at the end of a block | Step 19 proposes |
| `bless` changes a value others hold | `ref($o)` before and after | Refused (D19) |
| Glob assignment | "One op, six behaviours" | Refused (D19) |
| `goto` | Three unrelated constructs under one name | Refused |
| String increment | `"Zz9"++` is `"AAa0"` | Fault on a non-number |
| The iterator a hash carries | `each`, reset by `keys` | Refused (D22) |
| `tie`, `DESTROY`, formats, run-time `eval` | Refused there too | Refused |

**The corpus** (to borrow, with permission: D11).

- About 3,000 one-line programs written to find wrong answers:
  `t/corpus/probes/` (1,054), and under
  `docs/research/son-ir-audit-2026-11-19/probes/` the directories `p`
  and `q` (418), `a` (288), `r` (499), `f` (847). Chalk's
  `t/data/audit-probes/` holds 1,451 of them with a baseline.
- `t/corpus/mdtest/pvm/`: 441 cases in 67 topic files, graded in 14
  tiers from literals to recursion, each with the program and perl's
  exact output, in a format (`FORMAT.md`) made so several
  implementations can share a file. pvm is a separate Perl
  implementation (pvm.tools) the corpus was copied from.
- Chalk's own `t/corpus/mdtest/`, 257 cases.

**Lessons about agents, borrowed into `CLAUDE.md`.**

- "Six live miscompiles once passed a green suite because every check
  read the graph and none ran the program." Tests here run programs.
- "A probe set measures itself." Hence the census of probes nobody
  wrote for this implementation (D11).
- Harness errors made facts: a loop that ate its own input reported
  986 of 986 clean when 857 were. Hence: make a check fail on purpose
  before trusting it.
- "perl is the oracle, and memory was wrong twice." Hence: never
  write what perl does from memory. (While this spec was written, the
  agent recalled `2 ** 62` as an exact integer; perl prints
  `4.61168601842739e+18`.)

## Opal (`stevan/pp`)

A three-week proof of concept, about 5,000 lines of TypeScript: a copy
of perl's optree, threaded by `op_next` and run over a value stack. It
runs recursive functions, `if`, `while` and scalar lexicals.

**The design notes are the asset**, and this spec is their second
attempt:

- `docs/NOTES.md`: the goal (D1).
- `docs/DESIGN.md`: "The biggest difference is the introduction of an
  AST phase, which `perl` does not have. It is during this phase when
  we can perform things like type checking and static analysis." And
  perl as "a partial reference implementation", to "reduce decision
  fatigue and remove the temptation of Second System Syndrome". D2 is
  that idea made a rule, with perl's output in place of its optree.
- `docs/HISTORY.md`: the 2007 conversation with mst: a small set of
  primitives, `map` and `grep` as a fold, "half the ops could be
  imports". D22, and step 23.
- `docs/BUILTINS.md`: a first list of builtins with types. For
  `SURFACE.md` and step 25.
- Decisions visible in its code: real booleans, signatures and no
  `@_`, brackets on calls. Kept (D17, D21).

**Not borrowed.**

- Unifying `==` and `eq`: it changes what a program means, against D2.
- `+[ ]` and `+{ }` as the only literals: D21 handles the guess
  instead.
- The front end: no precedence (`10 - 2 - 3` is 11), no positions,
  operators lost by the tokenizer. D29 lists what it taught.
- The run-time model: lexicals found by name through the callers'
  frames, which is dynamic scope; values left on the stack by a
  statement leak into the next.
- Compiling one statement at a time, as a stream.

**To port as examples** (step 24): the programs in `t/*.t` and
`tests/`: factorial, Fibonacci, gcd, even and odd, 99 bottles,
Ackermann, Hanoi, Collatz. `lib/Test.opal.pm`, a TAP library in the
language, once it no longer leans on dynamic scope.

## Allium

A serializable mirror of perl's opcodes, optrees, pads and stashes.
Two things in it are design and not mirror:

- **The triage of perl's 415 opcodes**
  (`dev/data/opcode-categories.csv`, defined in
  `docs/INSTRUCTION-SET.md`): Core 248, IO 84, OS 42, Processes 10,
  Deprecated 24 ("not going to support": `tie`, `each`, dbm, SysV IPC,
  `reset`, `dump`), Prohibited 7 ("not going to allow": string `eval`,
  block `eval`, `do FILE`, custom ops). D20 and D22. It began as an
  import of `Safe`'s opcode tags and was edited by hand; it is a first
  pass, and treated here as one.
- **A numeric tower** (`lib/Allium/Type/`): "a small numerical tower
  (borrowed from Scheme) ... each type can contain all the types above
  it this better matches the way Perl behaves". The same shape as
  Chalk's lattice, arrived at separately.

What its data shows about perl's own form, and why none of that form is
copied: in its 34 sample programs 18% of the ops are ones perl
nullified, more pad entries are unnamed temporaries than variables,
and many "Core" opcodes are the optimizer's fused pairs. The argument
vocabulary of its opcode prototypes (Scalar, Numeric, Array, Hash,
Code, List, optional) is a good shape for the table of builtins (D29).

## Crayon

A tree-sitter-perl parse turned into a tree of plain hashes; the
interpreter planned on top was written and deleted the same day. Its
goal (`docs/superpowers/specs/2026-03-31-chalk-ast-design.md`): "a
Pugs-style experimentation ground for prototyping changes to the Perl
5 core". It changed no decision here. What it gave:

- **A vocabulary for the syntax tree** (`lib/Crayon/AST.pm`, 53 kinds
  of node, each a hash with a `type`). The right grain for statements
  and declarations, and it ports to a TypeScript union as it stands.
  It has no positions, no context and no binding of a use to its
  declaration, each left out on purpose there and each needed here
  (D29, D18); and it runs together things this design tells apart:
  `my ($x) = ...` and `my $x = ...`, `return` and loop control, a
  slice and a subscript, a call through a reference and a method
  call. Step 1 starts the tree from it, with those changes.
- **About fifty rows `SURFACE.md` had missed**, from what its grammar
  and tests reach for: unary `+`, the comma operator, the operators
  that don't associate, v-strings, `=>` quoting, dereference without
  braces, loop control that leaves a `map`, and most of `perlclass`.
- **Traps T51 to T71**, among them a kind the first fifty lacked:
  programs an obvious parser accepts and perl refuses.
- **`writing-perl-5.42.md`**, Stevan's style guide for agents writing
  Perl: `use v5.42; use utf8;`, signatures and never `@_`, `class`
  over hashes, postfix dereference and never `@$ref`, `+{ }` for a
  hash, `qw[ ]`, `say`. It is the baseline for examples and ports
  (D8), and agrees with D16, D17, D19 and D21 where it speaks. Three
  things in it to check against 5.42 before leaning on it (read from
  5.42's own documentation, not run): `is_bool` is not imported by
  `use v5.42`, and `reftype` and `is_tainted` are; a lexical method
  is called with `->&`, not `->`; and `:writer` makes `set_x`. It
  also asks for `use open ':std', ':encoding(UTF-8)';`, which is the
  question step 3 has to settle.
- **About 25 small programs** in its plan, for the example table.

Not borrowed: tree-sitter-perl as the parser (D6, D29; and it accepts
`role`, `BUILD` and `sub n(:$x)`, none of which is Perl, so it is no
oracle); `perlish.bnf`, a second and wider grammar than Chalk's, with
no precedence in it and its text damaged by a round trip through a
rich-text editor, useful as a checklist to read and not as input to
anything; the plan's execution model, which had no context, let a
program's sub shadow a builtin, and ran `last` and `return` as host
exceptions that its own `try` would have caught. Its plan held every
line of code in advance and was abandoned in its first afternoon,
which is one more reason there is no `docs/plans/` here.

## To read when classes are proposed

Two of Stevan's repositories, for roles, which he wants in the object
system from the start (`PLAN.md`, step 17, has the note and what each
holds): `stevan/p5-roles-algebra`, an algebra of role composition for
`feature 'class'` with tests of it against Moose, Moo, Role::Tiny,
Object::Pad and the mop; and `stevan/p5-core-role-tests`, programs
written for roles in core. perl 5.42 compiles neither `role` nor
`:does`. Not read closely yet: nothing here is borrowed from them so
far.

## Parked, with the reason, so each stops coming up

- **Sea of Nodes, or any optimizing middle.** D6. Types (step 26) are
  how checks get removed; the C compiler does the rest.
- **An Earley or generalized parser.** D6.
- **Self-hosting.** D6. Possible later; nothing waits on it.
- **LLVM as the target.** D3. C through a target interface; a native
  target when something needs one.
- **Byte-identity with perl where perl changes from run to run**
  (hash order, addresses). D14. Where perl is fixed and merely odd,
  it is followed: Chalk ported perl's merge sort to match the order
  of a comparator's calls, and step 10 weighs doing the same.
- **`DESTROY`, reference counting.** D26.
- **`local`.** D17. To return, if at all, as a variable local to a
  task, with concurrency.
- **`BEGIN` as partial evaluation.** D20.
- **Grammars and rules; multiple dispatch; macros; lazy lists;
  junctions.** D5: not picked.
- **CPAN, XS, embedding perl.** D1.
- **Bignums and rationals.** D23.
