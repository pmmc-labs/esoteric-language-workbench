# A browser for a decision log

A decision log in the workbench's format (`docs/PROCESS.md`, "The
decision log") as one HTML page: the log hyperlinked, the project's
other documents beside it, what's open, an entry among the ones it
cites and the ones that cite it, and an arc map of the whole under a
lens. Built from
[`docs/briefs/decisions-browser.md`](../../docs/briefs/decisions-browser.md);
a64-slight's log, 290 entries in 30 sections, was the first to browse.

## Running it

```
make decisions                  # this log and a64-slight's, into build/
make decisions A64=path/to/a64-slight
```

That writes `build/decisions-curly.html` and
`build/decisions-a64-slight.html`, each with its JSON beside it, and
reads every `.md` beside each project's log: `LANGUAGE`, `DESIGN`,
`SURFACE`, `PLAN`, `TRAPS` and `BACKGROUND` first, those that exist,
then any others by name, and last the workbench's own `PROCESS`,
`MODELS` and `REPORT` as `--other`; and for a64-slight
its Sublime syntax, `editors/sublime/Slight/Slight.sublime-syntax`, to
colour the code in them. A page
is one file with the data inlined: open it from Finder or send it; it
needs no server and fetches nothing. By hand:

```
python3 tools/decisions/extract.py ../a64-slight/docs/DECISIONS.md -o a64.json \
    --doc ../a64-slight/docs/PLAN.md --doc ../a64-slight/docs/DESIGN.md
python3 tools/decisions/page.py a64.json -o a64.html --name a64-slight \
    --base https://github.com/pmmc-labs/a64-slight/blob/main/docs/
```

`--doc` is any Markdown document of the project, as many as wanted.
`--other` is a document to show with them that isn't about this log:
its `D12` is another log's, so it's left as text, and the document
cites nothing and drifts from nothing. A
link to one that came (`[DESIGN.md](DESIGN.md)`) stays in the page;
`--base` is where other relative links go, and without it they're shown
as text. `--syntax` is a Sublime syntax for the language's
s-expressions; without it code isn't coloured. `--fragment` leaves out the
doctype and metas, for a host that wraps the page itself.

The extractor fails if the entries it parsed aren't as many as the
lines that start `**D`, or if a number appears twice, so a format
change that drops an entry is loud. Its output is deterministic, so a
JSON can be committed and diffed.

## The page

- **Log.** Every entry in the file's order (or by number), every `Dn`
  a link, each entry's citations split into those it cites (earlier),
  those it points to (later, the "retired by" notes), and those that
  cite it. An entry retired or changed by a later one says so at the
  top, with the sentence that says it. The sidebar has the sections and
  a filter by who decided. The search box filters as you type: every
  word must match; `D158` is that entry; a bare number is that entry
  or the number as a word (a golden test, say). Enter on a single
  match, or on a number, goes to it; `/` focuses the box, Escape clears
  it. Each entry links to its neighbourhood in the graph and its place
  on the arc map, and lists the sections of the documents that cite it
  ("In the docs").
- **Docs.** Each document, cut at its headings, every `Dn` a link, and
  a quoted section title after a document's name (`PLAN.md's "Floats
  without boxes"`) a link to that section. A heading that ends with a
  status, "(done)", "(proposed, open)", "(agreed, D253)", gets a badge,
  and the sidebar filters by status, "Open only" among them. A
  citation of a decision a later one retired or changed, in a sentence
  that doesn't say so, has a wavy red underline, and the contents show
  how many a section has. The search filters sections; `D158` finds
  those that cite it. slight's code is coloured: special forms, a
  `defun`'s name and parameters, builtins, strings, comments, numbers,
  keywords, and `$$`, `#true` and the like.
- **Open.** The sections whose status is proposed, an idea, agreed but
  not built, or begun, with the decisions each cites; those marked
  **(open)** and the open questions; what was stopped, parked or
  retired, folded. Then every drifting citation, by document, with its
  sentence.
- **Around.** One entry in the middle, in full; on its left a card for
  each entry it cites, on its right one for each that cites it and for
  each document section that does, and with two steps a column further
  out each way. A card has the number, who decided (the dot), the
  section (the bar) and the title; a retired entry's number is struck
  through, and a retirement's line is red. Click a card to stand on
  that entry, so Back retraces the walk; hover one for its links among
  the cards shown. The middle stays put while long columns scroll.
