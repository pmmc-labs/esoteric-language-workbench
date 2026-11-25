# The review of step 5's definition, and of the compiler built from it

As step 3's and step 4's ([`../step4-review/`](../step4-review/README.md)):
a reader with the proposal's words and perl 5.42, who wrote a model of
what the step adds, generated programs, and held them to perl; and then,
the step having been built meanwhile, held the compiler to perl with the
same generators. What it found is in its report (and, once it is taken
up, in `../../TRAPS.md` and `../../PLAN.md` under step 5).

The model does not write the built language again. Every operator of
steps 1 to 4 is the runtime's own function, called through `rtm.c`
(`runtime/rt.c` with a fault that can be caught and output into a
buffer, built into a scratch directory when `model.py` is loaded). What
is new is written from the proposal alone: variables and scopes, `my` in
a condition, assignment as an operator, `OP=` and what an undef on its
left is, `++` and `--` by what the variable holds, late reads, blocks,
`if`/`elsif`/`else`/`unless`, modifiers.

| File | |
|---|---|
| `model.py` | The model: a program is a tree of tuples; `run` gives its output and its fault; `show` prints it with brackets round every operand. The refusals it knows (a constant `=` in a test, `(...) x N` where `say`'s list reaches), and the findings as predicates, so that a search can go on past them |
| `rtm.c` | The bridge to the built runtime |
| `minshow.py` | A second printer: the fewest brackets perlop's table allows, and `say E;` for `say(E);` if asked |
| `harness.py` | A program under the model and under perl, held to the rule: no fault, the same bytes and perl silent; a fault, a prefix |
| `gen_late.py` | Random programs about late reads: assignment, `OP=`, `++`/`--`, the logical operators and builtins over three variables |
| `gen_late2.py` | Not random: every operator and builtin, a left operand made from `$x` in 39 forms, a right operand that changes `$x` in 22 ways, six contexts |
| `gen_alias.py` | Not random: the target of an assignment among its own operands, every operator |
| `gen_struct.py` | Blocks, chains of `if`, modifiers, where a `my` is visible |
| `gen_past.py` | Pasts: 280 values of every kind and edge, 62 read-only statements, then `++` `--` `OP=`, and 49 observations |
| `gen_past_ex.py` | Not random: every value, every single read, `++` and `--`, five observations |
| `gen_pair.py` | The claim itself, on pairs: a program, and the same with reads put in; where perl's two outputs part, the model must have faulted in both by then |
| `gen_prec.py` | `gen_late.py`'s trees through `minshow.py` |
| `gen_fh.py` | The proposal's file-handle rule as text, held to perl |
| `classify_found.py` | perl's `Found = in conditional` held to a rule over `gen_struct.py`'s programs |
| `compiler.py` | **The compiler held to perl**, with the generators above: `python3 docs/briefs/step5-review/compiler.py KIND SEED COUNT`. Programs go forty to a file, each in a block; what differs is run again alone before it is called WRONG. `plant` puts two known WRONG programs in, as its own check |
| `gen_cat.py` | Strings: rows of dots, `.=`, assignments inside expressions, constant tests: where perl makes one operation of several (kind `cat` of `compiler.py`) |
| `spacing.py` | The compiler's reading of a text held to perl's, where the blanks are: a generated program cut into tokens and joined again with nothing, a blank, a newline or a comment between each two; through `compiler.py` |
| `handles.py` | The compiler's file-handle refusal: a variable first after `say`, `print`, `substr(`, `index(`, each blank, each operator spelled both ways, each operand; through `compiler.py` |
| `shapes.py`, `shapes/` | Programs written by hand, a paragraph each, given to the compiler and perl: `python3 docs/briefs/step5-review/shapes.py docs/briefs/step5-review/shapes/*.txt`. **`shapes/findings.txt` is what the review found WRONG in the compiler as it was built (d7883c5), one program of each kind**: all twelve should come to be refused, faults, or the same as perl |
| `probe.py` | The same paragraphs given to `perl -c` and perl alone, with `-d` for what perl parsed |

Each `gen_*.py` and `compiler.py` says in its first lines how to break
the model or plant a program so that the check goes red, and each was
seen to. Programs and logs go to the system's scratch directory, never
into the tree. `CURLY_PERL` names perl 5.42, as everywhere. One perl
runs at a time in each script. None of this is part of `make test`.
