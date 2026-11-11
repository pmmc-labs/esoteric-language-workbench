# Plan

SMOL's build order. The proposal is agreed: the implementation is an
interpreter (D14), and the open questions are settled (D15 to D22). Each
step says what it adds, what it tests, and what it leaves out on purpose.
Each carries a Referee line and a Size line, as `docs/PROCESS.md` asks.

**Progress:** steps 0 to 9 are done. Step 5 is complete (5a, 5b and 5c, D24). Step 7 gives integers and strings their classes (D36, D37). Step 8, the examples, found the gaps in `docs/ISSUES.md`. Step 9 answers every one of them (D38 to D43), and no entry is open.

## Step 0 was built by a small-tier builder

Step 0 was marked large, and this session's builder is a small-tier model.
`docs/MODELS.md` says a small model shouldn't decide anything, and that it
builds what a pattern and a check already settle. The process asks for a
larger model to write or split a large step first. The person accepted a
small builder for step 0 instead, and the commit that landed it records the
mismatch. Step 0 had no pattern to repeat, so the golden tests and the unit
tests were the check to satisfy. The steps after it are sized against those
tests.

## Decided: an interpreter, not a compiler (D14)

The interpreter is a tree-walking one in TypeScript, run by Node, with the
lexer, parser and evaluator as pure functions over immutable data.

- The subject is runtime structure: instances, method tables that change,
  closures, a class chain. A compiler to C has to build a heap, a garbage
  collector, closure environments and a value encoding before the first
  bootstrap test can pass. That is most of the work and none of the
  subject.
- Performance is out of scope (D8), so a compiler's main payoff is zero.
- Node already provides a collector and closures, so the bootstrap runs on
  a real object model without the plumbing.
- The process still fits. Ghuloum's rule holds: step 0 runs end to end
  (read, parse, evaluate, print), and each step adds one feature with its
  golden tests.

Costs:

- `t/run.sh` changes shape. It runs the interpreter on each `.smol` file,
  instead of compiling and running a binary. The rest of the golden format
  stays: stdout and stderr together, `exit: N`, the watchdog.
- The bootstrap sits on JavaScript's object model. A bootstrap all the way
  down would be a later step: a SMOL evaluator written in SMOL. That is a
  separate proposal, and the more interesting one.

