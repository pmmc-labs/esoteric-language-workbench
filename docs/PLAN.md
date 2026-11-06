# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** steps 0 to 5 are done. Step 5 (D20 from the person; D21 to D27 defaults, still for the person to confirm) landed as proposed. Step 6 is a placeholder, not yet planned.

Read [`DESIGN.md`](DESIGN.md) first. Where a step meets an **(open)**
item, propose options to the user before building (see `CLAUDE.md`).

## Proposed layout

[The tree as planned. `CLAUDE.md` has the layout as built; when they
differ, this stays as a record of the plan.]

## Steps

Each step says what it adds, what it touches, what tests it adds, and
what it leaves out on purpose. A step marked **(done)** keeps its text,
with a note where what landed differs.

### 0. Scaffold (done)

- The build: `bin/langc.ts` reads a file, compiles it to C next to the
  output, and links it with `runtime/rt.c` by `cc` (`LANG_CC` overrides);
  `make test` runs the unit tests then the golden tests. C rather than
  assembly, so step 0 runs on any machine with a C compiler; a native
  target comes when the language needs one, through a target interface.
- The reader (`compiler/src/reader.ts`): integers, symbols and lists,
  each form with its line and column; `;` comments. Unit tests in
  `compiler/tests/`.
- A compiler for one kind of literal (`codegen.ts`): a program that is
  `42` compiles to a binary that prints `42`. Integers are 63 bits,
  shifted left one, tag 0 (`runtime/rt.h`); one past the range is a
  compile error, checked by a unit test since the golden runner calls a
  failed compile a failure.
- `t/run.sh`: compile each golden test, run it with the environment the
  tests assume (none yet; the knobs go there as the runtime gains them),
  compare stdout and stderr together with the `.expected` file, plus
  `exit: N` when the status isn't 0, `JOBS` at a time, with a watchdog.
- Golden tests 000 and 001, their outputs by hand.

Each step carries a **Referee** line, set when the step is proposed:
`extend t/referee/NAME.py to cover this`, or `none`, with the reason
(`docs/PROCESS.md`, "The referee"), and a **Size** line, the capability
the step needs of the agent that builds it, by `docs/MODELS.md`'s tiers: *large* where
there's a decision to propose, a runtime mechanism to design, or a
model to write; *medium* where the design is agreed and the step
describes its tests; *small* where the step is a pattern to repeat.
A session's first move is to compare its own model with the step's size.

### 1. Arithmetic (done)

Size: large, for the model and the decisions; medium once they're
written.

- `(+ a b)`, `-`, `*`, `/`, `%`, nested, on 63-bit integers (D3, D4,
  D5); the runtime's checked operations in `runtime/rt.c`, the
  operator table in `codegen.ts`.
- Faults: overflow and division by zero end the program with a message
  and exit 1 (D6).
- `t/models/arith.py`: the operators over the edge values, Python's
  integers with the range and the division rule applied after. It
  writes tests 010 (every pair that gives a value, folded into one
  expression) and 011 to 015 (each a fault). The first version of the
  model folded a term before reducing it and overflowed: the compiler
  found the model's bug, which is the other half of why a model is
  worth having.
- The mechanical checks, `t/checks.py` (D8, D10): `models`, `tests`,
  `commits`, and the hook.
- Compile errors (arity, an unknown name, not an operator) as unit
  tests (D7).

### 2. Booleans, comparisons and `if` (done)

Size: medium. The decisions were made (D11 to D14), the model is
`t/models/compare.py`, and the tests 020 to 024 were red until the step. It
is done: `make test`, `make sanitize` and `make golden-clang` pass with no
test or model changed. One thing landed differently from the text: the
reader still makes `#true` and `#false` symbols, and `codegen.ts` gives them
their meaning.

The experiment's record is in `docs/MODELS.md`. Two models built this
step cold from the same commit: Sonnet's build is the branch
`step2-sonnet`, Haiku's `step2-haiku`, which is what main took; Haiku
again at low and at high effort are `step2-haiku-low` and
`step2-haiku-high`. What the
step's text lacked, found by both: it named only code and tests, so
neither was told to move `LANGUAGE.md`, the plan's heading or the
Status; Sonnet left them, Haiku moved them. A step says which documents
it moves, and "done when" includes them.

