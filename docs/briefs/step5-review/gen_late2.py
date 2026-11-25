#!/usr/bin/env python3
"""gen_late2.py [PART/OF]: every operator and builtin with a left operand made from
$x in each form and a later operand that changes $x in each way, in four
contexts (say, $y = ..., $x = ..., my $w = ...). Programs with a finding
already made (a `.` chain; `.=` of an assigned concat) are counted and skipped."""
import sys, itertools, collections
import model, harness
from model import lit

x, y = ('var', 'x'), ('var', 'y')
LEFT = {
 '$x': x, '($x)': ('paren', x), '+$x': ('uplus', x), '+($x)': ('uplus', ('paren', x)),
 '($x = 7)': ('asg', '=', x, lit('7')), '($x += 1)': ('asg', '+=', x, lit('1')), '($x .= "0")': ('asg', '.=', x, lit('"0"')),
 '(++$x)': ('pre', '++', 'x'), '(--$x)': ('pre', '--', 'x'),
 '($x || 0)': ('log', '||', x, lit('0')), '($x && $x)': ('log', '&&', x, x), '($x // 0)': ('log', '//', x, lit('0')),
 '(0 || $x)': ('log', '||', lit('0'), x), '($y or $x)': ('log', 'or', y, x),
 '($y ? $x : 0)': ('tern', y, x, lit('0')), '($y ? 0 : $x)': ('tern', y, lit('0'), x),
 '($x ||= 4)': ('asg', '||=', x, lit('4')), '($x //= 4)': ('asg', '//=', x, lit('4')), '($x &&= $x)': ('asg', '&&=', x, x),
 '($x = $x)': ('asg', '=', x, x), '($y = $x)': ('asg', '=', y, x),
 '($x++)': ('post', '++', 'x'), '($x--)': ('post', '--', 'x'),
 '-$x': ('neg', x), '!$x': ('not', x), '($x . "")': ('bin', '.', x, lit('""')), '($x + 0)': ('bin', '+', x, lit('0')),
 '($x x 1)': ('bin', 'x', x, lit('1')), 'length($x)': ('fn1', 'length', x), 'defined($x)': ('fn1', 'defined', x),
 '($x == 3)': ('bin', '==', x, lit('3')), '($x lt "b")': ('bin', 'lt', x, lit('"b"')), '($x * 1)': ('bin', '*', x, lit('1')),
 'substr($x, 0)': ('fn', 'substr', [x, lit('0')]), '(($x))': ('paren', ('paren', x)),
 '($x ? $x : $x)': ('tern', x, x, x), '(($x || 0) || 0)': ('log', '||', ('log', '||', x, lit('0')), lit('0')),
 '(+(++$x))': ('uplus', ('pre', '++', 'x')), '(($x = 7) || 0)': ('log', '||', ('asg', '=', x, lit('7')), lit('0')),
}
RIGHT = {
 '($x = 5)': ('asg', '=', x, lit('5')), '($x = "q")': ('asg', '=', x, lit('"q"')), '($x += 2)': ('asg', '+=', x, lit('2')),
 '($x++)': ('post', '++', 'x'), '(++$x)': ('pre', '++', 'x'), '($x--)': ('post', '--', 'x'), '(--$x)': ('pre', '--', 'x'),
 '($x .= "1")': ('asg', '.=', x, lit('"1"')), '($x ||= 9)': ('asg', '||=', x, lit('9')), '($x x= 2)': ('asg', 'x=', x, lit('2')),
 '($x = $y)': ('asg', '=', x, y), '($x *= 2)': ('asg', '*=', x, lit('2')), '($x -= 1)': ('asg', '-=', x, lit('1')),
 '($x **= 2)': ('asg', '**=', x, lit('2')), '($x /= 2)': ('asg', '/=', x, lit('2')), '($x %= 2)': ('asg', '%=', x, lit('2')),
 '($x //= 1)': ('asg', '//=', x, lit('1')), '($x &&= 0)': ('asg', '&&=', x, lit('0')), '($x = (undef))': ('asg', '=', x, lit('undef')),
 '(($x = 5) + 1)': ('bin', '+', ('asg', '=', x, lit('5')), lit('1')), '-($x = 5)': ('neg', ('asg', '=', x, lit('5'))),
 '(1 && ($x = 5))': ('log', '&&', lit('1'), ('asg', '=', x, lit('5'))),
}
BIN = ['+', '-', '*', '/', '%', '**', '.', 'x', '==', '!=', '<', '>', '<=', '>=', '<=>', 'eq', 'ne', 'lt', 'gt', 'le', 'ge', 'cmp', 'xor']
LOG = ['&&', '||', '//', 'and', 'or']
OPASG = ['+=', '-=', '*=', '/=', '%=', '**=', '.=', 'x=', '||=', '&&=', '//=']
INITS = [('3', '1'), ('"ab"', '0'), (None, '"2"'), ('1.5', '1'), ('"2"', None), ('0', '7'), ('true', '"b"')]


