#!/usr/bin/env python3
"""t/070 to t/089: functions (D31 to D34) and what they lean on: the 63-bit
range (D4), faults (D6, D11, D13), budgets (D21 to D24) and left-to-right
order (D25).

070 call                 definitions and calls, one calling the other
071 no-params            a function of no parameters
072 eight-params         a function of eight parameters
073 any-order            a call before the definition, and a function
                         calling one defined after it (D31)
074 mutual-tail          even/odd through 100,001 tail calls (D33)
075 fact-20              non-tail recursion with a value: 20! fits 63 bits
076 fact-21              21! doesn't: fault overflow (D4)
077 tail-loop            a tail-recursive loop of 100,000 iterations, past
                         D34's 10,000: tail calls add no depth (D33)
078 depth-edge           (sum 9999): 10,000 calls in progress, runs (D34)
079 depth-past           (sum 10000): the 10,001st faults stack (D34)
080 within-not-tail      a loop through a within, 10,001 deep: stack, where
                         a plain tail loop wouldn't (D33)
081 within-not-tail-edge the same at 10,000 deep: runs
082 budget-edge          a call is one operation (D32): a budget of exactly
                         what a program spends, with operators in a call's
                         arguments and a call inside an argument
083 budget-short         one less: budget spent
084 arg-order            two faulting arguments: the first is reported (D25)
085 charge-before-depth  a budget that runs out at the call that would also
                         be too deep: budget spent, the charge comes first
                         (D32, D34)
086 depth-after-charge   one more operation of budget: the same call is
                         charged and then faults stack (D34)
087 charge-before-body   (within 1 (g)): the call spends the one operation,
                         the body's first operation is refused (D32)
088 tail-if              ifs nested in tail position, collatz by tail
                         calls (D33)
089 fault-in-function    an if test that isn't a boolean, inside a function
                         (D13)

The model is a small evaluator of the language, from the decisions, with an
explicit stack and no Python recursion on the program, so a call 10,000 deep
or a loop 100,000 long is a loop here too. It parses the program text each
test writes. What it takes from the decisions:

- A program is definitions then one expression (D31). A call evaluates its
  arguments left to right, is charged as one operation, is checked for depth,
  then evaluates the body (D32).
- Depth is the number of non-tail calls in progress (D34); the program's
  expression is depth 0 and a call from it makes depth 1. A call is a tail
  call when the continuation after it is its caller's return and nothing
  else: so an `if`'s branches in tail position are, and an operator's
  operand, a call's argument, an `if`'s test and a `within`'s body or budget
  are not, since each leaves something to do afterwards (D33). A tail call
  replaces its caller's frame, so depth doesn't move; a call from the
  program's own expression has no caller's frame to replace and counts as
  depth 1 (D34's "a call from it makes depth 1").
- An operation is charged when applied, after its operands (or a call's
  arguments), before any check of its own (D22, D32). The budget is kept as
  `spent` and a `limit`, the lowest count in force (D23, D27's idea, which
  is only a way of keeping D23's rule); a within's end puts the outer limit
  back.
- Integers outside the 63-bit range fault overflow, booleans in arithmetic
  fault not an integer, division truncates (D4, D5, D11).

Each count the tests turn on is also worked out by hand in an assert next to
it (the closed forms are in the comments), so the evaluator is checked
against arithmetic and not only against itself.

Every command that regenerates a file is listed, one a line, so that
t/checks.py can run them all and diff (`make checks`), and `make models`
can write them:

    python3 t/models/fn.py --program 070 > t/070-call.lang
    python3 t/models/fn.py 070 > t/070-call.expected
    python3 t/models/fn.py --program 071 > t/071-no-params.lang
    python3 t/models/fn.py 071 > t/071-no-params.expected
    python3 t/models/fn.py --program 072 > t/072-eight-params.lang
    python3 t/models/fn.py 072 > t/072-eight-params.expected
    python3 t/models/fn.py --program 073 > t/073-any-order.lang
    python3 t/models/fn.py 073 > t/073-any-order.expected
    python3 t/models/fn.py --program 074 > t/074-mutual-tail.lang
    python3 t/models/fn.py 074 > t/074-mutual-tail.expected
    python3 t/models/fn.py --program 075 > t/075-fact-20.lang
    python3 t/models/fn.py 075 > t/075-fact-20.expected
    python3 t/models/fn.py --program 076 > t/076-fact-21.lang
    python3 t/models/fn.py 076 > t/076-fact-21.expected
    python3 t/models/fn.py --program 077 > t/077-tail-loop.lang
    python3 t/models/fn.py 077 > t/077-tail-loop.expected
    python3 t/models/fn.py --program 078 > t/078-depth-edge.lang
    python3 t/models/fn.py 078 > t/078-depth-edge.expected
    python3 t/models/fn.py --program 079 > t/079-depth-past.lang
    python3 t/models/fn.py 079 > t/079-depth-past.expected
    python3 t/models/fn.py --program 080 > t/080-within-not-tail.lang
    python3 t/models/fn.py 080 > t/080-within-not-tail.expected
    python3 t/models/fn.py --program 081 > t/081-within-not-tail-edge.lang
    python3 t/models/fn.py 081 > t/081-within-not-tail-edge.expected
    python3 t/models/fn.py --program 082 > t/082-budget-edge.lang
    python3 t/models/fn.py 082 > t/082-budget-edge.expected
    python3 t/models/fn.py --program 083 > t/083-budget-short.lang
    python3 t/models/fn.py 083 > t/083-budget-short.expected
    python3 t/models/fn.py --program 084 > t/084-arg-order.lang
    python3 t/models/fn.py 084 > t/084-arg-order.expected
    python3 t/models/fn.py --program 085 > t/085-charge-before-depth.lang
    python3 t/models/fn.py 085 > t/085-charge-before-depth.expected
    python3 t/models/fn.py --program 086 > t/086-depth-after-charge.lang
    python3 t/models/fn.py 086 > t/086-depth-after-charge.expected
    python3 t/models/fn.py --program 087 > t/087-charge-before-body.lang
    python3 t/models/fn.py 087 > t/087-charge-before-body.expected
    python3 t/models/fn.py --program 088 > t/088-tail-if.lang
    python3 t/models/fn.py 088 > t/088-tail-if.expected
    python3 t/models/fn.py --program 089 > t/089-fault-in-function.lang
    python3 t/models/fn.py 089 > t/089-fault-in-function.expected
"""