- `#true` and `#false` (D11): read as themselves (today the reader
  makes them symbols; either the reader or `codegen.ts` may give them
  their meaning, but `(+ #true 1)` must fault at run time, not fail to
  compile, since D11 says what it does). An immediate with its own tag
  (D14), in `runtime/rt.h`; `rt_print` prints them as written.
- The six comparisons (D12), as runtime functions beside the arithmetic
  in `rt.c`, through the operator table in `codegen.ts`. The orderings
  check both arguments are integers; `==` and `!=` compare any two
  values.
- The arithmetic checks its arguments are integers (D14), faulting
  `not an integer`; before this step nothing but an integer could reach
  it.
- `(if test then else)` (D13): a special form in `codegen.ts`, not an
  operator, since only the taken branch runs. The test is checked to be
  a boolean at run time, faulting `not a boolean`. C's `?:` does this;
  a form with other than three parts is a compile error, as a unit test.
- Tests: 020 (every comparison over the edge values, counted with `if`,
  from the model), 021 to 024 (by hand: a boolean printed; only the
  taken branch runs; `not an integer`; `not a boolean`). Unit tests for
  the compile errors (`if` with two parts; `(if)`).
- Leave out: `and`, `or`, `not`, `cond`, truthiness, anything else.
  Report, don't add, if something seems to need them.

### 3. Bit operations (done)

Referee: `t/referee/calc.py` covered this before the trials, kept out
of the repo then, in since; it judged both builders' models.

Size: large, for the model; the build is medium once the model and its
tests exist. The decisions are made (D15 to D17). No model and no tests
existed: this step's first work was `t/models/bits.py`, and the tests it
writes, 030 and up, before any code changed. The step is done when
`make test`, `make golden-clang` and `make sanitize` pass, the model
lists every file it writes (`make checks` holds it to that), and
`LANGUAGE.md`, this heading and `CLAUDE.md`'s Status are moved.

What landed differently from the text: the model folds its terms as a
balanced tree, not a chain, since clang stops at 256 levels of brackets
and the chain's 500 nested terms didn't compile under it. The shape of
the program is the only thing the model chooses; every value is computed
from the definition. The
step didn't name the compile-error unit tests for the bit operations'
arity and `bit/not`; they were added to `compiler/tests/codegen.test.ts`.

- `t/models/bits.py` first: the five operations over values that find
  the edges, from the definition in D15 and D16 and nothing else. The
  model's job is to compute what the decisions say, not what the
  runtime does; `t/models/README.md` says how, and `arith.py` and
  `compare.py` are the shape. Expected outputs for every value and
  every fault the decisions name, 030 and up, each fault in a test of
  its own since a fault ends the program (as 011 to 015).
