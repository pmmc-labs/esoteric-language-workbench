# Plan

SMOL's build order. **Nothing here is agreed.** It's a proposal: step 0
waits on the implementation pick and the open questions in
[`DESIGN.md`](DESIGN.md).

**Progress:** no SMOL step is built. The calculator's step 0 is still in
the tree, from the template, and goes when the implementation is picked.

**Sizes are a draft.** This was written by a small-tier model (Haiku 5.5).
`docs/MODELS.md` says proposals are large-tier work, so a larger model
should confirm this proposal and the Size lines before the person picks.

## Proposal: an interpreter, not a compiler

Recommended: a tree-walking interpreter in TypeScript, run by Node. The
reader, parser and evaluator are pure functions over immutable data, in
the workbench's style.

- The subject is runtime structure: instances, method tables that
  change, closures, a class chain. A compiler to C has to build a heap, a
  garbage collector, closure environments and a value encoding before the
  first bootstrap test can pass. That is most of the work and none of the
  subject.
- Performance is out of scope (D8), so a compiler's main payoff is zero.
- Node already provides a collector and closures, so the bootstrap runs
  on a real object model without the plumbing.
- The process still fits. Ghuloum's rule holds: step 0 runs end to end
  (read, parse, evaluate, print), and each step adds one feature with its
  golden tests.

Costs:

- `t/run.sh` changes shape. It runs the interpreter on each `.smol` file,
  instead of compiling and running a binary. The rest of the golden
  format stays: stdout and stderr together, `exit: N`, the watchdog.
- The bootstrap sits on JavaScript's object model. A bootstrap all the way
  down would be a later step: a SMOL evaluator written in SMOL. That is a
  separate proposal, and the more interesting one.

Alternatives:

- **Bytecode VM.** An instruction set, an assembler, frames and a dispatch
  loop, all to design. That's the work this experiment isn't about. Worth
  proposing only if the VM's own state should be modelled with the same
  objects.
- **Compile to JavaScript.** The cheapest compiler: one code-generation
  pass, with the host providing closures and the collector. It gains
  nothing over the interpreter except an output file. Keep it in mind if
  the interpreter gets slow.
- **Compile to C.** The calculator's route. Every cost above applies,
  several times over.

## Steps

Each step says what it adds, what it tests, and what it leaves out on
purpose. Each carries a Referee line and a Size line, as `docs/PROCESS.md`
asks.

### 0. Scaffold: reader, evaluator, runner (proposed)

- Adds: `bin/smol.ts`; a reader for the JavaScript-like syntax (integers,
  strings, `nil`, `true`, `false`, names with sigils, calls, method calls,
  `let`, `;` comments); an evaluator; a program prints the value of its
  last expression. A fault prints `fault: ...` on stderr and exits 1
  (default). `t/run.sh` runs the interpreter.
- Tests: golden tests 000 and 001, by hand: an integer, and a `let` with a
  call.
- Leaves out: closures, objects, catchable faults.
- Size: large (it fixes the reader and the runner). Referee: none.

### 1. Closures (proposed)

- Adds: `function (params) { ... }`, lexical capture, the trailing `%name`
  parameter, and the receiver once DESIGN open 2 is settled.
- Tests: by hand.
- Leaves out: anything that catches a fault.
- Size: medium (the design is in DESIGN.md). Referee: none.

### 2. Catchable faults (proposed)

- Adds: the `catch(closure)` built-in, or the form chosen in DESIGN open 4.
- Tests: by hand, in the shape of the sketch's `fails_ok`.
- Size: medium. Referee: none.

### 3. Scalar, Hash and Array (proposed)

- Adds: the three primitives, their built-in methods (`push`, `get`, `set`,
  `size`, `keys`, and so on), `Array.new`, `Hash.new`, and `@a.push(x)`.
  Built-in methods are host functions in the class's method table, so
  they dispatch like any other method.
- Tests: by hand.
- Leaves out: objects. These are the containers the sketch's attributes
  and method tables are built from.
- Size: medium (it repeats one pattern across three types). Referee: none.

### 4. Opaque instances and dispatch (proposed)

- Adds: the five `::` built-ins from D10; lookup through the class chain;
  `No method found for NAME` as a fault; ids from one counter.
- Tests: by hand, with a class built directly by `create_opaque_instance`:
  an instance finds its class's method, finds an inherited one, faults on
  a missing one, and gets distinct ids.
- Leaves out: `Class` and `Object`, which are step 5.
- Size: large (this is the core rule). Referee: none for now. Decide
  before step 5, where the model of the definition is written.

### 5. The bootstrap: Class and Object, in SMOL (proposed)

- Adds: `Class` and `Object` as SMOL source, with `new`, `name`,
  `superclass`, `class_precedence_list`, `get_method`, `id` and `class`,
  and the class-slot setter from DESIGN open 6.
- Tests: the sketch's 32 assertions, as a few golden tests. Their expected
  values are the values in the sketch's own `is` and `is_deeply` lines.
  The sketch's comments on ids are off by one, so the tests use the values
  and not the comments.
- Also tested: an instance can't call a method that only its class has
  (the sketch's "metaclass calling instance method fails" and its
  reverse). That is the meta-model working.
- Size: large (the bootstrap is the subject, and the expected values need
  a model's reading of the definition). Referee: none. The sketch's
  assertions are the independent source.

### 6. isa and can (proposed)

- Adds: `isa` and `can` as built-in methods on `Object` (DESIGN open 5).
- Tests: by hand. The sketch's stubs are the reason for the step.
- Size: small (the pattern is in place). Referee: none.

## Example-port table

| Example | Needs | Status |
|---|---|---|
| `docs/prior-art/MiniMetaModel.pl` (the sketch) | steps 0 to 5, and step 6 for `isa` and `can` | waits on step 5 |