import math
import sys

MIN, MAX = -(2**62), 2**62 - 1
DEPTH_LIMIT = 10000  # D34
INF = float('inf')

class Fault(Exception):
    """A fault; args[0] is its message."""

# ---- reader: tokens to nested lists, with an explicit stack ----

def read(text):
    toks = []
    for line in text.split('\n'):
        line = line.split(';', 1)[0]
        toks += line.replace('(', ' ( ').replace(')', ' ) ').split()
    stack, out = [], []
    for t in toks:
        if t == '(':
            stack.append(out)
            out = []
        elif t == ')':
            done, out = out, stack.pop()
            out.append(done)
        else:
            out.append(t)
    assert not stack
    return out

def atom(t):
    if t == '#true':
        return ('lit', True)
    if t == '#false':
        return ('lit', False)
    try:
        v = int(t)
    except ValueError:
        return ('name', t)
    assert MIN <= v <= MAX
    return ('lit', v)

BINOPS = ['+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!=']

def analyze(x, params, funcs):
    """A form as a tuple. Shallow source, so this one recurses."""
    if isinstance(x, str):
        k = atom(x)
        if k[0] == 'name':
            assert x in params, x
            return ('param', x)
        return k
    head, args = x[0], x[1:]
    if head in BINOPS:
        assert len(args) == 2
        return ('op', head, analyze(args[0], params, funcs), analyze(args[1], params, funcs))
    if head == 'if':
        return ('if',) + tuple(analyze(a, params, funcs) for a in args)
    if head == 'within':
        return ('within',) + tuple(analyze(a, params, funcs) for a in args)
    assert head in funcs and len(args) == funcs[head], head
    return ('call', head, tuple(analyze(a, params, funcs) for a in args))

def parse(text):
    forms = read(text)
    defs, funcs = {}, {}
    for f in forms[:-1]:
        assert f[0] == 'def'
        funcs[f[1][0]] = len(f[1]) - 1
    for f in forms[:-1]:
        name, params = f[1][0], f[1][1:]
        defs[name] = (params, analyze(f[2], params, funcs))
    return defs, analyze(forms[-1], [], funcs)

# ---- the evaluator ----

def tdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q

