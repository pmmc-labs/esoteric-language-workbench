#!/usr/bin/env python3
"""A word that is not a string: every word perl gives a meaning to, and some
shapes of word, in each place the proposal says "that string, whatever the
word". Reports each (word, place) where perl does not give exactly the word
as the key in silence: another key, a warning, or no compile.

    python3 docs/briefs/step12-review/words.py            # all
    python3 docs/briefs/step12-review/words.py q s y      # these words
"""
import sys
from common import perl, keywords

EXTRA = ['a', 'b', 'k', 'name', 'x3', 'x', 'xx', 'v65', 'v1', 'v1_0', 'v', 'e1', 'E', 'A', 'Z', 'LABEL', '_', '__', '_1',
         'a1', 'if_', 'main', 'CORE', 'SUPER', 'STDIN', 'nan', 'inf', 'Inf', 'NaN', 'qw', 'tr', 'lt', 'f', 'g', 'ff',
         '__SUB__', '__CLASS__', 'ne', 'isa', 'err', 'dump', 'format', 'sub', 'package', 'our', 'state', 'my', 'do', 'eval',
         'BEGIN', 'END', 'print', 'say', 'method', 'class', 'field', 'ADJUST', 'any', 'all', 'try', 'catch', 'finally', 'defer']

SHOW = 'say join "|", map { "[$_]" } sort keys %h;'
# place: (text with W for the word, what the proposal's rule gives for the key, W for the word)
PLACES = {
    'elem':          ('my %h; $h{W} = 1; ' + SHOW, 'W'),
    'elem-blank':    ('my %h; $h{ W } = 1; ' + SHOW, 'W'),
    'elem-lines':    ('my %h; $h{\nW\n} = 1; ' + SHOW, 'W'),
    'elem-comment':  ('my %h; $h{W # c\n} = 1; ' + SHOW, 'W'),
    'elem-read':     ('my %h = ("W", 7); say $h{W};', None),
    'arrow':         ('my %h = (W => 1); ' + SHOW, 'W'),
    'arrow-tight':   ('my %h = (W=>1); ' + SHOW, 'W'),
    'arrow-line':    ('my %h = (W\n=> 1); ' + SHOW, 'W'),
    'arrow-comment': ('my %h = (W # c\n  => 1); ' + SHOW, 'W'),
    'arrow-second':  ('my %h = (k => 1, W => 2); ' + SHOW, 'W,k'),
    'arrow-value':   ('my %h = (k => W => 2); ' + SHOW, None),          # a word as a value, then =>
    'arrow-first':   ('my @l = (W => 1); say "[$l[0]]";', 'W'),
    'arrow-say':     ('say W => 1;', None),
    'arrow-call':    ('sub ff(%o) { return join "|", map { "[$_]" } sort keys %o } say ff(W => 1);', 'W'),
    'arrow-return':  ('sub ff() { return (W => 1); } my %h = ff(); ' + SHOW, 'W'),
    'arrow-push':    ('my @l; push @l, W => 1; say "[$l[0]]";', 'W'),
    'arrow-join':    ('say join W => 1, 2;', None),
    'arrow-elem':    ('my %h; $h{W => } = 1; ' + SHOW, None),
    'arrow-stmt':    ('my %h; %h = (W => 1); ' + SHOW, 'W'),
    'arrow-map':     ('my %h = map { W => 1 } 1; ' + SHOW, None),
    'arrow-map2':    ('my %h = map { ; W => 1 } 1; ' + SHOW, None),
    'arrow-ternary': ('my %h = (1 ? W => 2 : 3, 4); ' + SHOW, None),
    'arrow-after-x': ('my %h = ("k" x W => 2); ' + SHOW, None),
    'string':        ('my %h = ("W", 7); say "$h{W}";', None),
    'string-blank':  ('my %h = ("W", 7); say "$h{ W }";', None),
    'slice-word':    ('my %h = ("W", 7, k => 2); say @h{W, "k"};', None),
    'exists':        ('my %h = ("W", 7); say exists $h{W} ? "y" : "n"; say delete $h{W};', None),
    'with-sub':      ('sub W() { return "CALLED" } my %h = (W => 1); $h{W} = 2; say join "|", map { "[$_=$h{$_}]" } sort keys %h;', None),
}


def expect(place, word):
    text, want = PLACES[place]
    if place == 'elem-read' or place.startswith('string'):
        return '7\n'
    if place == 'exists':
        return 'y\n7\n'
    if place == 'arrow-say':
        return word + '1\n'
    if place == 'arrow-join':
        return '1%s2\n' % word
    if place == 'with-sub':
        return '[%s=2]\n' % word
    if place == 'arrow-first':
        return '[%s]\n' % word
    if place in ('arrow-call', 'arrow-push'):
        return '[%s]\n' % word
    if want is None:
        return None
    return '|'.join('[%s]' % k for k in sorted(want.replace('W', word).split(','))) + '\n'


def main():
    words = sys.argv[1:] or sorted(set(keywords() + EXTRA))
    kw = set(keywords())
    n = 0
    odd = {}
    for w in words:
        for place, (text, _) in PLACES.items():
            if place == 'with-sub' and w in kw:
                continue
            n += 1
            out, err, code = perl(text.replace('W', w))
            want = expect(place, w)
            if want is None:
                # a place the proposal does not say is in: what perl does when it runs
                if code == 0:
                    odd.setdefault((place, 'not in the proposal, and perl runs it' + (', warning' if err else ', in silence: ' + out.strip().replace(w, 'W'))), []).append(w)
                continue
            if out == want and not err and code == 0:
                continue
            shown = w
            if code:
                what = 'perl stops'
            elif err:
                what = 'perl warns'
            else:
                what = 'ANOTHER KEY, IN SILENCE'
                shown = '%s (%r)' % (w, out.strip()[:24])
            odd.setdefault((place, what), []).append(shown)
    print('%d programs, %d words, %d places' % (n, len(words), len(PLACES)))
    print('places where every word is its own text, in silence: ' + ', '.join(p for p in PLACES if expect(p, 'k') is not None and not any(k[0] == p for k in odd)))
    for (place, what), ws in sorted(odd.items()):
        print('%-14s %s (%d words)\n      %s' % (place, what, len(ws), ' '.join(ws) if len(ws) < 60 else ' '.join(ws[:25]) + ' ...'))


main()
