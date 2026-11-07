# Experiment: one agent as designer and builder

The brief (`docs/briefs/design-and-build.md`): design a practical language
alone, decide everything, have it built step by step by sub-agents, and
report.

## The language

**Ditto** is a small, dynamically typed, imperative language with braces
and newlines (Go's shape), `let`, `fn`, `if`/`while`/`for ... in`,
Python's `and or not in`, `{expr}` string interpolation, checked 64-bit
ints, strings, lists, and insertion-ordered maps that double as records
(`r.f` is `r["f"]`). It has no truthiness, no floats, no first-class
functions, no globals visible in functions, and every fault reports
`path:line:col`. The compiler is 1,500 lines of TypeScript, emitting
C11; the runtime is 1,000 lines of C.

- **Every value is a value (D7, the core rule).** Assigning, passing or
  storing a list or map gives the receiver its own value; nothing you
  hold changes behind your back. It earns its place in the ledger
  example: a batch of transfers is applied to the function's own copy
  and simply dropped on failure, which in TypeScript needs a deep clone
  nobody remembers. It also buys loops over snapshots, structural `==`,
  and no cycles. D48 makes it cheap: a value held by one variable alone
  is updated in place.
- **`a else b` (D20).** It gives `b` when a lookup written in `a` misses:
  an index out of range, a missing key, or `int` of a non-number. What it
  catches is decided by where the code is written, so it compiles to
  branches. It earns its place in `counts[w] else 0`,
  `roads[here] else []` and `int(s) else 0`. Without it, each needs an
  `if ... in` and a second lookup.

## Numbers

- **Steps:** 10 of 10.
  - 0 to 8 as planned.
  - 9 was the reserve, spent on in-place updates (D48).
- **Decisions:** 48.
  - D1 to D33 by the designer, up front.
  - D34 to D44, D46 and D47 were builders' defaults. All were kept at
    review.
  - D45 (caching the runtime) and D48 were made at review.
- **Hard decisions:**
  - D7: how to get value semantics without copying on every assignment.
  - D20: what `else` catches, and its precedence. It binds tighter than
    `+`, so `counts[w] else 0 + 1` means what it's meant to.
  - D48: proving that an owner pointer can't leak.
- **Tests:**
  - 572 golden tests: 566 in `t/` and the 6 examples.
  - 174 unit tests.
  - Every golden test passes under gcc, clang, and clang with
    `-fsanitize=undefined,address`.
- **Models:** 9, in `t/models/`: ints, loops, functions, strings, lists,
  maps, fallback, examples and inplace. Every one is rerun by
  `t/checks.py`.
- **Examples:** 6, in `examples/`, from 12 to 42 lines each:
  - FizzBuzz
  - recursion
  - sorting
  - word count, reading standard input
  - route finding by breadth-first search
  - all-or-nothing ledger
- **Commits:** 32.

## Per step

Steps 0 to 8 were built by Sonnet sub-agents, one at a time, in the
foreground. Step 9 was built by the designer.

| Step | Builder | Tokens | Time | Flagged | Redone |
|---|---|---|---|---|---|
| 0 scaffold, lexer | Sonnet | 148k | 6.7 min | D34 to D37: trailing commas in calls, lexer gaps, parser error sites, `-Werror` | none |
| 1 int, bool, nil expressions | Sonnet | 149k | 5.3 min | D38: evaluation and check order of faults | none |
| 2 variables, control flow | Sonnet | 201k | 10.4 min | D39 and D40 | none |
| 3 functions | Sonnet | 225k | 12.5 min | D41; a pragma for `-Winfinite-recursion`; worry that 1000 frames might not fit under ASan (it does) | none |
| 4 strings | Sonnet | 231k | 14.6 min | D42 | none |
| 5 lists, core rule | Sonnet | 296k | 22.0 min | D43; **a 1000-element insertion sort needs about 8 GB** | led to step 9 |
| 6 maps | Sonnet | 299k | 22.4 min | D44; `make test` was taking 6 minutes | I added D45 (runtime cache) |
| 7 `else` | Sonnet | 198k | 16.1 min | D46; fixed its own hand-written test 713 in the green commit | none |
| 8 examples | Sonnet | 108k | 6.5 min | D47; all six passed on the first run | none |
| 9 in-place updates | designer | (in mine) | | | none |

Sub-agent total: about 1.86M tokens and 1 h 56 min of agent time. My
own usage (design, reviews, step 9 and this report) isn't visible to me
as a number. It was one long session: the design documents were about
1,000 lines written in one pass, followed by a review of each step. A
review was a run of `make test` and the report; I read code only where
something looked off.

## What I'd note

- **Designing everything up front worked.**
  - Builders took narrow defaults: check order and parser error sites,
    never semantics.
  - No step was redone.
  - The six examples ran unchanged on the first compile.
  - Writing the examples before any code changed one thing. The word
    count first wanted a sort by key; printing in first-seen order with
    a max loop read better, so first-class functions stayed out.
- **The one real problem came from a builder's measurement, not from the
  examples.**
  - D7's copy-on-every-update was fine for the examples but not for
    D4's promised scale.
  - Taking the reserve step for it was the right call. Without it, "data
    in the thousands" would have been false.
- **Still awkward:**
  - There are no first-class functions. Sorting by key means building
    `[key, value]` pairs.
  - Strings grow by copying (`s += c` is O(n)).
  - `g[r][c] = v` copies row `r`.
  - Integer-only arithmetic makes averages and percentages clumsy.
  - A function that "changes" something must be called as
    `x = f(x)`. That is the point of D7, but it's the first thing a
    TypeScript programmer will trip on.
  - `make test` takes about 5 minutes. Most of that is the sanitizer
    configuration compiling 572 programs.
- **What I'd do differently:**
  - Size D4 against a measured worst case at design time. The 8 GB
    figure was knowable then.
  - Build D48's ownership into step 5 instead of retrofitting it.
  - Make a cached runtime part of step 0's plan.
- **What I'd want a person to overrule or confirm:**
  - D13: functions can't see top-level variables. This is principled,
    but constants must be passed in.
  - D14: no floats.
  - D22: no first-class functions.
  - D20's precedence for `else`. It is defensible, but a reader may
    still want parentheses.
  - D48's soundness argument is in `DESIGN.md`. It deserves a second
    pair of eyes, because a mistake there is a silent aliasing bug.
    Tests 900 to 902 do catch a disabled `dt_share`.
