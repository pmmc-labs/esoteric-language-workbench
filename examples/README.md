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

The gaps the examples found are in `docs/ISSUES.md`, each with the decision
that answered it.
