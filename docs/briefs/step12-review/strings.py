#!/usr/bin/env python3
"""Q2a, a key in a string, held to perl: `"$h{CONTENT}TAIL"` for every
CONTENT of up to three pieces and every TAIL of up to two, against a model
of the rule as the proposal has it:

  CONTENT is blanks, one word, blanks   -> the element at that word
  CONTENT is blanks, $name, blanks      -> the element at that variable
  anything else                         -> refused
  TAIL begins `[`, `{`, or `->` before `[ { @ $ %` -> refused (step 11a's
  list for what follows a variable, with `[` counted as it is after an
  element)

Reports each string the model takes where perl prints something else,
warns or stops, and, with --tails, the tails by what perl does.

    python3 docs/briefs/step12-review/strings.py          # about 60,000 strings, in batches
"""
import itertools, re, sys
from common import perl

PIECES = ['a', 'k', 'q', 's', 'y', 'x', 'if', 'true', 'time', 'v65', 'A', '_', '1', '0', '01', ' ', '\t', '\n', '$k', '$i', '$', '@', '-', '+', '.', ',',
          "'", '=>', '::', '(', ')', '[', ']', '{', '}', '#', '\\', '=', 'e', 'k1']
TAILS = ['', '[', '{', '-', '>', ':', '(', '.', "'", ' ', '$', '@', '%', '*', ']', '}', 's', '0', '\\']
HASH = {'a': 'A', 'k': 'K', 'q': 'Q', 's': 'S', 'y': 'Y', 'x': 'X', 'if': 'IF', 'true': 'TRUE', 'time': 'TIME', 'v65': 'V65', 'A': 'AA', '_': 'U',
        '1': 'ONE', '0': 'ZERO', '01': 'OCT', 'e': 'E', 'k1': 'K1', 'ka': 'KA', 'kk': 'KK', 'aa': 'AAA', 'kq': 'x', 'ak': 'x'}
VARS = {'k': 'a', 'i': '1'}
WORD = re.compile(r'^[ \t]*([A-Za-z_][A-Za-z0-9_]*)[ \t]*\Z')
VAR = re.compile(r'^[ \t]*\$([A-Za-z_][A-Za-z0-9_]*)[ \t]*\Z')
BAD_TAIL = re.compile(r'^(\[|\{|->[\[{@$%])')


def model(content, tail):
    """What the rule prints for "<$h{content}tail>", or None for refused."""
    if BAD_TAIL.match(tail):
        return None
    if re.search(r'[$@]', tail) or '\\' in tail or '"' in tail:
        return None                       # another variable or an escape: not this test's business
    m = WORD.match(content)
    if m:
        key = m.group(1)
    else:
        m = VAR.match(content)
        if not m or m.group(1) not in VARS:
            return None
        key = VARS[m.group(1)]
    if key not in HASH:
        return None                       # undef: D48's fault
    return '<' + HASH[key] + tail + '>'


def batch(cases):
    """Run many strings in one perl each would hide which one stops: one perl a string,
    but only for strings the model takes; the others are counted, not run."""
    bad = []
    for content, tail in cases:
        want = model(content, tail)
        if want is None:
            continue
        setup = 'my %%h = (%s); my $k = "a"; my $i = 1; ' % ', '.join('"%s", "%s"' % kv for kv in HASH.items())
        out, err, code = perl(setup + 'say "<$h{%s}%s>";' % (content, tail))
        batch.ran += 1
        if out != want + '\n' or err or code:
            bad.append((content, tail, want, out, err.strip().split('\n')[0][:100], code))
    return bad


batch.ran = 0


def main():
    cases = []
    for n in (1, 2, 3):
        for c in itertools.product(PIECES, repeat=n):
            content = ''.join(c)
            if '"' in content:
                continue
            cases.append((content, ''))
    seen = set()
    cases = [c for c in cases if not (c in seen or seen.add(c))]
    tails = [a + b for a in TAILS for b in TAILS]
    for content in ('a', ' a ', '$k', ' $k ', 'q', 'true'):
        for t in tails:
            cases.append((content, t))
    bad = batch(cases)
    print('%d strings, %d the model takes and perl was asked about, %d differ' % (len(cases), batch.ran, len(bad)))
    for b in bad:
        print('  content %r tail %r: model %r, perl %r %s exit %d' % b)
    if '--tails' in sys.argv:
        for t in tails:
            out, err, code = perl('my %h = (a => "A"); say "<$h{a}' + t + '>";')
            print('  tail %-6r %s' % (t, out.strip() if code == 0 and not err else 'STOPS/WARNS: ' + err.strip().split('\n')[0][:90]))


main()
