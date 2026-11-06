# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** steps 0 to 4 are done. Step 5 is proposed below: D20 from the person, D21 to D27 the defaults that complete it, a referee extended and a brief written (`docs/BRIEF.md`); it waits for the person to confirm or change D21 to D27, and for a builder.

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

### 5. A budget: `(within n expr)`

Referee: `t/referee/calc.py`, extended in this proposal with `within` and
the charge, from D20 to D27 and not from the runtime. Wanted because the
semantics have traps a mirror would copy (the edge of the budget is an
off-by-one that reads either way; the charge comes before the operator's
own fault; budgets nest by the smallest; `n` is outside its own budget),
and because the outputs are counts, which are not checkable by eye
past a few operators. The referee keeps the budget as the decisions state
it (a list of what each enclosing `within` has left, every operation
taking one from each) and the runtime as a count and a limit, so the two
are different derivations of D24. It agreed with all 22 tests below
before they were handed over, and each of eight wrong runtimes (an
operator that is not charged, an off-by-one, an inner budget that
replaces the outer, a limit not put back, a negative `n` as 0, a charge
after the operator's check, a pow that is free, an `if` that is charged)
failed at least one of them. The builder does not read it.

Size: medium. The decisions are D21 to D27, the mechanism is in D27, every
test is below with its program and its expected output, and no model is
to be written: the outputs are worked by hand from the decisions (counts
and sums a person can check) and the referee has agreed with them.
It is not small: it adds the runtime's first state, a second kind of
generated C, and a form whose body runs inside the runtime's call, and a
small builder is to build and flag (the brief says so), the checks being
complete. It would be large if D21 to D27 were not written; they are
*default*, so the person's confirmation of them comes before the build,
and a builder who finds one wrong stops there (the brief).

D20 from the person: `(within n expr)` evaluates `expr` with a budget of
`n` operations, and faults when it's spent. D21 to D27 decide what that
leaves open, and the step builds them as they stand:

- An operation is one application of any of the seventeen operators;
  `if`, `within` and atoms cost nothing (D21). A budget of `n` allows
  `n` operations, and the next faults `out of budget`; nothing catches it
  (D22). `n` is an expression, an integer, not negative (`bad budget`),
  evaluated outside its own budget (D23). Budgets nest by the smallest,
  every operation charged to each around it, and siblings don't share
  (D24). An operation is charged after its arguments run and before it
  looks at them, so `(within 0 (/ 1 0))` is `out of budget` and `(within
  1 (/ 1 0))` is `division by zero` (D25). A special form of exactly two
  parts (D26). In the runtime a count and a limit, in the generated C a
  static function per `within` (D27).
- `compiler/src/codegen.ts`: `within` beside `if`, as D26 and D27 say:
  `compileWithin` checks the number of parts (`within takes 2 arguments,
  not N`, at the form), and gives `rt_within(N, lang_within_L_C)` with
  the name from the form's line and column; the function of each `within`
  in the program, inner first, is emitted before `lang_main` by a walk
  made *after* `compileExpr` has succeeded, so that compile errors come in
  the order the program is read. The header comment lists the forms.
- `runtime/rt.c` and `rt.h`: `rt_ops`, `rt_limit`, a `charge()` that is the
  first statement of each of the seventeen operator functions (a missing
  one is a test failing: 058 and 059), and `rt_within(rt_value n,
  rt_value (*body)(void))` as D27 says. Note the clang lesson in
  CLAUDE.md: the limit is saved in a statement of its own, and
  `rt_within` calls the body in one too. Then `make golden-clang` and
  `make sanitize`.
- Unit tests, in `compiler/tests/codegen.test.ts` (D7): `(within 5)`,
  `(within)`, `(+ 1 (within 1 2 3))` give `within takes 2 arguments, not
  N` at the right position; a bare `within` is `unknown name within`; an
  error before a `within` in reading order is the one reported
  (`(+ (g) (within 1 (f)))` says `g`); and the shape of the C for a
  nested `within`: one static function each, the inner first, the call
  naming it.
- Tests, 050 to 071, all small, each program and expected output as
  written here. The expected output comes from nowhere but this text (by
  hand, from D20 to D27) and the referee, which `make checks` runs
  over them; it never comes from the compiler (D8). Each test's file is
  the program preceded by one `;` comment line naming what it checks and
  its decision (the programs below are shown without it); the
  `.expected` is the value and a newline, or the fault line and `exit:
  1`. Write the files and run them red first (they fail at compile:
  `not an operator: within`), commit, then build.

  ```
  050 within-exact           (within 4 (+ (* 6 7) (- 10 (/ 7 2))))                  -> 49
  051 within-over            (within 3 (+ (* 6 7) (- 10 (/ 7 2))))                  -> fault: out of budget
  052 within-zero            (if (within 0 #true) (within 0 7) 8)                   -> 7
  053 within-zero-op         (within 0 (+ 1 2))                                     -> fault: out of budget
  054 within-charge-first    (within 0 (/ 1 0))                                     -> fault: out of budget
  055 within-then-fault      (within 1 (/ 1 0))                                     -> fault: division by zero
  056 within-if-lazy         (within 2 (if (< 1 2) (+ 1 2) (* (* 1 2) (* 3 4))))    -> 3
  057 within-if-test         (within 0 (if (< 1 2) 1 2))                            -> fault: out of budget
  058 within-all-ops         (within 25 BIG)                                        -> 109
  059 within-all-ops-over    (within 24 BIG)                                        -> fault: out of budget
  060 within-nested          (within 5 (+ (within 2 (* 3 4)) (within 3 (- (+ 1 2) (* 3 4)))))   -> 3
  061 within-nested-outer-binds        (within 2 (within 100 (+ (+ 1 2) (+ 3 4))))  -> fault: out of budget
  062 within-nested-charges-outer      (within 3 (+ (within 100 (* 2 3)) (* 4 5)))  -> 26
  063 within-nested-charges-outer-over (within 2 (+ (within 100 (* 2 3)) (* 4 5)))  -> fault: out of budget
  064 within-n-outside       (within 2 (within (* 1 1) (+ 3 4)))                    -> 7
  065 within-n-over-outer    (within 0 (within (+ 1 1) 5))                          -> fault: out of budget
  066 within-siblings        (within 3 (+ (within 1 (+ 1 1)) (within 1 (+ 2 2))))   -> 6
  067 within-siblings-over   (within 100 (+ (within 1 (+ 1 1)) (within 1 (+ (* 2 2) 3))))  -> fault: out of budget
  068 within-negative        (within -1 5)                                          -> fault: bad budget
  069 within-not-int         (within #true 5)                                       -> fault: not an integer
  070 within-huge            (within (+ 4611686018427387902 1) (** 1 4611686018427387903))  -> 1
  071 within-args-first      (within 1 (+ (/ 1 0) 2))                               -> fault: division by zero
  ```

  `BIG` is, on three lines in the file, every one of the seventeen
  operators, `+` nine times, 25 operations (ten operators other than
  `+`, nine `+`, six comparisons):

  ```
  (if (< 1 2) (if (<= 2 2) (if (> 3 2) (if (>= 3 2) (if (== 1 1) (if (!= 1 2)
    (+ (+ (+ (+ (+ (+ (+ (+ (+ (- 10 4) (* 2 3)) (/ 9 2)) (% 9 4)) (bit/and 12 10)) (bit/or 12 10)) (bit/xor 12 10)) (bit/shl 1 4)) (bit/shr 64 2)) (** 2 5))
    0) 0) 0) 0) 0) 0)
  ```

  Its value is 6 + 6 + 4 + 1 + 8 + 14 + 6 + 16 + 16 + 32 = 109. No test
  has a call whose two arguments could each fault, or one fault and the
  other run out of budget (D25), so none depends on the order a C
  compiler picks.
- Moves: `docs/LANGUAGE.md` gains a "Budgets" section after "Exponentiation"
  (what `within` does, the edge, `n`, nesting, the charge before the
  operator's own fault, with the examples `(within 4 ...)` and `(within
  0 (/ 1 0))` from 050 and 054; no tables) and its "Faults" paragraph the
  two names, `out of budget` and `bad budget`; this heading and the
  Progress line above (done, with what landed differently, if anything);
  `CLAUDE.md`'s Status (a sentence for step 5 with its tests, D20 to
  D27, who built it and at what Size, and **Next**). `docs/DESIGN.md` is
  still the template and is left. `docs/DECISIONS.md` is not moved, except to
  add a *default* entry for anything the builder had to decide (the
  brief says what to do); D21 to D27 become *(User)* only when the
  person says so.
- Leave out: any way to catch the fault or read what is left of a
  budget; a time budget (the tests use a virtual clock and the calculator
  has no time); a budget on memory; a fixed order of evaluation of a
  call's arguments (D25); statements and temporaries in the generated C;
  `-fbracket-depth`; a cost for anything but the seventeen operators; a
  compile-time check of `n`. Report, don't add, if something seems to
  need one.

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