- **Arcs.** Every entry on one axis by number, which is time (or as
  filed), and an arc for every citation: above the axis to an earlier
  entry, below to a later one. Coloured by the citing entry's section,
  by distance, or by who decided; retirements red. The strip is the
  sections. The axis is under a lens: scroll to zoom where the pointer
  is, and the axis stretches there and is squeezed toward the ends,
  which don't move, so the whole log is always in view; drag to slide
  the lens, `+` `-` `0` or the buttons to zoom. Where there's room an
  entry gets a dot, sized by how often it's cited, its number, and
  then its title. Hover an entry for its arcs; click to hold it, which
  brings it under the lens and puts the entry itself under the map,
  where its links hold the next; the arrow keys step along the axis.

A label that a document's table defines in a row's first cell
(TRAPS.md's `| T12 | program | ... |`) is a link wherever it's written,
with the row's next cell as its tooltip, and `#T12` is that row.

Links are `#D158`, `#around-D158`, `#arcs-D158`, `#T12`, `#open`, a document's
`#plan` and a section's `#plan-floats-without-boxes`, so Back works and
a view can be sent.

## The JSON

`format` (1), `person` (from the preamble's "**User** means X", or
null), `preamble`, `sections` (`title`, `intro`, `entries` in file
order), `unresolved` (mentions of numbers with no entry), `counts`, and
`entries`, each:

| Field | |
|---|---|
| `n`, `title`, `section`, `order` | Its number, title (Markdown), section's index, place in the file |
| `attribution` | `class` (`user`, `default`, `other`, `none`) and `text`; `points: true` when taken from the entry's points |
| `body` | Markdown, everything after the attribution |
| `mentions`, `mentioned_by` | Numbers, sorted, itself excluded |
| `retires`, `retired_by` | `{n, phrase}`, the phrase the clause that says so |
| `rejected` | `{text, alternatives}` from `Rejected:` to its paragraph's end, or null |
| `tests` | Golden test numbers cited (`golden test 381`, `tests 204–213`, `t/275`) |
| `cited_in` | The ids of the document sections that cite it |
| `first_seen`, `edits` | Null: room for history, which the first version leaves out |

With `--doc`, `docs` too, each `name`, `key` (the name as a link),
`title` and `sections`, each `id`, `level` (1 for the text before the
first `##`), `title`, `status` (`{class, text}` or null), `parent` (an
index), `body` (Markdown), `mentions`, and `drift` (`{n, by, sentence}`),
and `apart: true` on one given as `--other`; `doc_refs`, each quoted
section title the extractor resolved, by document, to its id; and
`labels`, each label a table defines, to `{id, text}`: the section with
its row, and the row's next cell.

## Judgement calls

- **One file, still.** A page opened from a file can load scripts from
  a CDN, so a server isn't what dependencies need; and nothing on a CDN
  reads a `.sublime-syntax` (highlight.js, Prism and Shiki each have
  their own grammars, and syntect, which reads Sublime's, is Rust). A
  server would earn its place for editing the log through the page.
- **Colouring code.** The tokenizer is the page's, about 40 lines, for
  s-expressions; the words come from the Sublime syntax at build time,
  read by `page.py` with regexes: each head in its `forms` context and
  the class its scope gives, whether a name or parameters follow
  (`defun`, `lambda`, `deftype`, `sig`), its `builtin` variable, and the
  constants in `atoms`. So a builtin added to the editor's syntax is
  coloured on the next build, and a syntax whose shape has changed fails
  the build rather than colour nothing. A block is slight's when it's
  marked `lisp` or `slight`, or unmarked and starting with `(` or `;`,
  so shell commands, output and `.sly` stay plain. Calls stay plain too,
  so a page of code isn't a page of colour. Code spans in running text
  aren't coloured.
- **No library.** Nothing here needs one, and without a CDN the page
  opens offline from a `file://` URL, which matters more for a file
  sent to be tried.
- **No graph.** The first version had a force layout: around an entry,
  one section, or everything. It crowded as soon as an entry had a
  dozen neighbours, and a dot can't be read, so every node needed a
  hover. Around an entry, the question is a list (what does this lean
  on, what leans on it), and columns of cards answer it with the
  titles in view and no layout to settle. The whole and the sections
  are the arc map's. What went: edges between two neighbours, which
  hovering a card now shows instead, and the section view. `#graph-D12`
  still goes to Around.
- **The lens** is Sarkar and Brown's fisheye: a point a fraction x of
  the way from the focus to an end goes to (d+1)x / (dx+1), a
  hyperbola, with d+1 the stretch at the focus. It's driven by where
  the pointer is but doesn't follow it: a lens that follows the
  pointer moves its targets as you reach for them. So a zoom or a drag
  solves for the focus that keeps the point under the pointer where it
  is (a bisection: the map falls as the focus rises). The scroll wheel
  over the map zooms and doesn't scroll the page.
- **Whose `D12`.** A project that copied the workbench's `PROCESS.md`
  and `MODELS.md` has documents that cite other logs' numbers; linked,
  each would go to the wrong decision. `--other` is the Makefile's
  guess for those three names; a project's own document that cites
  another log wants it too.
- **Mentions inside code spans don't count.** The brief's 291st number
  was `\u{D800}` in a Unicode range. Every mention now resolves.
- **Ranges.** `D175–D178` is each of the four. `D281 to D284` is too,
  but only when the span is 20 or less, so a chain written "D8 to D167"
  isn't 160 mentions.
- **Who decided** is the attribution's first word: `User`, or the
  person's name as the preamble gives it (a64-slight's later entries
  say *Stevan*), is user; `Default` is default; anything else is other
  (a64-slight's D217, *Claude, ... for Stevan's ...*). An entry made of
  points, each with its own attribution (D179), takes theirs if they
  agree. A mixed one, *User, the shape default*, counts as user, since
  the first word is who settled it.
- **Retirements are best effort.** A clause that says retires,
  replaces, supersedes, withdraws or "no longer holds". An active verb
  (retires, replaces, `Retired:`) takes the entries named after it, a
  passive one ("D76 is retired", "D52, D53 ... superseded") those
  before it, so "Refines D151 and D152, and withdraws TLS" retires
  nothing. "Retired by Dm" names the retirer; otherwise the direction
  is the numbers' order, since numbers are time. Refining isn't
  retiring (D151 "refines D30"). A document heading whose status says
  "retired by Dm" retires the other decisions its status names, which
  is how D277 retires D243 and D244: PLAN.md says so, the log doesn't.
  a64-slight gives 29 pairs; the page says "retired or changed", since
  most are in part.
- **A status** is a heading's trailing parenthesis, read by its words,
  the first that fits: retired, idea, proposed or open, stopped
  (stopped, rests, dropped, withdrawn, parked), begun, done or built,
  agreed. So "(agreed and built, D286)" is done, and "Floats without
  boxes (... stopped, D260; (c)'s step 1 done ...)" is stopped. A
  section under a heading named "Parked" is parked. A parenthesis with
  none of the words, LANGUAGE.md's "(@include :http)", is part of the
  title.
- **Drift** is a sentence that cites a retired decision and doesn't say
  so: no retiring word, no past tense ("was", "since", "till", "no
  longer", "instead", "now"), and not citing the retirer. Only a number
  written out counts (`D151–D155` isn't a claim about D152), and a
  retirement that was itself retired doesn't (D243's, once D277 retired
  it). Code blocks are examples, not citations. a64-slight has 15 in
  DESIGN, LANGUAGE and BACKGROUND, among them BACKGROUND's "gives stacks
  back at `recv` (D9)", and 24 in PLAN. A document most of whose
  headings (a third or more) have a status is a plan, a history, whose
  drift is expected, so the Open view folds it.
- **Open** is a status of proposed, idea, agreed or begun; a section
  marked **(open)**, though not where the docs name the rule ("anything
  marked (open)", "an (open) item"), which is every use in both
  projects today; or a section titled "Open questions".
- **Arcs above and below.** Most citations look back; the ones that
  look forward are notes added to an old entry, and below the axis
  they're the log's corrections, at a glance.
- **Colour for 30 sections** can't be 30 distinct colours; they're
  spread round the hue circle, and hovering names the section.
- **Sections or attribution** as the grouping is a control in each
  view, not a choice made here, as the brief asked; the log keeps the
  file's order, or the numbers'.

## To ask, after a day's use

1. Do you reach for Around or the arc map?
2. Which grouping helps more, the sections or who decided?
3. Is history wanted (when an entry landed, how it was edited), and
   for what?
