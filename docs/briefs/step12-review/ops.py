#!/usr/bin/env python3
"""T220 again, for all four named unary operators of the step: every infix
operator of the language after `exists $h{a}`, `delete $h{a}`, `keys %h`,
`values %h` with no brackets. For each: does perl compile it, and is it
`(OP ARG) infix 3` (the operator binds looser), or something else?

    python3 docs/briefs/step12-review/ops.py
"""
from common import perl

INFIX = ['+', '-', '*', '/', '%', '**', '.', 'x', '==', '!=', '<', '<=', '>', '>=', '<=>', 'eq', 'ne', 'lt', 'le', 'gt', 'ge',
         'cmp', '&&', '||', '//', '? 5 :', 'and', 'or', 'xor', '..', ',', '=>', '=', '+=', '.=', '||=', '//=', '&&=', '++', '--', '[0]', '{a}', '(', 'if 1', 'x 2 .', '=~', '<<', '&', '|', 'isa']
HEAD = 'my %h = (a => 4, b => 6); my @l; '
FORMS = {
    'exists $h{a}': 'exists($h{a})',
    'delete $h{a}': 'delete($h{a})',
    'keys %h': 'keys(%h)',
    'values %h': 'values(%h)',
    'exists $h{a}{b}': None,
    'delete @h{"a", "b"}': 'delete(@h{"a", "b"})',
    'delete local $h{a}': None,
    'exists &f': None,
    'keys my %g': None,
}


def run(expr):
    out, err, code = perl(HEAD + '@l = (' + expr + '); say join "|", map { defined($_) ? $_ : "undef" } @l; say join ",", map { "$_=$h{$_}" } sort keys %h;')
    return out, err, code


def main():
    n = 0
    for bare, bracketed in FORMS.items():
        print('== ' + bare)
        for op in INFIX:
            tail = ' 3' if op not in ('++', '--', '[0]', '{a}', '(', 'if 1') else ''
            if op == '(':
                tail = '3)'
            n += 1
            got = run(bare + ' ' + op + tail)
            if bracketed is None:
                loose = None
            else:
                n += 1
                loose = run('(' + bracketed + ') ' + op + tail)
            if got[2] != 0 and not got[0]:
                verdict = 'perl stops: ' + got[1].strip().split('\n')[0][:100]
            elif got == loose:
                verdict = 'looser, in silence' if not got[1] else 'looser; WARNS ' + got[1].strip().split('\n')[0][:80]
            else:
                verdict = 'ANOTHER WAY: %r %s' % (got[0], got[1].strip()[:100]) + (' (bracketed: %r)' % (loose[0],) if loose else '')
            print('   %-8s %s' % (op, verdict))
    print('%d programs' % n)


main()