def apply_op(op, a, b):
    if op in ('==', '!='):
        same = type(a) is type(b) and a == b
        return same if op == '==' else not same
    if isinstance(a, bool) or isinstance(b, bool):
        raise Fault('not an integer')
    if op in '/%' and b == 0:
        raise Fault('division by zero')
    r = {'+': lambda: a + b, '-': lambda: a - b, '*': lambda: a * b,
         '/': lambda: tdiv(a, b), '%': lambda: a - tdiv(a, b) * b,
         '<': lambda: a < b, '<=': lambda: a <= b,
         '>': lambda: a > b, '>=': lambda: a >= b}[op]()
    if not isinstance(r, bool) and not MIN <= r <= MAX:
        raise Fault('overflow')
    return r

def run(text):
    """(outcome, spent, deepest): outcome is ('value', v) or ('fault', msg);
    spent is the operations charged, a faulting charge not counted;
    deepest the greatest depth entered."""
    defs, main = parse(text)
    st = {'spent': 0, 'limit': INF, 'depth': 0, 'deepest': 0}
    stack = [('halt',)]
    mode, ctl, env = 'eval', main, {}

    def charge():
        if st['spent'] == st['limit']:
            raise Fault('budget spent')
        st['spent'] += 1

    try:
        while True:
            if mode == 'eval':
                kind = ctl[0]
                if kind == 'lit':
                    mode, val = 'ret', ctl[1]
                elif kind == 'param':
                    mode, val = 'ret', env[ctl[1]]
                elif kind == 'op':
                    stack.append(('arg1', ctl[1], ctl[3], env))
                    ctl = ctl[2]
                elif kind == 'if':
                    stack.append(('if', ctl[2], ctl[3], env))
                    ctl = ctl[1]
                elif kind == 'within':
                    stack.append(('within', ctl[2], env))
                    ctl = ctl[1]
                else:  # call
                    _, name, args = ctl
                    if args:
                        stack.append(('args', name, args, 1, [], env))
                        ctl = args[0]
                    else:
                        ctl, env = enter(name, [], defs, stack, st, charge)
                continue
            top = stack.pop()
            k = top[0]
            if k == 'halt':
                return ('value', val), st['spent'], st['deepest']
            if k == 'ret':
                st['depth'] -= 1
            elif k == 'arg1':
                stack.append(('arg2', top[1], val))
                mode, ctl, env = 'eval', top[2], top[3]
            elif k == 'arg2':
                charge()
                val = apply_op(top[1], top[2], val)
            elif k == 'if':
                if not isinstance(val, bool):
                    raise Fault('not a boolean')
                mode, ctl, env = 'eval', top[1] if val else top[2], top[3]
            elif k == 'within':
                if isinstance(val, bool):
                    raise Fault('not an integer')
                if val < 0:
                    raise Fault('bad budget')
                stack.append(('wend', st['limit']))
                st['limit'] = min(st['limit'], st['spent'] + val)
                mode, ctl, env = 'eval', top[1], top[2]
            elif k == 'wend':
                st['limit'] = top[1]
            elif k == 'args':
                _, name, args, i, vals, aenv = top
                vals = vals + [val]
                if i < len(args):
                    stack.append(('args', name, args, i + 1, vals, aenv))
                    mode, ctl, env = 'eval', args[i], aenv
                else:
                    ctl, env = enter(name, vals, defs, stack, st, charge)
                    mode = 'eval'
    except Fault as f:
        return ('fault', f.args[0]), st['spent'], st['deepest']

def enter(name, vals, defs, stack, st, charge):
    """A call whose arguments are done: charge, then depth, then the body."""
    charge()
    if stack[-1][0] == 'ret':
        pass  # a tail call replaces its caller's frame (D33)
    else:
        if st['depth'] + 1 > DEPTH_LIMIT:
            raise Fault('stack')
        st['depth'] += 1
        st['deepest'] = max(st['deepest'], st['depth'])
        stack.append(('ret',))
    params, body = defs[name]
    return body, dict(zip(params, vals))

# ---- the tests ----

SUM = '(def (sum n) (if (== n 0) 0 (+ n (sum (- n 1)))))'
LOOP_IN_WITHIN = '(def (loop n) (within 100000000 (if (== n 0) 0 (loop (- n 1)))))'
G = '(def (g) (/ 1 0))'

