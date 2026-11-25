#!/usr/bin/env python3
"""spacing.py SEED COUNT: the compiler's reading of a text held to perl's, where
the blanks are. A program from the generators is printed with the fewest
brackets, cut into tokens, and joined again with nothing, a blank, two, a tab,
a newline or a comment between each two, at random. What the text then means
is for the compiler and perl to say (the model has no part: `$x x 3` joined is
another program, or none): every text the compiler accepts must print what
perl prints, perl silent. Through compiler.py, many texts to a file."""
import os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compiler, minshow, gen_late, gen_struct, gen_past

TOKEN = re.compile(r'''"[^"]*"|\$\w+|\d+\.\d+(?:e[+-]?\d+)?|\d+(?:e[+-]?\d+)?|\.\d+|\w+|\*\*=|\|\|=|&&=|//=|<=>|\*\*|\+\+|--|\|\||&&|//|==|!=|<=|>=|\+=|-=|\*=|/=|%=|\.=|\S''')
SEPS = [' '] * 10 + [''] * 7 + ['\n', '\n', '\t', '  ', ' # c\n', '\n# c\n']


def respace(text, r):
    out = []
    for line in text.split('\n'):
        toks = TOKEN.findall(line)
        if not toks: continue
        s = toks[0]
        for t in toks[1:]:
            sep = r.choice(SEPS)
            # two words, or a word and a number, with nothing between are one word: mostly keep them apart
            if sep == '' and re.match(r'\w', t) and re.search(r'\w$', s) and r.random() < 0.9: sep = ' '
            s += sep + t
        out.append(s)
    return '\n'.join(out)


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    r = random.Random(seed)
    state = {}
    items = []
    for n in range(count):
        kind = r.choice(['late', 'late', 'struct', 'past'])
        if kind == 'late': p = gen_late.program(r)
        elif kind == 'struct': p = gen_struct.program(r)
        else:
            if 'inits' not in state: state['inits'] = gen_past.inits()
            p = gen_past.program(r, state['inits'])
        if kind == 'late': p = [s for s in p if not (s[0] == 'say' and s[1][0] == 'tern' and s[1][1][0] == 'fn1')][:5] + p[-1:]
        minshow.BARE = r.random() < 0.6
        items.append(compiler.Text(n, respace(minshow.block(p, ''), r)))
    print('%d texts' % len(items), flush=True)
    done = 0
    while items:
        group, items = items[:30], items[30:]
        compiler.batch(group)
        done += 30
        if done % 1500 == 0: print('  ... %d; %d WRONG so far' % (done, len(compiler.wrong)), flush=True)
    compiler.report('spacing-%d' % seed)


if __name__ == '__main__':
    main()
