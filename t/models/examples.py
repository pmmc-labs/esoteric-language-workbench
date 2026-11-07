#!/usr/bin/env python3
"""Model for step 8 (the examples): the expected output of the six programs
in examples/, and the standard input of the word count.

Each program is transcribed into Python by hand from the definition in
LANGUAGE.md, never by running the compiler. The transcription follows
D7 literally: every variable owns its value, and every assignment,
argument, return and store takes `copy.deepcopy` of what it is given
(the compiler does the opposite: it shares and never writes). `/` is not
used by any example, but `%` is, on non-negative ints only, where Python
and Ditto agree. The printed form is written from LANGUAGE.md (`show`):
strings bare at the top level and quoted inside a list or map, escapes
for backslash, quote, newline, tab and return, keys printed as values.
`print(x)` of a bool is `true`/`false`, of nil `nil`. The word count's
passage is here and written out by `--stdin`, so the program and the
model read the same text.

    python3 t/models/examples.py fizzbuzz > examples/fizzbuzz.expected
    python3 t/models/examples.py recursion > examples/recursion.expected
    python3 t/models/examples.py sorting > examples/sorting.expected
    python3 t/models/examples.py --stdin wordcount > examples/wordcount.stdin
    python3 t/models/examples.py wordcount > examples/wordcount.expected
    python3 t/models/examples.py routes > examples/routes.expected
    python3 t/models/examples.py ledger > examples/ledger.expected
"""
import copy
import sys

PASSAGE = """\
The old town of Marlow sits where the river bends, and on market days
it fills with more people than the narrow streets were ever built for.
Farmers bring cheese, apples and honey; the baker sells loaves that
are gone by ten o'clock; and a man with a cart of secondhand books
pitches his umbrella beside the fountain, whatever the weather. Nobody
in Marlow is in a hurry. A purchase takes as long as the conversation
that goes with it, and the conversation, as a rule, begins with the
weather and ends with the news of somebody's cousin.

Anna Brandt has kept the stall at the corner for thirty years -- her
mother kept it before her. She sells nothing but pears, and she knows
every one of them. "This one is ready today," she will say, "that one
needs till Friday, and that one, well, that one is for jam." Her
customers don't argue. They have learned that the pear she calls ready
is the best pear they will eat all week, and that the one she calls
jam is, in fact, still a very good pear.

At noon the bells of St. Anne ring twelve times, and for a moment the
whole square goes quiet, as if the town were counting along with them.
Then the noise comes back: the clink of cups, the slap of a fish on
a board, a child asking for the third time whether they can go home
yet. The baker shuts his shutters. The man with the books reads one of
them himself, and the pears -- the last of the pears -- are packed
into a basket for the first customer who asks.

By three the square is empty, and the river is the only thing in Marlow
that still has somewhere to be.
"""


