# Examples

Each example is a golden test. Its program is `NN-name.smol`, and its output is
in `NN-name.expected`, worked out by hand from `docs/LANGUAGE.md` before the
interpreter ran. The comments at the top of each program say what it shows.

| Example | Shows |
|---|---|
| `01-counter` | A class with state in its attrs, `attr` and `setAttr`, and methods that chain |
| `02-inheritance` | Override, a super call with `find_method`, `isa`, `can`, the class chain |
| `03-stack` | An Array under a class: a stack on `push` and `pop` |
| `04-recursion` | Recursion through `self`, in methods added to Integer with `define` |
| `05-inject` | Iterating without a loop: `each`, `inject` and `indexOf` on Array |
| `06-memo` | A memo table in a Hash, with keys from `toString()` and `has` |
| `07-strings` | Padding by recursion, code points in `size()`, and rows written with `print` |
| `08-faults` | `fault` with a message and a value, and `catch` |
| `09-linked-list` | A list of Hash nodes, with nil as the empty list |
| `10-queue` | A FIFO queue with a head index, and a round-robin scheduler |
| `11-rpn` | A dispatch table of functions, for an RPN calculator |
| `12-higher-order` | `map`, `filter`, `compose` and an adder, with `each` and `inject` |
| `13-introspection` | Classes made at run time: method names, owners, redefinition |
| `14-transfers` | Transfers under `catch`, where a failed one changes nothing |
| `15-set` | A set on a Hash: union, intersection, minus, subset |
| `16-words` | Word counts, the longest word, and a greedy wrap to a width |

The gaps the examples found are in `docs/ISSUES.md`, each with the decision
that answered it.
