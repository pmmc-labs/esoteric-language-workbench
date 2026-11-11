# Examples

Each example is a golden test. Its program is `NN-name.smol`, and its output is
in `NN-name.expected`, worked out by hand from `docs/LANGUAGE.md` before the
interpreter ran. The comments at the top of each program say what it shows.

| Example | Shows |
|---|---|
| `01-counter` | A class with state in its attrs, and methods that chain |
| `02-inheritance` | Override, an inherited method, `isa`, `can`, the class chain |
| `03-stack` | An Array under a class, and a stack without `pop` |
| `04-recursion` | Recursion through `self`, in Integer's method table |
| `05-inject` | Iterating without a loop: `inject` and `indexOf` on Array |
| `06-memo` | A memo table in a Hash, with keys from `toString()` |
| `07-strings` | Padding by recursion, and code points in `size()` |
| `08-faults` | `fault` with a message and a value, and `catch` |

The gaps the examples found, and the ones they stepped around, are in
`docs/ISSUES.md`.