Rejected: a bytecode VM (an instruction set, an assembler, frames and a
dispatch loop, all to design, none of it the subject); compiling to
JavaScript (no gain over the interpreter except an output file); compiling
to C (the calculator's route, with every cost above several times over).

## Steps

### 0. Scaffold: reader, evaluator, runner (done)

- Landed: `bin/smol.ts`; `compiler/src/` with `ast.ts`, `lexer.ts`,
  `parser.ts`, `eval.ts` and `errors.ts`; `t/run.sh`, which runs the
  interpreter; unit tests in `compiler/tests/`; golden tests 000 to 011.
- Differs from the plan as first written:
  - Comments are `//`. `;` separates statements (DESIGN, default), so it
    can't also begin a comment.
  - Golden tests 000 and 001 are kept, with the same programs. 002 to 011
    are added. The plan's "a let with a call" is `002-let`: no call can
    succeed before step 1, so calls and method calls are tested by their
    faults (007 and 008).
  - Integers are unbounded, not 63-bit. 011 checks that one more than 2^62
    is exact.
  - The calculator's C runtime, its compiler passes, and the compile step in
    `t/run.sh` are gone (D14).
- Tests: the golden tests above, by hand; the unit tests in
  `compiler/tests/`.
- Leaves out: closures, objects, catchable faults.
- Size: large, as written; built by a small-tier builder, as above.
  Referee: none.

### 1. Closures (done)

- Landed: function literals and calls, lexical capture, the arity check,
  and a body's value. Golden tests 012 to 021, and unit tests in the parser
  and the evaluator.
- Differs from the plan as first written:
  - `%name` waits for step 3. It collects the rest of the arguments into a
    Hash, and Hash doesn't exist yet (LANGUAGE.md).
  - `self` is an ordinary parameter for now. Its binding as the receiver
    comes with dispatch in step 4 (D15).
  - A function can't call itself by name, since a let binds after its value
    is computed (DESIGN, default). Recursion goes through methods, in step 4.
- Leaves out: anything that catches a fault.
- Size: medium, built by the same small-tier builder, with the defaults
  listed in DESIGN.md. Referee: none.

### 2. Catchable faults (done)

- Landed: the built-in `catch(closure)` (D17), bound in the starting
  environment. It calls the closure with no arguments, and returns the
  fault's message as a string, or `nil`. Golden tests 022 to 029, and unit
  tests in the evaluator.
- Differs from the plan as first written:
  - The sketch's `fails_ok` matches a regular expression. SMOL has none
    (D13), so the tests compare the whole message. Step 4's message for a
    missing method is the one that has to be compared, and it is `no method
    found for NAME on VALUE`, the wording of step 0's fault.
  - A fault in `catch`'s own argument, such as a value that isn't a function,
    is not caught (DESIGN, default). Only a fault in the call it makes is.
- Leaves out: anything that returns a fault as a value other than its message.
- Size: medium, built by the same small-tier builder. Referee: none.

### 3. Scalar, Hash and Array (done)

- Landed: Array and Hash values, which are references and change in place;
  the classes `Array` and `Hash`, with `new`; the methods push, get, set and
  size on Array, and get, set, keys and size on Hash; and the trailing
  `%name` parameter that step 1 deferred, since it collects into a Hash.
  Golden tests 030 to 049, and unit tests in the parser and the evaluator.
- Scalar is the values integers, strings, `nil` and the booleans, each bound
  to a name (D20). They have no methods yet, so `42.size()` is still a fault.
- Differs from the plan as first written:
  - The plan said the built-in methods dispatch "like any other method", but
    dispatch is step 4, which comes after this step. So each kind of value
    has a host table of methods, which a method call consults (DESIGN,
    default). Step 4 replaces the tables with class method tables (D10,
    D16), and step 5 makes `Array` and `Hash` SMOL classes that hold the same
    methods. This was a gap in the plan, and it is recorded here.
  - The plan didn't say arrays and hashes are references. A `let` copies the
    reference (default; golden test 040).
- Leaves out: objects.
- Size: medium as written, built by the same small-tier builder, as the
  person accepted for step 0. Referee: none.

**Step 4 needed a size check.** Step 4 is marked large, and the builder of
steps 0 to 3 was small-tier. The process says to stop before building a
large step with a small builder, and to ask. So step 4 waited, and was
built by a large-tier builder, to decisions the lead had made for the
points the plan left open.

### 4. Opaque instances and dispatch (done)

- Landed: the five built-ins from D10, `create_opaque_instance`,
  `opaque_instance_id`, `opaque_instance_class`, `opaque_instance_attrs`
  and `create_class`, as plain names in the starting environment; the
  instance value, shown as `<object ID>`; a method call on an instance,
  which looks through the single class chain (D16) and passes the receiver
  as `self` (D15); ids from one counter, from 1 for each run. Golden tests
  050 to 083, and unit tests in the evaluator.
- Differs from the plan as first written:
  - The host tables of step 3 stay. The plan said this step "replaces the
    host tables from step 3 with class method tables". A class method table
    is a Hash in the attrs of a class that is an instance, and `Array` and
    `Hash` aren't instances until step 5 makes them SMOL classes. Moving
    their methods now would mean building those classes on the host, and
    then again in SMOL. So arrays, hashes and the class values `Array` and
    `Hash` dispatch as in step 3, and take no ids. Step 5 replaces the
    tables.
  - The fault for a missing method is `no method found for NAME on VALUE`,
    the wording of step 0 that the notes on step 2 fixed, and not the
    plan's `No method found for NAME`.
  - `attrs` is one Hash value. The sketch takes flat arguments; a Hash
    lets step 5 write `function ($class, %attrs) {
    create_opaque_instance($class, %attrs) }`. The instance holds that Hash
    by reference, where the sketch copies.
  - `create_class` gave its instance the class `nil`, where the sketch gives
    `Class`. Step 5 settled it: the prelude's `create_class` gives instances of
    `Class` (D26), and the built-in under it still gives `nil`.
  - `create_class`'s defaults are `"$name"`, `"$superclass"` and
    `"%methods"`, by D21's keys and without `%:attributes` (D22).
  - A method's arity counts only the arguments after `self`, and a function
    with no parameter for `self` is a fault when called as a method. The
    plan didn't say.
  - The tests go past the plan's four: the receiver as `self`, a method
    that calls another through `self`, a class's method not reachable from
    its own instances and the reverse (the sketch's two `fails_ok` cases,
    with a hand-made metaclass), attrs by reference, `create_class`, and
    the faults.
- Leaves out: `Class` and `Object`, `opaque_instance_set_class` and any
  prelude, which are step 5; `isa` and `can`, which are step 6.
- Size: large (this is the core rule), built by a large-tier builder.
  Referee: none. Decide before step 5, where the model of the definition
  is written.

### 5. The bootstrap: Class and Object, in SMOL (split, D24)

**5a, done.** The prelude in `lib/prelude.smol` runs before every program. It
makes `Class` (object 1) and `Object` (object 2), with `name`, `superclass`
and `get_method` on Class, and `new`, `id` and `class` on Object, plus the
setter `opaque_instance_set_class` (D19). The prelude binds `Class` and `Object`, and 5c added the Boolean classes. Golden tests 085 to 093 take the
sketch's assertions, each with its expected value from the sketch's own `is`
and `is_deeply` lines, except the four about `class_precedence_list`, which 095 takes. The
programs' own objects started at 3 (D25), which D28 moves to 7, and D32 to 100.

**5b, done (D31, D32, D33).** The prelude makes `Array` (7) and `Hash` (8), with
the host's methods in their `"%methods"`, taken by `host_method` (D33), and
registers them as the classes of arrays and hashes (D31). It then calls
`reserve_ids(100)`, so a program's own objects start at 100 (D32). The host
method tables and the host class value are gone, and `Array` prints as
`<object 7>`. Golden tests 099 to 109, and the user ids in 046 to 098 moved by
93, each re-derived by hand; 093 is renamed `093-own-ids-start-at-100`. Differs
from the proposal:

- `new` is a method of the class, and the core rule looks for `Array.new` in
  `Array`'s class. So each of `Array` and `Hash` has a metaclass, `"Array
  class"` and `"Hash class"` (9 and 10), under `Class`, which holds `new`
  (DESIGN, default). The bootstrap has ten objects, not eight; the ids they
  take are reserved, so a program's numbers don't move.
- The prelude needs hashes before `Hash` exists, and `class_precedence_list`
  needs `Array.new()` before `Array` exists. Both are worked around in the
  prelude, with no new builtin (DESIGN, default).
- `opaque_instance_class` answers a primitive's registered class, so
  `true.class()` is `True` too.

The proposal below is the record; the numbers in it are superseded by D32. `Array` and `Hash` as SMOL classes, with their
methods in class method tables. A method call on a host value finds no class
today, which is why the host tables exist. Proposed: a registry from a value to
its class, set by a builtin, `set_primitive_class(sample, class)`, where the
sample picks the entry: its kind, or for `true`, `false` and `nil`, the value
itself. A method call on a value with a registered class walks that class's
chain, as for an instance (D10). Array and Hash register their classes in the
prelude, and their methods become builtins in `"%methods"`. Builtins take any
number of arguments, so `Array.new(a, b, ...)` and `push(x, ...)` can be
builtins. The same registry gives Boolean and nil their classes for 5c.
Rejected: keeping the host tables and pointing the class at them, which is two
dispatch routes; and a class field on every array and hash value, which keeps
the class in two places. Cost: two more bootstrap objects, so user ids move again (D28 records the numbering). Golden tests 030 to 049 do not change, since their outputs don't.

**5c, done.** Conditionals are methods of booleans, with a Boolean class (D27).
Option A (D28): `Boolean`, `True`, `False` and `UndefinedObject`, the last for
`nil`. `class_precedence_list` stops where the superclass is `nil`, by asking it
`isNil()`, and branches with a boolean's method. Golden tests 095 to 097 take
the sketch's cpl assertions, the conditionals and the untaken branch. The
registry that gives the three constants their classes is D29.

- Adds: `Class` and `Object` as SMOL source, with `new`, `name`,
  `superclass`, `class_precedence_list`, `get_method`, `id` and `class`,
  and the setter `opaque_instance_set_class` (D19), which makes `Class` an
  instance of itself.
- Also adds, moved here from step 4: `Array` and `Hash` as SMOL classes,
  with their methods in class method tables in place of the host tables of
  step 3. Step 4 left the tables, since a class method table needs a class
  that is an instance (the note under step 4).
- Method tables and attributes use the keys D21 gives (`"%methods"`,
  `"$name"`). `%:attributes` and `lock_keys` are gone (D22).
- Tests: the sketch's 32 assertions, as a few golden tests. Their expected
  values are the values in the sketch's own `is` and `is_deeply` lines. The
  sketch's comments on ids are off by one, so the tests use the values and
  not the comments.
- Also tested: an instance can't call a method that only its class has
  (the sketch's "metaclass calling instance method fails", and its reverse).
  That is the meta-model working.
- Size: large (the bootstrap is the subject, and the expected values need a
  model's reading of the definition). Referee: none. The sketch's
  assertions are the independent source.

### 6. isa and can (done)

- Landed: `isa(cls)` and `can(name)` as built-in methods on `Object` (D18),
  host builtins reached through `host_method` (D35). Golden tests 110 to 115,
  and unit tests in the evaluator.
- Differs from the plan as first written: the methods are host builtins, not
  SMOL, because `isa` needs a walk of the chain and SMOL has no loop (D35).
- Size: small, built by the lead. Referee: none.

### 7. Primitive classes for integers and strings (done)

- Landed: `Integer` and `String`, made by the prelude after `Array` and `Hash`,
  with their methods as host builtins in their `"%methods"` (D36). Integers and
  strings register by kind, so `set_primitive_class` gives them a class as it
  does arrays and hashes (D31), and a program may reassign it (D37). Golden
  tests 116 to 131, and unit tests in the evaluator.
- Golden tests 008, 096, 107 and 111 assumed an integer has no class. Their
  programs or comments changed where they did, and their expected output was
  worked out again by hand.
- Differs from the plan as first written: the plan didn't name the methods.
  D36 names them, as defaults for review. Functions still have no class.
- Leaves out: operators and division (ISSUES.md), string indexing, and string
  escapes.
- Size: medium, as a mirror of step 3's Array methods on the registry of D29
  and D31. Built by the lead, which is small-tier, so the design
  and its method list are the risk: D36 is marked default for the person to
  look at. The process has a large model write a step, and this one wasn't, so
  the mismatch is recorded in the commit. Referee: none.

### 8. Examples, and the gaps they show (done)

- Plan: write example programs in `examples/`, each with an `.expected` golden
  test, as CLAUDE.md's layout says. A larger model designs and writes them. Their
  expected output is worked out from LANGUAGE.md, not run through the
  interpreter, so a mismatch is a fact to investigate. An example that needs a
  feature the language lacks is changed or left out (D6); the gap goes to
  `docs/ISSUES.md` for a proposal.
- Landed: `examples/01-counter` to `08-faults`, each with an `.expected` worked
  out by hand from LANGUAGE.md alone, before the interpreter ran. They pass on
  the first run. `examples/README.md` indexes them. The gaps are in
  `docs/ISSUES.md`, each waiting for a proposal.
- Differs from the plan as first written: a larger model designed and
  wrote the examples, as the person allowed. It ran no SMOL, so no expected
  output came from the interpreter. The lead ran them, and fixed the doc
  passages the report found unclear.
- Size: large to design, medium to write. Referee: none.

### 9. The examples' gaps (done)

- Landed: `print(x)` (D38); `find_method` on Class, and so a super call as
  `superclass().find_method(name)(self)` (D39); `each`, `inject` and `indexOf`
  on Array (D40); `pop`, `has` and `divBy` (D41); `define` on Class, and `attr`
  and `setAttr` on Object (D42). Five gaps are decided against, with reasons
  (D43). Golden tests 132 to 151; examples 01 to 07 use the new features, and
  05 and 07 have new expected outputs; 71 unit tests.
- Changed: `t/106` asked for `pop` as its missing host method, and `pop` exists
  now, so it asks for `shift`. This is the same kind of change as 107 and 111.
- Differs from the plan as first written: `find_method` has a helper,
  `find_method_from(label, seen)`, which carries the loop guard. It is a method
  of Class, and it is documented. Example 02 adds Puppy's `speak` with
  `define` after the `let`, since a function can't name the class it is inside.
- Size: medium, built by a low-effort builder to the lead's answers in D38 to
  D43. The lead re-derived the new expected outputs by hand and read the diff.
  Referee: none.

## Example-port table

| Example | Needs | Status |
|---|---|---|
| `docs/prior-art/MiniMetaModel.pl` (the sketch) | steps 0 to 6 | ported: its assertions are golden tests 085 to 097, and its `isa` and `can` stubs are built (D18, D35) |