def fact_prog(n):
    return ['(def (fact n) (if (== n 0) 1 (* n (fact (- n 1)))))', f'(fact {n})']

def tail_loop(n):
    return ['(def (loop n acc) (if (== n 0) acc (loop (- n 1) (+ acc n))))', f'(loop {n} 0)']

def budget_prog(n):
    return ['(def (f x y) (+ x y))', f'(within {n} (f (+ 1 2) (* 3 (f 1 1))))']

def sum_budget_prog(n):
    return [SUM, f'(within {n} (sum 10000))']

def collatz_steps(n):
    s = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        s += 1
    return s

def cases():
    """number -> (name, comment lines, program lines)."""
    c = {}
    c['070'] = ('call', ['Definitions and calls (D31): a function calling another.'],
        ['(def (sq x) (* x x))',
         '(def (hyp2 a b) (+ (sq a) (sq b)))',
         '(+ (hyp2 3 4) (sq 10))'])
    c['071'] = ('no-params', ['A function of no parameters (D31).'],
        ['(def (answer) (* 6 7))', '(+ (answer) (answer))'])
    c['072'] = ('eight-params', ['A function of eight parameters, each weighted so a swap shows (D31).'],
        ['(def (mix a b c d e f g h)',
         '    (+ (+ (+ (* 1 a) (* 2 b)) (+ (* 3 c) (* 4 d)))',
         '       (+ (+ (* 5 e) (* 6 f)) (+ (* 7 g) (* 8 h)))))',
         '(mix 1 -2 3 -4 5 -6 7 -8)'])
    c['073'] = ('any-order', ['Every definition sees every other, whatever the order (D31).'],
        ['(def (twice-inc x) (inc (inc x)))',
         '(def (top) (+ (twice-inc 10) (inc 0)))',
         '(def (inc x) (+ x 1))',
         '(top)'])
    c['074'] = ('mutual-tail', ['Mutual recursion through tail calls (D31, D33): 100,001 calls, depth 1.'],
        ['(def (even n) (if (== n 0) #true (odd (- n 1))))',
         '(def (odd n) (if (== n 0) #false (even (- n 1))))',
         '(even 100001)'])
    c['075'] = ('fact-20', ['Non-tail recursion with a value (D34): 20! fits 63 bits (D4).'], fact_prog(20))
    c['076'] = ('fact-21', ['21! is past the range: fault overflow (D4), at the multiplication.'], fact_prog(21))
    c['077'] = ('tail-loop', ['A tail-recursive loop of 100,000 iterations (D33): tail calls add no depth,',
                              '; and the depth limit is 10,000 (D34).'], tail_loop(100000))
    c['078'] = ('depth-edge', ['(sum 9999) is 10,000 calls in progress: it runs (D34).'], [SUM, '(sum 9999)'])
    c['079'] = ('depth-past', ['(sum 10000) needs a 10,001st call in progress: fault stack (D34).'], [SUM, '(sum 10000)'])
    c['080'] = ('within-not-tail', ['A within\'s body is not tail position (D33): the loop below is 10,001 deep',
                                    '; at n=10000, and faults stack where a plain tail loop would not.'],
        [LOOP_IN_WITHIN, '(loop 10000)'])
    c['081'] = ('within-not-tail-edge', ['The same loop one iteration shorter is 10,000 deep: it runs (D33, D34).'],
        [LOOP_IN_WITHIN, '(loop 9999)'])
    ops_total = 6  # worked out below and asserted
    c['082'] = ('budget-edge', ['A call is one operation (D32). Operations here: + 1, (f 1 1) the call 1 and',
                                '; its body\'s + 1, * 1, the outer call 1 and its body\'s + 1 = 6. A budget',
                                '; of exactly 6 runs.'], budget_prog(ops_total))
    c['083'] = ('budget-short', ['The same program with a budget of 5: the last + is refused (D22, D32).'], budget_prog(ops_total - 1))
    c['084'] = ('arg-order', ['Arguments left to right (D25, D32): both faults are possible, the first is',
                              '; reported.'],
        ['(def (f a b) (+ a b))', '(f (/ 1 0) (+ #true 1))'])
    # sum 10000 reaches the 10,001st call after 10,000 calls, 10,000 == and
    # 10,000 -: 30,000 operations; that call's charge is the 30,001st.
    c['085'] = ('charge-before-depth', ['(sum 10000) is 30,000 operations before the call that is too deep (D34).',
                                        '; A budget of 30000 is spent at that call\'s charge, which comes first',
                                        '; (D32): budget spent, not stack.'], sum_budget_prog(30000))
    c['086'] = ('depth-after-charge', ['With 30001 the charge succeeds and the depth check fails: stack (D32, D34).'],
        sum_budget_prog(30001))
    c['087'] = ('charge-before-body', ['The call spends the one operation (D32), then the body\'s / is refused,',
                                       '; before its own check (D22): budget spent, not division by zero.'],
        [G, '(within 1 (g))'])
    c['088'] = ('tail-if', ['An if in tail position, nested, calling in both branches (D33): the Collatz',
                            '; steps of 27 (111) by tail calls.'],
        ['(def (collatz n steps)',
         '    (if (== n 1)',
         '        steps',
         '        (if (== (% n 2) 0)',
         '            (collatz (/ n 2) (+ steps 1))',
         '            (collatz (+ (* 3 n) 1) (+ steps 1)))))',
         '(collatz 27 0)'])
    c['089'] = ('fault-in-function', ['An if test that is not a boolean, inside a function (D13).'],
        ['(def (pick x) (if x 1 2))', '(+ (pick #true) (pick 5))'])
    return c

