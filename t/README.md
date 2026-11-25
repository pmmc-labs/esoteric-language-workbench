# Golden tests

`NNN-name.pl` is a program and `NNN-name.expected` is what it must
print: stdout and stderr together, in order, plus a last line `exit: N`
when the exit status isn't 0. Numbers are never reused. Every test is
a file perl 5.42 can be given as it is. `run.sh` compiles one, runs it
with the environment every test assumes, and diffs; `checks.py oracle`
asks perl whether the `.expected` is right.

Header lines a test may carry, as comments before the first statement
(before `use v5.42;` too), each starting its line:

- `# kind: same | dies | fault | refused | new`. Without one, `same`.
- `# stdin: bytes` (printf `%b` escapes), the test's standard input;
  `# args: words`, its arguments; `# env: NAME=value ...`, its
  environment. perl is given the same three.
- `# model: t/models/name.py`, when a model wrote the test.
- `# limit: seconds`, 1 to 60, how long perl may take over the test,
  where the usual ten isn't right.

A header appears once. `# env:` may not set a variable of perl's own
(`PERL_HASH_SEED`, `PERL5OPT`), `PATH`, or the loader's: the test's
environment is perl's too when the check runs it.

A test that writes files writes under `build/t/`.

## The five kinds, and where each one's expected output comes from

**Never from the compiler** (D7). And for most tests, not from a
person either:

- **`same`**: from perl. The program agrees with perl 5.42 (D2), so
  `.expected` is perl's stdout, and its exit status when that isn't 0.
  `make oracle` writes it, and `t/checks.py oracle` reruns perl on
  every `make test` and fails if the file differs. perl must print
  nothing on stderr, compiling (`perl -c`, which says `FILE syntax OK`
  there and may say nothing else) or running: a warning means the
  language should have faulted or refused (D15), and the test is then
  of another kind, or a mistake. perl is run under eight hash seeds,
  and the outputs must match (D14). The seeds are 64 hex digits each:
  `PERL_HASH_SEED=1` to `8` set one byte of perl's seed and leave the
  keys of a small hash in the same buckets every time.
- **`dies`**: from perl. An uncaught `die`: perl's stdout, then its
  stderr, then `exit: 255` (D12).
- **`fault`**: by hand. The lines the program prints before it stops,
  then `fault: MESSAGE at FILE line N.`, then `exit: 1`. The check
  requires perl to compile the file, runs the compiled program, and
  requires its stdout to be the start of perl's stdout for the same
  file (D12): the language stopped early, and said nothing perl
  wouldn't have. The program must end under perl, within the time
  allowed: where the language faults perl may only warn and carry on,
  so a loop that the fault alone would end never ends under perl
  (T131). Count such a loop by something the fault doesn't touch.
- **`refused`**: by hand. The compiler's message,
  `FILE:LINE:COL: message`, then `exit: 1`. The test passes when the
  program does not compile and says exactly that. perl isn't asked.
- **`new`**: a feature perl doesn't have. Its decision names the model
  or the referee that writes the output.

From step 6 a program can run for ever. `t/run.sh` kills a test after
`$TIMEOUT` seconds (60) and fails it, and stops one that prints more
than `$OUTPUT_BLOCKS` blocks of 512 bytes (16384: 8 MB), which a loop
that prints as it goes reaches long before the first; `t/checks.py`
does the same to perl, at 16 MB. Both are made to bite by
`t/harness/run.test.ts` and `t/checks/same-prints-for-ever.pl`.

perl and the compiler are given the same path, from the repository's
root (`t/000-say.pl`): a fault's line and a refusal's carry it, and so
will a `die`'s.

A model in `models/` is for edges: it writes a test program over the
values that find them, and the expected output from the definition
(Python's integers, `fractions`, `float`). The oracle check then holds
perl to the same answer. When the two disagree, neither file is
patched: the disagreement is a finding about a decision, and is
reported.

There is no referee, the workbench's second implementation in
`t/referee/`: perl is one, for everything but the exceptions to D2,
and each of those brings its own.

## What a `same` test may not do

Depend on anything D14 lists: hash order (sort the keys), a
reference's address, the real time, an unseeded `rand`, the process
id, the text of a system error. The seeds catch most of the first, and
the check also reads the file and rejects `keys`, `values`, `each` or
a whole hash that isn't the operand of `sort` (directly, or through
`map`, `grep` and `reverse`) or of `scalar`, since a small hash can
come out the same under every seed tried. The reading is by pattern
and errs toward rejecting: write the test so that it can see the sort.
It can't see whether the sort settles the order. **A sort with a tie
in it shows the hash's order**, and two tied keys come out the same
way under all eight seeds about once in 128 tests: break every tie
(`sort { $n{$b} <=> $n{$a} or $a cmp $b }`).
The rest are the author's to keep out, and a test that fails on
Stevan's machine and not the cloud's has usually found one. Nor, until
steps 8 and 15 say how, may it go 100 calls deep or call `warn`: perl
writes to stderr for both.

What the check doesn't see, the compiler mostly refuses: a test must
compile, and `no warnings`, `$SIG{__WARN__}`, `BEGIN`, string `eval`
and a dumper are not in the language. `docs/TRAPS.md`, "The checks
themselves", lists what a review got past the check and which step
has to close each.

## The check's own tests

`checks/` holds tests of `checks.py oracle` itself: each is a Perl
file, a `.expected`, and a header saying whether the check must pass
it or how it must fail it. They run with every `make checks`. Its
[`README.md`](checks/README.md) has the list.

## Determinism

A test runs the same way every time or it isn't a test. `run.sh` sets
what makes that so, as the runtime gains it:

- The collector's knobs (step 7; D63 to D65), in `t/knobs.sh`: every
  test runs with a collection at every allocation
  (`CURLY_GC_STRESS=1`), with a collected string's memory never used
  again (`CURLY_GC_POISON=1`), and under a cap of 256 MB
  (`CURLY_HEAP_CAP`), so that a root the collector was not shown is
  an `internal:` error the first time it could matter and a test that
  runs away is `out of memory` in a second. A test says otherwise for
  itself in its `# env:` header: the cap tests (800 on) turn the
  first two off, since under poison a gigabyte of garbage is a
  gigabyte held. `t/run.sh` sources the file and `t/checks.py` reads
  it, so the knobs are the same wherever a test's binary runs.
- A virtual clock, which moves only when nothing can run, and a fixed
  random seed (step 22).
- A scheduling seed, and record and replay of everything that comes in
  from the world, if concurrency comes (step 29).

None exists yet: a program can't do anything that differs between two
runs.

## Kinds of test

- `t/`: the golden tests. Each plan step adds some.
- `t/checks/`: the oracle check's own tests.
- `examples/`: programs, each with a `.expected` a golden test too
  (step 24).
- `compiler/tests/`: unit tests per pass, for what a golden test can't
  reach (token positions, the tree) and, while the refusals are few
  enough to list, each one's message and position.
- `runtime/tests/`: C programs that call the runtime directly, for
  what no compiled program can reach yet, run by a `.test.ts` beside
  them.
- `t/census/`: other people's probes, and a ratchet (step 11, below).

## The census

`t/census/` (from step 11, D11) is not golden tests. It is other
people's programs, written to find wrong answers in implementations of
Perl 5, each with perl's output. `make census` gives each a verdict:
SAME, REFUSED, LOUD or WRONG. The counts are a file; WRONG must be 0
and SAME may not fall. A WRONG is fixed before anything else, and
leaves a golden test behind.
