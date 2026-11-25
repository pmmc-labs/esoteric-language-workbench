#!/usr/bin/env python3
"""gen_fh.py [--break]: the file-handle refusal, held to perl mechanically. For a
variable first after say/print (and after say( with brackets), a blank of each
kind, then each operator of the language spelled with and without a blank
before its operand: if the proposal's rule does not refuse the text, perl must
print what the same expression prints when it is assigned to a variable first
(where no file handle can be meant). --break drops the rule's `.` clause."""
import os
import itertools, sys, re
import harness

WORDS = {'x', 'eq', 'ne', 'gt', 'lt', 'ge', 'le', 'cmp', 'if', 'unless', 'and', 'or', 'xor'}
BREAK = '--break' in sys.argv


def refused(s):
    """The proposal's rule, on the text after the blanks that follow the variable."""
    if not s: return False
    c, d = s[0], s[1:2]
    if c in '-+' and d and not d.isspace() and d != '=': return True
    if c == '.' and d.isdigit() and not BREAK: return True
    if c in '*%<&' and (d.isalpha() or d == '_'): return True
    if c == '/' and d and not d.isspace() and d not in '=/': return True
    if s.startswith('<<') and s[2:3] and not s[2:3].isspace() and s[2:3] != '=': return True
    if c in '$@"\'`': return True
    if c.isdigit(): return True
    if c.isalpha() or c == '_':
        return re.match(r'\w+', s).group(0) not in WORDS
    return False


OPS = ['+', '-', '*', '/', '%', '**', '.', 'x', '==', '!=', '<', '>', '<=', '>=', '<=>', 'eq', 'ne', 'lt', 'gt', 'le', 'ge', 'cmp',
       '&&', '||', '//', '=', '+=', '-=', '*=', '/=', '%=', '**=', '.=', 'x=', '||=', '&&=', '//=']
OPERANDS = ['2', '$y', '-2', '+2', '.5', '"2"', "'2'", '(2)', 'true', '-$y', '!$y', '++$y', '--$y', '2.5', 'length("ab")', '$y++']
BLANKS = [' ', '\t', '\n', '  ', ' \n ']
SHAPES = [('say ', ';'), ('say(', ');'), ('print ', ';'), ('say((', '));'), ('say(+', ');')]


def tails():
    for op, operand, gap in itertools.product(OPS, OPERANDS, ['', ' ']):
        if op in ('x', 'eq', 'ne', 'lt', 'gt', 'le', 'ge', 'cmp', 'x=') and gap == '' and operand[0] not in '("\'$-+!.':
            continue                                   # `x2`, `eqtrue`: another word
        if op == 'x' and gap == '' and operand[0] != '(': continue      # the built language wants a blank or a bracket after x
        if op.endswith('=') and op not in ('==', '!=', '<=', '>=') and operand in ('++$y', '--$y', '$y++'): pass
        yield op + gap + operand
    for t in ['? 1 : 2', '?1 : 2', '?1:2', '? $y : 2', '?$y : 2', '?-1 : 2', '?"a" : "b"', '++', '--', 'if $y', 'unless $y', 'if 1', 'x 2 . "|"',
              '. "a" . "b"', '- 1 - 1', '-1 - 1', '+ +1', '* 2 ** 2', '*2', '%2', '<2', '>2', '/2', '/ 2', '// 2', '//2', '&& 2', '&&2', '.2', '. 2', '. .2']:
        yield t


def main():
    n = bad = refusedn = 0
    log = open(os.path.join(harness.HERE, 'fh.log'), 'w')
    for tail in tails():
        for blank in BLANKS:
            for head, end in SHAPES:
                text = '$x' + blank + tail
                modifier = tail.startswith(('if ', 'unless '))
                prog = 'use v5.42;\nmy $x = 6;\nmy $y = 2;\n%s%s%s\n' % (head, text, end)
                n += 1
                if refused(tail): refusedn += 1; continue
                if modifier:
                    if head != 'say ' and head != 'print ': continue
                    safe = 'use v5.42;\nmy $x = 6;\nmy $y = 2;\n%s($x) %s;\n' % (head.strip(), tail)
                else:
                    safe = 'use v5.42;\nmy $x = 6;\nmy $y = 2;\nmy $r = $x %s;\n%s$r%s\n' % (tail, head.rstrip('(+').rstrip() + '(', ');')
                sout, serr, sexit = harness.perl(safe)
                if serr or sexit: continue             # not a program of the language either way (a fault, or refused)
                pout, perr, pexit = harness.perl(prog)
                if (pout, perr, pexit) != (sout, b'', 0):
                    bad += 1
                    log.write('----\n%s## perl: exit %d stdout %r stderr %r; the same expression assigned first prints %r\n' % (prog, pexit, pout, perr, sout))
                    log.flush()
                    if bad <= 6: print('----\n%s## perl: exit %d stdout %r stderr %r; assigned first: %r' % (prog, pexit, pout, perr[:200], sout))
    print('file-handle rule: %d texts, %d refused by the rule, %d not refused where perl differs' % (n, refusedn, bad))


if __name__ == '__main__':
    main()