def program_text(test):
    name, comment, lines = cases()[test]
    head = [f'; {comment[0]}'] + [c if c.startswith(';') else '; ' + c for c in comment[1:]]
    head.append('; Expected output from t/models/fn.py, a model of D31 to D34.')
    return '\n'.join(head + lines) + '\n'

def outcome(test):
    return run('\n'.join(cases()[test][2]))

def check_by_hand():
    """The counts and values the tests turn on, against arithmetic."""
    o = lambda t: outcome(t)
    assert o('070')[0] == ('value', (9 + 16) + 100)
    assert o('071')[0] == ('value', 84)
    assert o('072')[0] == ('value', sum(i * v for i, v in zip(range(1, 9), [1, -2, 3, -4, 5, -6, 7, -8])))
    assert o('073')[0] == ('value', 12 + 1)
    r = o('074')
    assert r[0] == ('value', 100001 % 2 == 0) and r[2] == 1
    assert o('075')[0] == ('value', math.factorial(20)) and math.factorial(20) <= MAX
    assert math.factorial(21) > MAX and o('076')[0] == ('fault', 'overflow')
    r = o('077')
    assert r[0] == ('value', 100000 * 100001 // 2) and r[2] == 1
    assert r[1] == 1 + 100000 * 4 + 1  # the call; per iteration ==, -, + and the call; the last ==
    r = o('078')
    assert r[0] == ('value', 9999 * 10000 // 2) and r[2] == 10000
    assert o('079')[0] == ('fault', 'stack')
    assert o('080')[0] == ('fault', 'stack')
    assert o('081')[0] == ('value', 0) and o('081')[2] == 10000
    # 082: 1 (+) + 2 (inner call, its +) + 1 (*) + 2 (outer call, its +)
    full = run('\n'.join(budget_prog('100')))
    assert full[1] == 6 and full[0] == ('value', 3 + 3 * 2)
    assert o('082')[0] == ('value', 9) and o('083')[0] == ('fault', 'budget spent')
    assert o('084')[0] == ('fault', 'division by zero')
    unbounded = run(SUM + '\n(sum 10000)')
    assert unbounded[0] == ('fault', 'stack') and unbounded[1] == 30000 + 1
    assert o('085')[0] == ('fault', 'budget spent') and o('086')[0] == ('fault', 'stack')
    assert o('087')[0] == ('fault', 'budget spent')
    assert run(G + '\n(within 2 (g))')[0] == ('fault', 'division by zero')
    assert o('088')[0] == ('value', collatz_steps(27)) == ('value', 111)
    assert o('089')[0] == ('fault', 'not a boolean')

def expected(test):
    kind, v = outcome(test)[0]
    if kind == 'fault':
        return f'fault: {v}\nexit: 1\n'
    return ('#true' if v is True else '#false' if v is False else str(v)) + '\n'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--program']
    if not args:
        sys.exit(__doc__)
    check_by_hand()
    test = args[0]
    sys.stdout.write(program_text(test) if '--program' in sys.argv else expected(test))