- Then the operations, as runtime functions beside the arithmetic in
  `rt.c`, through the operator table in `codegen.ts`. `bit/shl` checks
  its result's range (D4, D16); both shifts check the count (D16).
  Note the clang lesson in CLAUDE.md, and that a left shift of a
  negative value is undefined C (`rt.h`'s comment).
- A fault's name as D17 says.
- Unit tests for what a golden test can't see (D7), if anything new.
- Leave out: `bit/not`, a count masked rather than checked, unsigned
  anything. Report, don't add.


Both trials' branches are kept: `step3-sonnet` and `step3-haiku`,
which is what main took. The record is in `docs/MODELS.md`. Open, from
Haiku's run: the compiler emits one nested C expression per program, so
a user's program about 250 operators deep fails under clang's bracket
limit. A decision when a program that deep is wanted: statements with
temporaries, or `-fbracket-depth`, or a documented limit.

### 4. Exponentiation (done)

Referee: `t/referee/calc.py`, extended with the builders' D19 once
they'd stated it, since the decision was theirs to propose.

Size: large, for the model. D18 (and D19, which the build had to add:
D18 gave only the operator). The model first, `t/models/pow.py`
and its tests, 040 and up, then the code; done when `make test`,
`make golden-clang` and `make sanitize` pass, the model lists what it
writes, and `LANGUAGE.md`, this heading and `CLAUDE.md`'s Status are
moved.

What landed: `t/models/pow.py` and tests 040 to 045, committed red, then
`rt_pow` (squaring, so an exponent of 2^62 - 1 on a base of 1 is quick)
and the table entry. The model's one shortcut, overflow without computing
when |a| >= 2 and b >= 63, is asserted against the real power up to 200.

Both trials' branches are kept: `step4-sonnet`, which is what main
took, and `step4-haiku`. The record is in `docs/MODELS.md`. D19 is a
default the builder wrote; it waits on the person.

`t/referee/calc.py` was recursive and failed past about 1,000 levels;
it's a loop now, 100,000 deep, and `PROCESS.md` says a referee is
written as one.

### 5. A budget: `(within n expr)` (done)

Referee: `t/referee/calc.py`, extended with the proposal, before any
build. Wanted because the semantics are the language's own, with no
textbook answer to check by eye, and with traps a mirror of the runtime
would copy: the budget's edge (n operations run, the n+1th faults), the
charge before or after the operands and before or after the checks, an
inner budget escaping the outer, and C's argument order, which gcc and
clang already disagree on (D25). It agrees with the 26 tests before
this step and with the 20 below, and, while proposing, with a
prototype of D26 and D27 (kept out of the repo) on 1,200 random
programs under gcc and clang.

Size: medium. D20 is the person's and D21 to D27 decide the rest,
including the shape of the C and of the runtime's counter; every test's
program and expected output is written below; the referee exists. No
model is written: each output is read off a program of a line or two,
and the one that takes more than a glance, 052, is worked here. What's
left is code to a stated design, under complete checks, which is
medium by `docs/MODELS.md`. The brief is `docs/BRIEF.md`; a builder
smaller than medium builds and flags, as it says.

D21 to D27 are defaults the person hasn't confirmed. If they change
any, this text and the tests change with them before the build, and
the referee is rerun over the tests. A build on them unconfirmed builds
them as written.

Landed as written: tests 050 to 069 committed red (all twenty failing
under gcc, all but 059 under clang), then the runtime's counter, the
compiler's `within` and temporaries, and the unit tests; `make test`,
`make golden-clang`, `make sanitize` and `make check` pass, with no
earlier file under `t/` changed and no decision added. Built by Sonnet
5.5 from the brief, on a step marked medium.

Done when: tests 050 to 069 are written exactly as below and committed
red before the code (every one fails to compile today, since `within`
is unknown, except 059, which fails under gcc and passes under clang:
that's D25's bug); then `make test`, `make golden-clang` and `make
sanitize` pass, with no file under `t/` changed but the twenty added
(and `make check` passes too, if `npm install` works where it's built);
and `LANGUAGE.md`, this heading, the progress line, and `CLAUDE.md`'s
Status and code style are moved.

- `within` (D24): a special form in `codegen.ts`, beside `if`: two
  parts, else the compile error `within takes 2 arguments, not N` at
  the form. It emits `(bK = rt_within(N), rt_within_end(bK, E))`
  (D26).
- The order (D25, D26): an operator whose two operands are both lists
  emits `(tI = L, tJ = R, op(tI, tJ))`; with an atom on either side,
  the plain call it emits now. The temporaries are declared at the top
  of `lang_main`, `rt_value tI` and `int64_t bK`, numbered per program
  from 0 (a count threaded through `compileExpr`, or a counter made in
  `compileProgram` and passed down; not module state, since the unit
  tests compile many programs in one process). `if` stays C's `?:`.
- The runtime (D27): `spent` and `limit` in `rt.c`, static; a `charge`
  at the top of each of the seventeen operator functions, before
  `need_ints` (and in `rt_eq` and `rt_ne`, which have no check, and
  through `RT_CHECKED` for `+`, `-` and `*`); `rt_within` and
  `rt_within_end` declared in `rt.h`. The clang lesson in `CLAUDE.md`
  holds: compute `spent + n` only after the comparison that says it
  fits.
- Golden tests 050 to 069, below. Each file is one comment line, of the
  builder's wording, naming the decisions it tests and saying the
  expected output is by hand from this step (not naming a model: a path
  under `t/models/` in a comment is a claim `make checks` holds the
  test to), then the program as given. Each expected is as given,
  ending in a newline; a fault is two lines. Every expected output was
  worked by hand from D21 to D25 and agrees with the referee.
  - 050 `within`: `(within 3 (+ (* 2 3) (- 10 4)))` gives `12`; three
    operations, a budget of three (D22).
  - 051 `within-spent`: `(within 2 (+ (* 2 3) (- 10 4)))` gives
    `fault: budget spent` / `exit: 1`; the third is refused (D22).
  - 052 `within-every-op`: the program below gives `155`: each of the
    seventeen operators once, so seventeen operations (D21). Worked:
    `(bit/shl 3 4)` 48, `(bit/shr 48 2)` 12, `(** 12 2)` 144; `(< 1 2)`
    and `(>= 3 3)` `#true`, `==` `#true`; `(<= 5 4)` `#false`, `(> 5 4)`
    `#true`, `!=` `#true`; `(bit/and 12 10)` 8, `(* 2 3)` 6, `(- 7 6)` 1,
    `(/ 17 2)` 8, `(% 8 5)` 3, `(bit/or 1 3)` 3, `(+ 8 3)` 11; `(bit/xor
    144 11)` 155. The two `0`s are branches not taken. The file holds
    the block as shown, less its indent, so `(within 17` starts the
    line.

        (within 17
          (bit/xor (** (bit/shr (bit/shl 3 4) 2) 2)
                   (if (== (< 1 2) (>= 3 3))
                       (if (!= (<= 5 4) (> 5 4))
                           (+ (bit/and 12 10) (bit/or (- 7 (* 2 3)) (% (/ 17 2) 5)))
                           0)
                       0)))

  - 053 `within-every-op-spent`: the same program with `16` for `17`
    gives `fault: budget spent` / `exit: 1`. With 052, it fails if any
    one operator isn't charged.
  - 054 `within-free`: `(within 0 (if #true (within 0 7) (/ 1 0)))`
    gives `7`: `if`, `within` and literals cost nothing, and the branch
    not taken isn't charged (D21, D24).
  - 055 `within-if`: `(within 2 (if (< 1 2) (+ 40 2) (+ (+ 1 1) (+ 1
    1))))` gives `42`: the test and the taken branch, two; the other
    branch would have been three (D21).
  - 056 `within-pow`: `(within 1 (** 1 4611686018427387903))` gives
    `1`: `**` is one operation, whatever its exponent (D21).
  - 057 `within-charge-after-operands`: `(within 1 (+ (/ 1 0) 2))`
    gives `fault: division by zero` / `exit: 1`: the division is the
    one operation the budget allows (D22).
  - 058 `within-charge-first`: `(within 0 (/ 1 0))` gives `fault:
    budget spent` / `exit: 1`: the charge comes before the operator's
    checks (D22).
  - 059 `order`: `(+ (/ 1 0) (+ #true 1))` gives `fault: division by
    zero` / `exit: 1`: the left operand first (D25). Red under gcc
    today, which says `not an integer`.
  - 060 `within-order`: `(within 1 (+ (* 2 3) (/ 1 0)))` gives
    `fault: budget spent` / `exit: 1`: the multiplication takes the
    one, so the division is refused (D22, D25).
  - 061 `within-outer-binds`: `(within 1 (within 5 (+ (+ 1 2) 3)))`
    gives `fault: budget spent` / `exit: 1` (D23).
  - 062 `within-inner-binds`: `(within 5 (within 1 (+ (+ 1 2) 3)))`
    gives `fault: budget spent` / `exit: 1` (D23).
  - 063 `within-nested`: `(within 3 (+ (within 5 (+ (+ 1 2) 3)) 4))`
    gives `10`: the inner's two operations and the outer `+` (D23).
  - 064 `within-nested-spent`: the same with `2` for the outer `3`
    gives `fault: budget spent` / `exit: 1`: the outer paid for the
    inner's two (D23).
  - 065 `within-computed`: `(within 2 (within (+ 1 1) (* 3 4)))` gives
    `12` (D24).
  - 066 `within-computed-spent`: `(within 1 (within (+ 1 1) (* 3 4)))`
    gives `fault: budget spent` / `exit: 1`: the budget's `+` is
    charged to the outer (D24).
  - 067 `within-not-int`: `(within #true 1)` gives `fault: not an
    integer` / `exit: 1` (D24).
  - 068 `within-bad-budget`: `(within -1 (/ 1 0))` gives `fault: bad
    budget` / `exit: 1`: checked before the body runs (D24).
  - 069 `within-bool`: `(within 1 (< 1 2))` gives `#true`: a
    `within`'s value is its body's, of any type (D22).
- Unit tests, in `compiler/tests/codegen.test.ts`, added beside the
  others (D7), none of the existing ones changed. With the file's own
  `fails`:

        fails('(within)', 'within takes 2 arguments, not 0', 1, 1);
        fails('(within 5)', 'within takes 2 arguments, not 1', 1, 1);
        fails('(+ 1 (within 1 2 3))', 'within takes 2 arguments, not 3', 1, 6);
        fails('within', 'unknown name within', 1, 1);
        assert.match(compileProgram(read('(+ (/ 1 0) (+ #true 1))')),
            /\((t\d+) = rt_div\(rt_int\(1LL\), rt_int\(0LL\)\), (t\d+) = rt_add\(RT_TRUE, rt_int\(1LL\)\), rt_add\(\1, \2\)\)/);
        assert.match(compileProgram(read('(within 5 (+ 1 2))')),
            /\((b\d+) = rt_within\(rt_int\(5LL\)\), rt_within_end\(\1, rt_add\(rt_int\(1LL\), rt_int\(2LL\)\)\)\)/);

- Documents: `LANGUAGE.md` gains a section on budgets after
  exponentiation (what an operation is, the edge, nesting, the budget
  as an expression, with examples from the tests above, no tables), a
  sentence under Forms that evaluation is left to right and the first
  fault ends the program (D25), and `budget spent` and `bad budget` in
  Faults. This heading gains (done) and a note of what landed
  differently, if anything; the progress line moves. `CLAUDE.md`'s
  Status gains step 5 (D20 to D27, tests 050 to 069, the builder's
  model and tier) and its **Next**; its code style's argument-order
  lesson gains D26's rule (two operands that can fault or charge are
  never two arguments of one call). `DECISIONS.md` gains an entry only
  if the build had to decide something these don't (`docs/BRIEF.md`
  says how). `DESIGN.md` isn't moved: it's still the template's
  skeleton, as through steps 1 to 4.
- Leave out: a way to catch `budget spent` or to ask what's left; a
  budget of anything but operator applications (time, memory, depth);
  which of one operator's own checks comes first (open; no test applies
  an operator that could fail two of its own checks); the
  bracket limit (open since step 3; D26 keeps it where it was, and no
  test goes deeper); a model under `t/models/`; an environment variable
  or flag for a default budget. Report, don't add, if something seems
  to need them.

### 6. [Local bindings.] Referee: [decide]. Size: medium.

### 7. [Heap values.]

### 8. [Procedures, calls and tail calls.]

### 9. [Closures.]

### 10. [Whatever the language is really about: its core rule.]

### 11. [The prelude, in the language.]

### 12. [Examples: ports of existing programs, each a golden test.]

### 13. [Tooling: the runtime cached, tests in parallel, the guide's
code checked.]

## Proposals

[Agreed proposals become steps above. Proposals not yet agreed go here,
each with its options and the agent's recommendation, marked
**proposed** until the person picks, and the pick recorded as a `Dn`.]

## Example-port table

| Example | Needs | Status |
|---|---|---|
| [name] | [the features it needs, by step] | [waits on step n / ported / dropped (Dn)] |
