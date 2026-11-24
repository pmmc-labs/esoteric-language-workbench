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
| `same-short-seeds` | Passes under every short seed, `PERL_HASH_SEED=1` to `300`; only seeds of the full width move its keys |
| `same-tie` | A real sort with a tie in it, which no reading can see |
| `same-hash-in-string` | A hash inside a string that runs code |
| `same-scalar-each` | `scalar(each %h)`, which is a key and not a count |
| `same-scalar-reverse` | `scalar reverse keys %h` |
| `same-sort-one-key` | `sort((values %h)[0])`: a sort of one value |
| `same-sort-variable` | `&$sort(keys %h)`: a variable called sort |
| `same-two-headers` | Two `# args:` lines, which `t/run.sh` and the check read differently |
| `same-env-seed` | `# env: PERL_HASH_SEED=0`, which would turn the seeds off |
| `same-limit` | A limit that isn't a whole number of seconds |
| `same-cr-header` | A `# kind:` after a carriage return, which only Python takes for a new line |
| `dies-ok` | A good `dies` test |
| `dies-wrong-message` | The wrong message in the `.expected` |
| `dies-lives` | It doesn't die |
| `fault-ok` | A good `fault` test |
| `fault-extra-line` | The program printed a line perl doesn't |
| `fault-perl-refuses` | perl can't compile it, and nothing was printed first |
| `fault-never-ends` | It never ends under perl |
| `fault-no-fault-line` | The `.expected` has no fault line |
| `fault-unsorted` | The reading rule holds for a `fault` test too |
| `fault-warns-compiling` | perl warns as it compiles: a refusal, so no fault test |
| `refused-ok` | A good `refused` test, which perl would run |
| `refused-shape` | A `.expected` that isn't one diagnostic and `exit: 1` |
| `refused-line-zero` | A diagnostic at line 0, column 0 |
| `refused-past-end` | A diagnostic at a line the file doesn't have |
| `kind-unknown` | A kind that isn't one |

When the check changes, break it on purpose and see one of these go
red; when it gains a rule, it gains a fixture that only that rule
fails. Step 0 did this for every rule the check has (stderr ignored,
one seed, short seeds, no reading rule, `perl -c` not run, and so
on), and each turned at least one fixture red.

The second half of this table came from an adversarial review: a
reader given the check and perl, and asked to get a wrong test past
it. It did, sixteen ways. What was cheap to close is closed and has
its fixture here; the rest is in `docs/TRAPS.md`, "The checks
themselves", against the step that brings the construct. Do that
again when the check grows: its author can't see what it misses.

A `.stdout` is honoured only in this directory. Beside a real test it
fails `make checks`.
