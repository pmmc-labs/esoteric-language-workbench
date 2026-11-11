# Issues

Gaps in the language that the steps and the examples have found. Under
"Examples bend to the language" (D6), a gap is recorded and the example changes,
until a proposal is picked. An open entry says what was wanted, where it showed,
and what is open. A resolved one names its decision in `docs/DECISIONS.md` and
the result. The doc passages that were unclear are at the end, and fixed.

## Open

None. The gaps the examples found are answered by D38 to D43, below.

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
