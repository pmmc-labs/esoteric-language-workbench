# Plan

SMOL's build order. The proposal is agreed: the implementation is an
interpreter (D14), and the open questions are settled (D15 to D22). Each
step says what it adds, what it tests, and what it leaves out on purpose.
Each carries a Referee line and a Size line, as `docs/PROCESS.md` asks.

**Progress:** steps 0 and 1 are done. Next: step 2, catchable faults, agreed and not started.

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

### 2. Catchable faults (agreed)

- Adds: the built-in `catch(closure)` (D17), which returns the fault's
  message, or `nil`.
- Tests: by hand, in the shape of the sketch's `fails_ok`.
- Size: medium. Referee: none.

### 3. Scalar, Hash and Array (agreed)

- Adds: the three primitives (Scalar as a value bound to a name, D20), their
  built-in methods (`push`, `get`, `set`, `size`, `keys`, and so on),
  `Array.new`, `Hash.new`, and `@a.push(x)`. Built-in methods are host
  functions in the class's method table, so they dispatch like any other
  method.
- Tests: by hand.
- Leaves out: objects. These are the containers the sketch's attributes and
  method tables are built from.
- Size: medium (it repeats one pattern across three types). Referee: none.

### 4. Opaque instances and dispatch (agreed)

- Adds: the five built-ins from D10; lookup through the single class chain
  (D16); `No method found for NAME` as a fault; ids from one counter.
- Tests: by hand, with a class built directly by `create_opaque_instance`:
  an instance finds its class's method, finds an inherited one, faults on a
  missing one, and gets distinct ids.
- Leaves out: `Class` and `Object`, which are step 5.
- Size: large (this is the core rule). Referee: none for now. Decide
  before step 5, where the model of the definition is written.

### 5. The bootstrap: Class and Object, in SMOL (agreed)

- Adds: `Class` and `Object` as SMOL source, with `new`, `name`,
  `superclass`, `class_precedence_list`, `get_method`, `id` and `class`,
  and the setter `opaque_instance_set_class` (D19), which makes `Class` an
  instance of itself.
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

### 6. isa and can (agreed)

- Adds: `isa` and `can` as built-in methods on `Object` (D18).
- Tests: by hand. The sketch's stubs are the reason for the step.
- Size: small (the pattern is in place). Referee: none.

## Example-port table

| Example | Needs | Status |
|---|---|---|
| `docs/prior-art/MiniMetaModel.pl` (the sketch) | steps 1 to 5, and step 6 for `isa` and `can` | waits on step 2 |
