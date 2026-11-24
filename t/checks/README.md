# The oracle check's own tests

`t/checks.py oracle` decides whether a golden test's `.expected` is
right, so everything after step 0 leans on it, and a check that passes
what it should fail looks exactly like a check with nothing to find.
Each file here is a test the check must pass, or must fail in a named
way, and `make checks` runs them all before it looks at a real test.

A fixture is a Perl file (all of Perl is allowed here: these are not
programs of the language), its `.expected`, and a header:

- `# check: ok`: the check must have nothing to say.
- `# check: fails: TEXT`: the check must fail it, and every reason it
  gives must have TEXT in it.

A `fault` fixture also has a `.stdout`: what a compiled program
printed before it stopped. The fixtures can't be compiled, so the file
stands in for the binary. (That the check can compile and run a real
test is tested apart, on `t/000-say.pl`.)

| Fixture | What it is |
|---|---|
| `same-ok` | A good `same` test, with hashes sorted every way the reading rule knows |
| `same-headers` | perl is given the test's stdin, arguments and environment |
| `same-exit` | An exit status that isn't 0, in the `.expected` |
| `same-wrong-byte` | A wrong byte in the `.expected` |
| `same-no-newline` | A missing last newline in the `.expected` |
| `same-exit-missing` | perl exits 3 and the `.expected` doesn't say so |
| `same-warns` | perl warns as it runs |
| `same-warns-compiling` | perl warns as it compiles |
| `same-died` | perl dies: a `dies` test called `same` |
| `same-perl-refuses` | perl can't compile it |
| `same-seeds` | Sorted, so it reads well, but the order is still perl's |
| `same-unsorted-keys` | One key, so the seeds agree; only reading finds it |
| `same-unsorted-values` | A `sort` in the statement, of something else |
| `same-hash-in-list` | A whole hash in a list |
| `dies-ok` | A good `dies` test |
| `dies-wrong-message` | The wrong message in the `.expected` |
| `dies-lives` | It doesn't die |
| `fault-ok` | A good `fault` test |
| `fault-extra-line` | The program printed a line perl doesn't |
| `fault-perl-refuses` | perl can't compile it, and nothing was printed first |
| `fault-never-ends` | It never ends under perl |
| `fault-no-fault-line` | The `.expected` has no fault line |
| `fault-unsorted` | The reading rule holds for a `fault` test too |
| `refused-ok` | A good `refused` test, which perl would run |
| `refused-shape` | A `.expected` that isn't one diagnostic and `exit: 1` |
| `kind-unknown` | A kind that isn't one |

When the check changes, break it on purpose and see one of these go
red; when it gains a rule, it gains a fixture that only that rule
fails. Step 0 did this fourteen ways (stderr ignored, one seed, no
reading rule, `perl -c` not run, and so on), and each turned at least
one fixture red.
