#!/usr/bin/env python3
"""handles.py: the file-handle refusal as the compiler has it, held to perl.

A variable first after say or print (and after `say(`, `say((`, `say(+`), a
blank of each kind, then each operator of the language with and without a
blank before its operand, and each operand; and the same with the variable
first inside `substr(` and `index(`, where perl looks for a file handle too.
Every text the compiler accepts must print what perl prints, perl silent
(compiler.py does the comparing, many texts to a file)."""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compiler

OPS = ['+', '-', '*', '/', '%', '**', '.', 'x', '==', '!=', '<', '>', '<=', '>=', '<=>', 'eq', 'ne', 'lt', 'gt', 'le', 'ge', 'cmp',
       '&&', '||', '//', '=', '+=', '-=', '*=', '/=', '%=', '**=', '.=', 'x=', '||=', '&&=', '//=']
OPERANDS = ['2', '$y', '-2', '+2', '.5', '"2"', "'2'", '(2)', 'true', '-$y', '!$y', '++$y', '--$y', '2.5', 'length("ab")', '$y++', 'undef']
BLANKS = [' ', '\t', '\n', '  ', ' # c\n', '\n# c\n  ']
SHAPES = [('say ', ';'), ('say(', ');'), ('print ', ';'), ('say((', '));'), ('say(+', ');'), ('say(substr(', ', 0));'), ('say(index(', ', "2"));'),
          ('say(substr((', '), 0));'), ('say(length(', '));'), ('say(1 + substr(', ', 0, 1));'), ('say ', ' if $y;'), ('say(', ') unless $y;')]


def tails():
    for op, operand, gap in itertools.product(OPS, OPERANDS, ['', ' ']):
        yield op + gap + operand
    for t in ['? 1 : 2', '?1 : 2', '?1:2', '? $y : 2', '?$y : 2', '?-1 : 2', '?"a" : "b"', '++', '--', 'x 2 . "|"',
              '. "a" . "b"', '- 1 - 1', '-1 - 1', '+ +1', '* 2 ** 2', '. .2', 'and 1', 'or 1', 'xor 1', 'x2', 'lt2', 'eq"6"', "eq'6'", 'x(2)', 'x=2',
              '<true', '< true', '*true', '%true', '&&true', '<$y', '*$y', '%$y', '/$y', '/ $y', '//$y', '<=$y', '-=1', '+=1', '- -1', '-\n1', '+\t1']:
        yield t


def main():
    # handles.py [shapes=0,2,4] [quick] [PART/OF]: some of the shapes; fewer operands and blanks; a slice
    global OPERANDS, BLANKS
    shapes = SHAPES
    part, of = 0, 1
    for a in sys.argv[1:]:
        if '/' in a: part, of = map(int, a.split('/'))
        if a.startswith('shapes='): shapes = [SHAPES[int(n)] for n in a[7:].split(',')]
        if a == 'quick':
            OPERANDS = ['2', '$y', '-2', '+2', '.5', '"2"', '(2)', 'true', '++$y']
            BLANKS = [' ', '\n', ' # c\n']
    items = []
    for tail in tails():
        for blank in BLANKS:
            for head, end in shapes:
                items.append(compiler.Text(len(items), 'my $x = 6;\nmy $y = 2;\n%s$x%s%s%s' % (head, blank, tail, end)))
    items = [it for n, it in enumerate(items) if n % of == part]
    print('%d texts' % len(items), flush=True)
    while items:
        group, items = items[:60], items[60:]
        compiler.batch(group)
    compiler.report('handles')


if __name__ == '__main__':
    main()