def exprs(L, R):
    for op in BIN: yield ('bin', op, L, R)
    for op in LOG: yield ('log', op, L, R)
    yield ('tern', L, R, lit('"f"'))
    yield ('tern', L, lit('"t"'), R)
    yield ('tern', lit('1'), L, R)
    yield ('bin', '+', ('tern', lit('1'), L, lit('0')), R)
    yield ('fn', 'substr', [L, R])
    yield ('fn', 'substr', [lit('"abcdefghij"'), L, R])
    yield ('fn', 'substr', [L, lit('0'), R])
    yield ('fn', 'index', [L, lit('"1"'), R])
    yield ('fn', 'index', [lit('"abc2abc5"'), L, R])
    yield ('bin', '+', ('bin', '+', L, lit('0')), R)
    yield ('bin', '+', L, ('bin', '+', R, L))
    yield ('bin', '.', L, ('bin', '.', R, L))
    yield ('bin', '+', ('bin', '+', L, R), L)
    yield ('bin', '.', ('bin', '.', L, R), L)        # a chain: skipped, and counted


def contexts(e, L):
    yield [('say', e)]
    yield [('expr', ('asg', '=', y, e)), ('say', ('fn1', 'defined', y)), ('say', ('log', '//', y, lit('"u"')))]
    yield [('expr', ('asg', '=', x, e))]
    yield [('my', 'w', e), ('say', ('log', '//', ('var', 'w'), lit('"u"')))]
    yield [('mod', ('say', lit('"t"')), 'if', e)]
    yield [('if', [(e, [('say', lit('"t"'))])], [('say', lit('"e"'))])]


def main():
    part, of = (0, 1)
    for a in sys.argv[1:]:
        if '/' in a: part, of = map(int, a.split('/'))
    t = harness.Tally('late reads, every pair, part %d of %d' % (part, of), 'late2-%d.log' % part)
    kinds = collections.Counter(); skipped = collections.Counter(); n = 0
    tail = [('say', ('log', '//', x, lit('"x undef"'))), ('say', ('log', '//', y, lit('"y undef"')))]
    progs = []
    for (ln, L), (rn, R) in itertools.product(LEFT.items(), RIGHT.items()):
        for e in exprs(L, R):
            for body in contexts(e, L):
                progs.append(body)
        # the left of an OP= when the right changes the variable
        for op in OPASG:
            progs.append([('expr', ('asg', op, x, R))])
            progs.append([('say', ('asg', op, x, R))])
            progs.append([('expr', ('asg', op, y, ('bin', '+', L, R)))])
    for i, body in enumerate(progs):
        if i % of != part: continue
        init = INITS[(i // of) % len(INITS)]
        p = [('my', 'x', None if init[0] is None else lit(init[0])), ('my', 'y', None if init[1] is None else lit(init[1]))] + body + tail
        if model.any_truth_refused(p): skipped['truth position (the proposal refuses)'] += 1; continue
        if model.any_list_refused(p): skipped['list context (T104)'] += 1; continue
        if model.has_chain(p): skipped['a chain of dots (finding)'] += 1; continue
        if model.has_append_of_assigned_concat(p): skipped['.= of an assigned concat (finding)'] += 1; continue
        v = t.check(p)
        if v: kinds[v.split(':')[0] + (' Found =' if 'Found =' in v else '')] += 1
    t.done()
    print(dict(kinds), dict(skipped))


if __name__ == '__main__':
    main()
