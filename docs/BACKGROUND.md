# Background

Prior art, what was borrowed and from where, and ideas parked so they
stop coming up.

## Borrowed

- **Mutable value semantics** (D7): Swift's arrays and dictionaries are
  values with copy-on-write; Hylo (formerly Val) builds a whole language
  on mutable value semantics; Go's arrays and structs are values. Ditto
  takes the semantics without the machinery: heap objects are immutable,
  and an update rebuilds the path to the variable, as a persistent data
  structure would, but by copying.
- **`else` for a missed lookup** (D20): Zig's `x catch default`,
  Swift's and C#'s `??`, Kotlin's `?:`, Perl's `//`, Python's
  `dict.get(k, d)`. Ditto's differs in catching misses (not nil) and
  in deciding what it catches lexically.
- **Syntax** (D11): Go's braces without parentheses and newline
  termination; Rust's `..` and `..=` ranges and `fn`; JavaScript's
  `let`; Python's `and or not in not in`, insertion-ordered dicts,
  interpolated strings (as `{}` without the `f`), and its recursion
  limit of 1000.
- **No truthiness** (D10): Go, Rust, Swift.
- **Checked integer arithmetic** (D14): Swift and Rust's debug builds,
  with C and Go's truncating division.
- **Expression statements must be calls** (D21): Go's "evaluated but not
  used" error.

## Parked

- **Floats.** A second numeric type, a printing format and its model.
  Add with a decimal printing rule (shortest round-trip) if programs
  need them.
- **First-class functions and closures.** With D7, closures would
  capture by value, which is simple, but they need a function value
  type and indirect calls, a step of their own. `sort` by key, `map`
  and `filter` would follow.
- **In-place updates below the outermost level, and for strings.** D48
  writes in place only through the variable itself; `g[r][c] = v` still
  copies row `r`, and `s += c` copies `s`. Owning nested levels would
  need an element to know its container is owned.
- **A collector.** Programs at D4's scale end before memory matters.
- **Static types.** A checker over this language would be ordinary
  (records as maps make it structural); the budget had no room.
- **Modules, files, command-line arguments, line-by-line input.** No
  example needed them.
