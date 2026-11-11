# Issues

Gaps in the language that the steps and the examples have found. Under
"Examples bend to the language" (D6), a gap is recorded and the example changes,
until a proposal is picked. An open entry says what was wanted, where it showed,
and what is open. A resolved one names its decision in `docs/DECISIONS.md` and
the result. The doc passages that were unclear are at the end, and fixed.

## Open

These came from examples 09 to 16, which the person has not yet answered. Each says
what was wanted, the options, and a recommendation. None is built: each needs a
decision, because most touch the language's surface or a decision already made.

- **Functions have no class, so a nil test can't see what find_method gives.**
  Example 13 can't call `isNil()` on a method that `get_method` or `find_method`
  returns, since a function has no methods. Options: (a) give functions a class,
  Function, registered by kind as Integer and String are; (b) keep it, and test
  identity with `includes`, as example 13 does. Recommendation: (a). This reopens
  D36, which left Function out for want of a method. Needs a decision.
- **Hash has no remove.** Example 15 leaves `remove` out of a set. Option:
  `remove(k)` on Hash, which gives the value removed, or nil, as `pop` does for an
  Array. Recommendation: add it. Needs a decision.
- **Array has no shift.** Example 10 keeps a head index, so dequeued items stay in
  the array. Option: `shift()`, which copies the rest. Recommendation: leave it;
  the head index is the pattern. Needs a decision.
- **Strings have no split, no character access, no substring, and no string to
  integer.** Examples 11 and 16 wanted `split` and a number from a string. Options:
  add `split(sep)` and `toInteger()`; or none, with text given as arrays of words.
  Recommendation: decide when a text example needs more. Needs a decision.
- **Booleans have no `and` or `or`.** Example 15 folds with `ifTrueFalse`. Option:
  `and(block)` and `or(block)`, in the style of the conditionals, whose blocks run
  only when needed. Recommendation: add them. Needs a decision.
- **A rest parameter takes pairs only.** Example 15 wanted `setOf("red", ...)`.
  Option: a rest parameter that takes a plain list. Recommendation: leave it; an
  Array argument does the job. Needs a decision.
- **No array or hash literal.** D12 promised `[a, b]` and `{k => v}`. The build has
  only `Array.new` and `Hash.new`, as LANGUAGE.md says, and DESIGN.md still lists
  the literals. Options: build them as sugar for those two; or revise D12.
  Example 14 nests `Array.new` calls. Needs a decision.
- **No remainder.** Example 12 tests evenness as `x.equals(x.divBy(2).times(2))`.
  D41 left remainder out, since no example asked. Option: `remainder(n)`, which
  matches `divBy`. Recommendation: add it, since parity tests are common. Needs a
  decision.
- **No map or filter on Array.** Example 12 writes them by hand with `each` and
  `push`. Option: prelude methods in SMOL, built on `inject`, as `define` is.
  Recommendation: add them, with no new builtin. Needs a decision.
- **A recursive method is added to every instance of its class.** Example 09's
  `sumList` is on Hash and UndefinedObject, since a function can't name itself
  (D43). A note, not a proposal: it comes back with the question of a recursive
  `let`.

## Resolved

- **Only the last value is printed.** D38: `print(x)` writes a line and gives
  `x`; the last value is still printed, after it. Example 07 prints its rows.
- **No super call.** D39: `find_method(label)` on Class walks the chain, and a
  super call is `C.superclass().find_method(name)(self)`. Example 02 uses it.
- **No iteration on Array.** D40: `each`, `inject` and `indexOf` are host
  builtins on Array. Example 05 uses them.
- **Division.** D41: `divBy(n)` truncates toward zero, and zero is the fault
  `divBy by zero`. There is no remainder.
- **No `pop` or remove on Array.** D41: `pop()` removes the last item and gives
  it, or nil. Example 03 uses it, and its `top` index is gone.
- **No "has key" on Hash.** D41: `has(k)` is true for a key that is there, even
  with nil under it. Example 06 uses it.
- **Verbose attributes.** D42: `attr(name)` and `setAttr(name, value)` on
  Object, in the prelude. Example 01 uses them.
- **Verbose addition of a method to an existing class.** D42: `define(name,
  fn)` on Class, in the prelude. Examples 02, 04 and 05 use it.
- **Operators.** D43: decided against. Arithmetic stays `1.plus(2)`; revisit if
  an example needs them.
- **A function can't call itself by name.** D43: decided against. Methods
  recurse through `self`, and example 07 passes the function to itself.
- **No newline or escape in strings.** D43: decided against. `print` gives the
  line breaks.
- **No grouping.** D43: decided against. `(1).plus(2)` stays a syntax error; a
  literal receiver needs no parentheses.
- **create_class's default superclass is nil.** D43: decided against. The
  default stays nil, and a class sets `"$superclass", Object`.

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
- The five built-in functions were listed together with `fault`, which is not
  one of them. The five are named, and `fault` is its own built-in.
- The message of `fault` showed a string value without saying how. It now says
  a string is in quotes, as Output shows it.
- The sentence on a value with no class was hard to follow. It is reworded.