def show(v, top=True):
    if v is None:
        return "nil"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        if top:
            return v
        out = v.replace("\\", "\\\\").replace('"', '\\"')
        out = out.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
        return '"' + out + '"'
    if isinstance(v, list):
        return "[" + ", ".join(show(x, False) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join(show(k, False) + ": " + show(x, False) for k, x in v.items()) + "}"
    raise AssertionError(v)


def fizzbuzz(out):
    for i in range(1, 101):
        if i % 15 == 0:
            out("FizzBuzz")
        elif i % 3 == 0:
            out("Fizz")
        elif i % 5 == 0:
            out("Buzz")
        else:
            out(show(i))


def recursion(out):
    def fact(n):
        if n == 0:
            return 1
        return n * fact(n - 1)

    def fib(n):
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    for n in range(0, 21):
        out(f"{n}! = {fact(n)}, fib({n}) = {fib(n)}")


def sorting(out):
    def quicksort(xs):
        xs = copy.deepcopy(xs)
        if len(xs) < 2:
            return xs
        pivot = xs[0]
        smaller = []
        larger = []
        for i in range(1, len(xs)):
            if xs[i] < pivot:
                smaller = smaller + [xs[i]]
            else:
                larger = larger + [xs[i]]
        return quicksort(smaller) + [pivot] + quicksort(larger)

    def insertion_sort(xs):
        xs = copy.deepcopy(xs)
        for i in range(1, len(xs)):
            j = i
            while j > 0 and xs[j - 1] > xs[j]:
                t = xs[j]
                xs[j] = xs[j - 1]
                xs[j - 1] = t
                j -= 1
        return xs

    data = [31, 4, 15, 9, 26, 5, 35, 8, 97, 93, 2, 38, 46, 26, 43]
    out(show(quicksort(copy.deepcopy(data))))
    out(show(insertion_sort(copy.deepcopy(data))))
    out(show(data))
    out(show(sorted(data) == quicksort(copy.deepcopy(data))))


def wordcount(out):
    def clean(word):
        o = ""
        for c in word.lower():
            if ("a" <= c <= "z") or c == "'":
                o += c
        return o

    counts = {}
    total = 0
    for raw in PASSAGE.split():  # words(): runs of space, tab, newline, return
        w = clean(raw)
        if w != "":
            counts[w] = counts.get(w, 0) + 1
            total += 1
    best = ""
    for w in counts:
        if best == "" or counts[w] > counts[best]:
            best = w
    out(f"{total} words, {len(counts)} different")
    out(f'most common: "{best}", {counts[best]} times')
    for w in counts:
        if counts[w] > 1:
            out(f"{w}: {counts[w]}")


def routes(out):
    def route(roads, start, goal):
        roads = copy.deepcopy(roads)
        came_from = {}
        came_from[start] = start
        queue = [start]
        nxt = 0
        while nxt < len(queue):
            here = queue[nxt]
            nxt += 1
            if here == goal:
                path = [goal]
                while path[0] != start:
                    path = [came_from[path[0]]] + path
                return path
            for road in copy.deepcopy(roads[here] if here in roads else []):
                if road not in came_from:
                    came_from[road] = here
                    queue = queue + [road]
        return None

    roads = {
        "home": ["bakery", "park"],
        "bakery": ["home", "market", "school"],
        "park": ["home", "lake"],
        "market": ["bakery", "station"],
        "school": ["bakery", "station"],
        "lake": ["park"],
        "station": ["market", "school"],
    }
    out(show(route(roads, "home", "station")))
    out(show(route(roads, "lake", "school")))
    out(show(route(roads, "home", "airport")))


def ledger(out):
    def apply(accounts, batch):
        accounts = copy.deepcopy(accounts)
        for t in copy.deepcopy(batch):
            if t["from"] not in accounts or t["to"] not in accounts:
                return {"ok": False, "why": f"no account for {show(t)}"}
            if accounts[t["from"]]["balance"] < t["amount"]:
                return {"ok": False,
                        "why": f"{t['from']} has only {accounts[t['from']]['balance']}"}
            accounts[t["from"]]["balance"] -= t["amount"]
            accounts[t["to"]]["balance"] += t["amount"]
            accounts[t["from"]]["log"] = accounts[t["from"]]["log"] + [f"-{t['amount']} to {t['to']}"]
            accounts[t["to"]]["log"] = accounts[t["to"]]["log"] + [f"+{t['amount']} from {t['from']}"]
        return {"ok": True, "accounts": accounts}

    accounts = {
        "alice": {"balance": 100, "log": []},
        "bob": {"balance": 50, "log": []},
        "carol": {"balance": 0, "log": []},
    }
    opening = copy.deepcopy(accounts)
    batches = [
        [{"from": "alice", "to": "bob", "amount": 30}, {"from": "bob", "to": "carol", "amount": 60}],
        [{"from": "carol", "to": "alice", "amount": 10}, {"from": "carol", "to": "bob", "amount": 90}],
        [{"from": "bob", "to": "dave", "amount": 5}],
    ]
    for batch in copy.deepcopy(batches):
        result = apply(copy.deepcopy(accounts), batch)
        if result["ok"]:
            accounts = copy.deepcopy(result["accounts"])
            out(f"applied {len(batch)} transfers")
        else:
            out(f"rejected: {result['why']}")
    for name in copy.deepcopy(accounts):
        out(f"{name}: {accounts[name]['balance']} {show(accounts[name]['log'])}")
    out(f"opening: {show(opening)}")


PROGRAMS = {f.__name__: f for f in (fizzbuzz, recursion, sorting, wordcount, routes, ledger)}

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--stdin"]:
        assert args[1] == "wordcount"
        sys.stdout.write(PASSAGE)
    else:
        PROGRAMS[args[0]](lambda line: sys.stdout.write(line + "\n"))
