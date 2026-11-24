# Golden tests

This replaces two sections of the workbench's `t/README.md`, the test
format and "Where expected output comes from"; the rest of that file
(determinism, the kinds of test directory) stands.

`NNN-name.pl` is a program and `NNN-name.expected` is what it must
print: stdout and stderr together, in order, plus a last line `exit: N`
when the exit status isn't 0. Numbers are never reused. Every test is
a file perl 5.42 can be given as it is.

Header lines a test may carry, as comments before the first statement
(before `use v5.42;` too):

- `# kind: same | dies | fault | refused | new`. Without one, `same`.
- `# stdin: bytes` (printf `%b` escapes), `# args: words`,
  `# env: NAME=value ...`, as in the workbench.
- `# model: t/models/name.py`, when a model wrote the test.

## The five kinds, and where each one's expected output comes from

**Never from the compiler** (D7). And for most tests, not from a
person either:

- **`same`**: from perl. The program agrees with perl 5.42 (D2), so
  `.expected` is perl's stdout, and its exit status when that isn't 0.
  `make oracle` writes it, and `t/checks.py oracle` reruns perl on
  every `make test` and fails if the file differs. perl must print
  nothing on stderr, compiling (`perl -c`) or running: a warning means
  the language should have faulted or refused (D15), and the test is
  then of another kind, or a mistake. perl is run under eight hash
  seeds, and the outputs must match (D14).
- **`dies`**: from perl. An uncaught `die`: perl's stdout, then its
  stderr, then `exit: 255` (D12).
- **`fault`**: by hand. The lines the program prints before it stops,
  then `fault: MESSAGE at FILE line N.`, then `exit: 1`. The check
  requires perl to compile the file, runs the compiled program, and
  requires its stdout to be the start of perl's stdout for the same
  file (D12): the language stopped early, and said nothing perl
  wouldn't have. The program must end under perl, within the time
  allowed.
- **`refused`**: by hand. The compiler's message,
  `FILE:LINE:COL: message`, then `exit: 1`. The test passes when the
  program does not compile and says exactly that. perl isn't asked.
- **`new`**: a feature perl doesn't have. Its decision names the model
  or the referee that writes the output.

A model in `models/` is for edges: it writes a test program over the
values that find them, and the expected output from the definition
(Python's integers, `fractions`, `float`). The oracle check then holds
perl to the same answer. When the two disagree, neither file is
patched: the disagreement is a finding about a decision, and is
reported.

## What a `same` test may not do

Depend on anything D14 lists: hash order (sort the keys), a
reference's address, the real time, an unseeded `rand`, the process
id, the text of a system error. The seeds catch most of the first, and
the check also reads the file and rejects `keys`, `values` or a hash
in a list printed without `sort`, since a small hash can come out the
same under every seed tried. The rest are the author's to keep out,
and a test that fails on Stevan's machine and not the cloud's has
usually found one. Nor, until steps 8 and 15 say how, may it go 100
calls deep or call `warn`: perl writes to stderr for both.

## The census

`t/census/` (from step 11, D11) is not golden tests. It is other
people's programs, written to find wrong answers in implementations of
Perl 5, each with perl's output. `make census` gives each a verdict:
SAME, REFUSED, LOUD or WRONG. The counts are a file; WRONG must be 0
and SAME may not fall. A WRONG is fixed before anything else, and
leaves a golden test behind.
