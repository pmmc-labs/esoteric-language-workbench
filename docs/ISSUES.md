# Issues

Gaps in the language that the steps and the examples have found. Each is a
candidate for a proposal, and none is built. Under "Examples bend to the
language" (D6), a gap is recorded and the example changes, until the person
picks a proposal. Each entry says what was wanted, where it showed, and what is
open. The doc passages that were unclear are at the end, and fixed.

## Open

- **Operators.** `1 + 2` is not SMOL, so arithmetic is `1.plus(2)`. Left out of
  step 7 on purpose. Open: whether operators are wanted, and if so, whether they
  are method sugar or grammar. Not proposed.
- **Division.** There is no `divBy`, so no integer quotient or remainder. Left
  out of step 7 on purpose. Open: the rounding of a negative quotient, and what a
  zero divisor does. Not proposed.
- **Only the last value is printed.** Examples 01 to 08 gather their results into
  one array at the end, because a program prints one value and there is no print
  builtin. Open: a print builtin, or the rule stays. Needs a proposal.
- **No super call.** Example 02 fetches Dog's `speak` with
  `Dog.get_method("speak")` and calls it with `self`. That works only because Dog
  defines `speak` itself: `get_method` reads one class's own table, so an
  inherited method would come back as nil. Open: a `super` form (grammar), a
  builtin that calls the method above the receiver's class, or `get_method`
  walking the chain. Needs a proposal.
- **No iteration on Array.** There is no `each`, `map` or `inject`, and no loop.
  Example 05 writes `inject` and `indexOf` as methods of Array's table, recursing
  over an index. Open: library methods in the prelude, written in SMOL (no new
  builtin), or a host builtin that calls a closure. The first needs no change to
  the language. Needs a choice.
- **A function can't call itself by name.** A `let` binds after its value is made
  (DESIGN, default). Example 07 passes the function to itself as `me`. Methods
  recurse through `self` (examples 04 and 05). Open: a recursive `let`, or keep
  it. Needs a proposal.
- **No newline or escape in strings.** A string has no `\n`, so text can't span
  lines, and example 07 returns an array of rows. Open: escapes, tied to the
  print question above. Needs a proposal.
- **No `pop` or remove on Array.** Example 03 keeps its own `top` index. Open:
  `pop` as a host builtin. Nice to have.
- **No "has key" on Hash.** `get` gives nil for a missing key, and a key stored
  with nil looks the same. Example 06 uses `isNil()`, which is right only because
  it never stores nil. Open: `has(k)`. Nice to have.
- **Verbose attributes.** Each method reads and writes state through
  `opaque_instance_attrs(self).get("count")`. Open: an accessor, such as
  `attr(name)` on Object. Nice to have; a library choice.
- **Verbose addition of a method to an existing class.** Examples 04 and 05 use
  `opaque_instance_attrs(Integer).get("%methods").set(...)`. Open: a
  `define(name, function)` on Class. Nice to have; a library choice.
- **No grouping.** `(1).plus(2)` is a syntax error. The examples name the
  intermediate values with `let`. Open: whether parentheses are wanted. Nice to
  have.
- **create_class's default superclass is nil.** A class made without
  `"$superclass"` has none of Object's methods, so `class()` or `isa` on its
  instances is a fault. Every example sets `"$superclass", Object`. Open: whether
  the default should be Object. Needs a choice.

## Unclear in LANGUAGE.md, now fixed

- The value of a conditional was not stated. Bootstrap now says it is the value
  of the block it runs, or `nil`.
- Receivers were not defined. Expressions now says what may be one, and that
  grouping by parentheses is not in the language.
- The built-in functions were counted as five, then as six. The count now
  matches the list.
- A value with no class was said to answer false to `isa` and `can`, which is
  reachable only through `host_method`. Bootstrap now says so.
- A printed string needs no escaping, since no string can contain a `"`. Output
  now says so.
- DESIGN.md's truthiness and its host_method fault were stale. Both are fixed.
