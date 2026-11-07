# Brief: a browser for a decision log

For a session that builds the first version. Written at the end of a
Fable session that measured the problem and discussed the shape;
nothing has been built. The person is Stevan; the first log to browse
is a64-slight's.

## Setting up the session

- **Model:** Opus, high effort. This is a design-and-build task with
  judgement in it (what to show, what to leave out), which
  `docs/MODELS.md` puts at the large tier; the build itself is medium.
- **Repositories:** `pmmc-labs/esoteric-language-workbench` (this one;
  the tool lives here, since it's process tooling that works on any
  log in this format) and `pmmc-labs/a64-slight` (the first subject,
  read-only: nothing in it changes). Attach both; work in the workbench.
- **Read first, in this order:** this brief; `docs/PROCESS.md`'s
  section "The decision log" and the entry format at the top of
  `docs/DECISIONS.md`; then a64-slight's `docs/DECISIONS.md` itself,
  which is the data, and its `CLAUDE.md`'s working rules, which say why
  the log is shaped as it is. Don't read a64-slight's `PLAN.md` or
  `DESIGN.md` beyond what the entries point at; they're large and not
  the subject.
- **History:** the first version needs none. If a later version does,
  note that a cloud clone of a64-slight is shallow (about 310 commits,
  back to 2026-10-10), the log was moved into `docs/` on 2026-11-03 so
  `git log --follow` is needed across the move, and D1 to D164 predate
  the shallow window: deepen with a bounded `git fetch --depth=1000`
  before any timeline work.
- **Process:** the workbench's rules apply (`CLAUDE.md`). This is a
  tool, not a language change, so no decision entry is needed for its
  existence; a design choice worth recording goes in a short section of
  the tool's own README rather than the log. Commit as the work lands;
  the commit hook wants a step or decision in the subject only for
  changes under `compiler/`, `runtime/`, `lib/` or `bin/`, which this
  doesn't touch.

## The problem

a64-slight's `docs/DECISIONS.md` is 290 entries and 7,500 lines, in 30
sections. It stopped fitting in the author's head: finding a decision,
reading it, and following it to the ones it leans on or that retired it
means searching a long file by number. In the author's words, the
decisions file no longer fits in his context window. The log is the
process's memory; if the person can't navigate it, the agent is the
only one who can, and that's the wrong way round.

The goal, in the author's order: find a decision; read its write-up;
jump to the decisions it cites and the ones that cite it; see how
decisions group and relate; and, later, visualise the relations in
more than one way. A hyperlinked rendering of the file does most of
the first three; a graph does the fourth; the fifth is open (the
author mentioned the cross-reference arc map of the Bible as the kind
of thing he has in mind: every entry on a line, arcs between those that
refer to each other, the shape of the whole visible at once).

## The data, as measured

- 290 entries `**Dn. Title.**`, numbered by time, placed by subject:
  the 30 `## ` sections mix subject ("Language", "Values and memory")
  and era ("Step 7", "Benchmarks", which has 49 entries alone). So the
  file's order and the time order differ.
- Every entry has an attribution in italics right after its title:
  `*(User)*`, `*(Default)*`, or a longer form with a quote or a reason
  (129 User, 92 Default, the rest mixed or quoted; parse the italic
  span and classify it as user, default or other, keeping the text).
- 877 mentions of a `Dn` inside entries, over all 291 numbers: a dense
  graph. Direction: an entry mentions earlier ones it leans on and
  sometimes later ones that changed it ("retired by D277", "since
  D167"). 17 entries carry explicit retire, supersede or withdraw
  language; the long chain is D8 to D167 to D276.
- Entries contain `Rejected:` passages, code spans, and references to
  golden test numbers, files and plan sections. Those are worth
  extracting as fields where cheap (rejections, test numbers), and
  otherwise left in the body.
- The format is the workbench's too (`docs/DECISIONS.md` here, 27
  entries): the tool should read both without special cases, which is
  the test that it reads the format and not one file.

## What to build, first version

One extractor and one page.

**The extractor**, Python, standard library: reads a `DECISIONS.md`,
writes `decisions.json`: for each entry its number, title, section,
attribution (class and text), body as Markdown, the numbers it
mentions, the numbers that mention it, whether it retires or is retired
by another (from the language in the text, best effort, with the phrase
kept), rejected alternatives if separable, test numbers cited. Plus the
section order and the file's preamble. Deterministic, so the JSON can
be committed and diffed. Assert the entry count against a plain count
of `**D` lines, so a parse that drops an entry fails loudly.

**The page**, a single static HTML file that loads the JSON (or has it
inlined, so it opens from a file:// URL without a server; prefer
inlined, one file to send), with:

1. **The log, hyperlinked.** Every entry rendered, in file order, with
   every `Dn` in its text a link to that entry, a back-reference list
   under each entry ("cited by D12, D40, ..."), an anchor per entry, and
   the attribution shown as a mark. A sidebar or top bar with the
   sections, and a search box that filters by number, title words or
   body words as you type. This alone answers the first three goals and
   is the part to get right first.
2. **The graph.** A force-directed layout of entries and mentions:
   node size by citations received, colour by attribution, sections as
   hulls or a colour ring, retire links as a distinct edge. Click a
   node to open its entry in the log view; hover for the title. A
   control to show one section, or one entry's neighbourhood to a
   chosen depth, since 290 nodes and 877 edges all at once is a hairball
   and the neighbourhood is what the author wants to see.
3. **The arc map**, the second visualisation, if time allows: all
   entries on one axis in number order, an arc for every mention, arc
   colour by the citing entry's section or by distance. It shows the
   shape of the whole and the long reaches; it is the Bible map the
   author named. Click an arc's end to open the entry.

Keep the page to one dependency at most (a force layout library from a
CDN is fine; the arc map needs none, SVG by hand is enough). Dark and
light both readable. Works on the a64-slight log and the workbench's
own; `make` target or one command to regenerate both.

Leave out of the first version: history (when each entry landed, how
it was edited), the commit-to-decision join, editing the log through
the page. Each is a later version if wanted; the extractor's JSON
should leave room (a `first_seen` and `edits` field that are null for
now) rather than be redesigned.

## What done looks like

- `tools/decisions/` (or a name the builder prefers) in the workbench:
  the extractor, the page template, a README saying how to run it and
  the design choices that were judgement calls.
- `build/decisions-a64-slight.html` and `build/decisions-workbench.html`
  generated and opened once by the builder; the a64-slight one sent to
  the person to try, since whether it helps him find things is the
  only test that matters.
- The extractor asserts its entry counts (290 and 27 today).
- Three questions put to the person after he has used it for a day:
  whether the neighbourhood view or the arc map is the one he reaches
  for; whether the sections or the attribution is the better grouping;
  and whether history is wanted and for what.

## Things the Fable session noticed that the builder should know

- The number of an entry is stable and never reused, and cross-
  references use the bare form `D123` almost everywhere, occasionally
  `D8's` or `(D8)` or `D8–D10` ranges; a range is a mention of each.
- Some mentions are to the entry itself or to a decision number that
  belongs to the plan rather than the log (the plan has numbered steps,
  not Dn, so this shouldn't happen, but check that every mentioned
  number resolves to an entry; the count of distinct mentioned numbers
  was 291 against 290 entries, so one doesn't).
- Sections that are eras ("Step 7") will look odd beside sections that
  are subjects ("Language") in any grouping view; let the view take
  either and let the person say which he wants, rather than re-sorting
  the log.
- The author reads on a Mac; the page should be fine in Safari.
