# Background

## The Perl sketch

`docs/prior-art/MiniMetaModel.pl` is the guide (D9). It comes from the Pugs
project in the mid-2000s. It was one of the first properly bootstrapped
meta-models, and it led to the first Perl 6 meta-model and then to Moose
for Perl 5. Its 32 assertions pass under Test::More (`perl
MiniMetaModel.pl`).

In brief: every value is an opaque instance with an id, a class and an
attribute hash. A `Dispatchable` package sends method calls by walking
the class chain. `Class` is an instance of itself, `Object` is the root,
and a class's precedence list is its superclass chain.

What SMOL doesn't take from it, and why:

- The AUTOLOAD promotion of methods into Perl packages. It's an artifact
  of Perl's packages (D10).
- Prototypes (`($%)`, `($$)`), lvalue accessors, `goto &`, `local`,
  `lock_keys`, and the `$:` and `%:` key prefixes. The sigils move into
  the names (D9, D11). `lock_keys` is DESIGN open 10.
- `%:attributes`, which `create_class` sets and nothing reads (DESIGN
  open 9).

Gaps found by running the sketch. The golden tests shouldn't copy them:

- `isa` and `can` are routed to AUTOLOAD and die with "No method found".
  I checked both. (DESIGN open 5.)
- The comments on ids are off by one: "the fourth id" is 3. The values
  are right.
- `class_precendence_list` is misspelled. SMOL spells it `precedence`
  (default).

## Smalltalk and CLOS

From Smalltalk: everything is an object, classes are objects, and each
class is an instance of a metaclass. From CLOS: the class precedence
list, and multiple inheritance. Multiple inheritance is parked until
DESIGN open 3 is settled; single inheritance is recommended.

## Parked

- A native target, C or assembly. The calculator had one, and D8 rules out
  performance as a reason to need it.
- Regular expressions, Perl's context-dependent sigils, and Perl
  compatibility (D13).
- A bytecode VM (the alternatives in `PLAN.md`).
- A SMOL evaluator written in SMOL. It would be a proposal of its own,
  after the bootstrap works.

## The calculator

The template's calculator (`compiler/`, `runtime/`, `t/000-int`, `t/001-int-min`)
is in commit `4f6563e`, the commit this tree was made from. Its decisions
D1 to D4 are removed from `DECISIONS.md`, and D5 to D7 are kept.
