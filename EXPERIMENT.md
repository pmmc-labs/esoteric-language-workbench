# Experiment: one agent as designer and builder

The brief was `docs/briefs/design-and-build.md`. There was no person in
the run, so I designed the language, made every decision, and handed
each step to a sub-agent.

## The language

**Strata** is a small imperative language: 64-bit checked integers, byte
strings, `let`, `if`, `while`, top-level functions, `print`. It compiles
from TypeScript to C. The unusual part is that a variable is not a box,
it's a stack of everything it has ever held:

- `x <- e` lays a new value on top of `x`.
- `#x` counts the layers.
- `x@k` is `x` as it was `k` writes ago.

Every expression evaluates to such a history, and operators take the
top. So `@` does two jobs: `x@1 + 1` uses the previous value, and
`f(xs@1)` recurses on the rest of a list. There is no other container.

**Core rule (D7):** every name is a history; a write lays a new layer,
`@` reads the past, and nothing can change or remove it.

## Numbers

- **Steps:** 7 of a budget of 10 (0 to 6), all done.
- **Decisions:** 40.
  - D1 to D32 were made at design time, before any code. Three were
    attributed *(experimenter)*, because the brief fixed them.
  - D33 to D40 were *(default)*, one per step from 0 to 5 plus the
    lexer's, recorded by builders. I kept all eight at review.
- **The hard decisions:**
  - D11 and D12: an expression *is* a history; `let` names a whole
    history and `<-` lays only its top. This is what lets one value
    kind serve as both a scalar and a list.
  - D13: `@` returns a suffix, not an atom.
  - D21: I rejected strings as histories of characters. It was
    tempting, but it would have made strings containers.
- **Tests:**
  - 90 golden tests: 85 in `t/` and 5 examples. Each passes under gcc,
    clang, and clang with `-fsanitize=undefined,address`.
  - 37 unit tests.
  - 6 Python models: arith, long, and 4 for the examples. `t/checks.py`
    reruns them.
- **Examples:** fizzbuzz, factorial, sort (insertion sort by recursion
  on `@1`), reverse, and history (the core rule: Fibonacci as
  `f <- f + f@1`, undo by writing an older value, a `trend` function
  reading its argument's past, `#` as a counter).

## Per step

| Step | Builder | Tokens | Time | Flagged |
|---|---|---|---|---|
| Design | me | (main session) | | |
| 0 scaffold, lexer, `print INT` | Sonnet | 106k | 2.4 min | D33 to D35 |
| 1 numbers | Sonnet | 112k | 4.3 min | D36 |
| 2 histories (core rule) | Sonnet | 119k | 5.1 min | D37 |
| 3 control | Haiku | 156k | 6.3 min | D38 |
| 4 functions | Sonnet | 114k | 5.3 min | D39 |
| 5 strings | Sonnet | 119k | 6.4 min | D40 |
| 6 examples | Sonnet | 92k | 3.6 min | none |

What each step's builder flagged:

- **Step 0 (D33 to D35):** parse-error wording, lexer details, and the
  runtime's shape.
- **Step 1 (D36):** a chained comparison gets no special message; it
  reads `expected statement, found '<'`.
- **Step 2 (D37):** where `unknown variable` points, and that a list
  evaluates all of its elements before laying any of them.
- **Step 3 (D38):** after a block ends, its names can be declared again.
- **Step 4 (D39):** functions compile to static C functions, and the
  depth counter wraps each call. It passed 10000-deep under ASan.
- **Step 5 (D40):** builtin arity is checked at compile time, and a
  literal is copied into the arena each time it's evaluated.

Every step was green on its first build. Nothing was redone and no
sub-agent was retried. My only change to a builder's work was
cosmetic: the sanitized run's summary line said "clang" just like the
plain clang run.

Several builders added tests beyond the plan, mostly one fault per file.
Two fixed their own hand-written expectations: a miscounted column, and a
model that first had `MIN % -1` as 0. In both cases they fixed the
reasoning and reran, rather than copying the compiler's output.

Usage: the sub-agents took about 820k tokens and about 33 minutes of
wall time between them. The main session's own usage isn't visible to
me. It went mostly on the design documents and seven short reviews.

## What I'd do differently

- **Leave less to the builders.** The design pass closed most of the
  silences, but every builder still found some. Each step's defaults
  were mostly fault positions and parse-error wording. A one-paragraph
  "error positions and messages" table per form, written at design
  time, would have removed most of D33 to D40.
- **Give Haiku less.** Step 3 was the smallest step, but its builder
  spent the most tokens. On a small step, Haiku cost more than Sonnet
  on a medium one.
- **The examples found friction that I'd now design for:**
  - There's no way to read a list oldest first. Every example writes
    its own countdown or recursive `show`.
  - `return` needs an expression.
  - `print ""` is the only way to end a line.
  - Building a list from an existing history needs `let out = xs`
    before `out <- x`.

  Each of these is small. The first is the one that matters, since lists
  come out newest-first by construction.

## What I'd want a person to overrule

- **D12, `let y = x` shares `x`'s whole past.** It's consistent with the
  rule, but it means `#y` depends on how `x` was built, which surprises.
  A person might prefer that `let` lay the top only, and that a whole
  history be adopted only from a call's result or a literal.
- **D14, no shadowing at all.** Strict, and it made scoping trivial. But
  helper functions can't reuse a name from an enclosing block, which a
  person might find fussy.
- **D26, memory is never freed.** A loop counter keeps every value it
  has ever had. That's fine at this scale, but it's a ceiling a person
  should choose knowingly.
- **D21, three builtins and no character codes.** Text programs beyond
  "count and reverse" will want `ord`/`chr` and probably input (D28).
