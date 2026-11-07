# Background

Prior art, what was borrowed, and ideas parked so they stop coming up.

## Borrowed

- **The persistent cons list** (Lisp, 1958; every functional language
  since). A history is one: a layer points at the one below, a write
  conses, `@k` is `k` cdrs, and since nothing is mutated, sharing is
  free. Strata's twist is that every variable is one, and assignment is
  cons onto it.
- **Single assignment / immutable bindings** (Erlang, SSA form,
  dataflow languages such as Lucid). Lucid's `fby` ("followed by") and
  its view of a variable as the stream of its values over iterations is
  the closest ancestor of D7; Strata keeps the stream on the variable
  and lets the program read backwards into it, where Lucid's operators
  (`first`, `next`) look along the stream from the current point.
- **Version history as data**: Datomic's "the database as a value",
  where every fact is kept with its time and you query as-of; git's
  `HEAD~k`, which is exactly `@k` (and its syntax suggested the
  postfix operator).
- **Checked 64-bit integers** with truncating division: Rust's debug
  builds, Java's `Math.addExact`.
- **Ghuloum's incremental compiler** for the build order (`PROCESS.md`).

## Not borrowed

No existing esoteric language is recreated. The nearest in spirit are
those built around one unusual memory model (Befunge's grid, Brainfuck's
tape, Unlambda's combinators); Strata's history is meant to be one that
an ordinary program can live with.

## Parked

- **Strings as histories of characters.** Elegant (a string's reverse
  would be its history read from the top), but makes strings containers
  and needs printing and `+` rules for histories (D21).
- **`rewind x`**, removing layers. Against D7.
- **Reading forward** (`x@-1`, "the next value"): would need lazy or
  speculative evaluation.
- **Garbage collection.** With D4's scale, never-free (D26) is enough.
  A collector would need a shadow stack of roots in the generated C.
- **Input.** `stdin` lines and `num(s)` would make filters writable;
  parked with D28 until a program needs it.
- **A referee** (a Python evaluator of Strata) as `PROCESS.md`
  describes: not in this run, by the brief.
