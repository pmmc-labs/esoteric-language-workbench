#!/usr/bin/env python3
"""The referee: an evaluator of the calculator from its decisions (D3 to
D7, D11 to D25, D31 to D34), on Python's unbounded integers, with the
63-bit range and the division and shift rules applied as the decisions
say. Written from DECISIONS.md and not from the runtime, so that it is
a second implementation, and `make checks` runs it over every golden
test and fails where the two disagree. A program it doesn't cover, or
one with an error before running (D28, D31), which no golden test is
(D7), is reported as such, exit 3, and the check skips it; the large
model extends it when a step's proposal says a referee is wanted
(docs/PROCESS.md, "The referee").

The builder of a step does not read this file: that's what makes the
referee's agreement with the builder's model worth something. The
judge runs it.

Both the reader and the evaluator are loops with a stack of their own,
not recursive functions: a program may nest thousands deep, and the
first version of this file, recursive, failed past about a thousand
where a builder's tests went deeper.

Budgets (D20 to D25) are kept the way the decisions say them, not the
way the runtime is told to (D27): a list of what each budget in force
has left, every operation charged to all of them, and refused when any
is at 0 (D23). That costs the depth of `within`s per operation, which
a referee can afford, and it makes the runtime's single limit a second
derivation rather than a copy.

Functions (D31 to D34) are frames on the same stack: a call waits on
its body as an operator waits on its operands, and the depth is a count
of the calls waiting. A tail call (D33) drops its caller's frames
before its body starts, so a loop of tail calls runs in the stack it
started with, and a call 10,000 deep is 10,000 frames of a Python list,
not of Python's own stack.

    python3 t/referee/calc.py t/010-arith.lang
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1

class Fault(Exception):
    pass

def fit(n):
    if n < MIN or n > MAX:
        raise Fault('overflow')
    return n

def need_int(v):
    if isinstance(v, bool):
        raise Fault('not an integer')
    return v

def quot(a, b):
    if b == 0:
        raise Fault('division by zero')
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q

# The quotient can overflow (MIN / -1); the remainder never can, and
# D5 puts no range check on it: (% MIN -1) is 0.
def div(a, b):
    return fit(quot(a, b))

def mod(a, b):
    return a - quot(a, b) * b

def shift_count(n):
    if n < 0 or n > 62:
        raise Fault('bad shift')
    return n

# D19: a negative exponent faults; 0 ** 0 is 1 as Python's is.
def power(a, b):
    if b < 0:
        raise Fault('bad exponent')
    if b > 64 and abs(a) >= 2:
        raise Fault('overflow')
    return fit(a ** b)

BIN = {
    '+': lambda a, b: fit(need_int(a) + need_int(b)),
    '-': lambda a, b: fit(need_int(a) - need_int(b)),
    '*': lambda a, b: fit(need_int(a) * need_int(b)),
    '/': lambda a, b: div(need_int(a), need_int(b)),
    '%': lambda a, b: mod(need_int(a), need_int(b)),
    '<': lambda a, b: need_int(a) < need_int(b),
    '<=': lambda a, b: need_int(a) <= need_int(b),
    '>': lambda a, b: need_int(a) > need_int(b),
    '>=': lambda a, b: need_int(a) >= need_int(b),
    '==': lambda a, b: a == b and type(a) is type(b),
    '!=': lambda a, b: not (a == b and type(a) is type(b)),
    'bit/and': lambda a, b: need_int(a) & need_int(b),
    'bit/or': lambda a, b: need_int(a) | need_int(b),
    'bit/xor': lambda a, b: need_int(a) ^ need_int(b),
    'bit/shl': lambda a, b: fit(need_int(a) << shift_count(need_int(b))),
    'bit/shr': lambda a, b: need_int(a) >> shift_count(need_int(b)),
    '**': lambda a, b: power(need_int(a), need_int(b)),
}

# The reader: integers, symbols, lists; `;` comments. A list is built on
# a stack of open lists, so depth costs nothing but memory.
def read(src):
    toks, i = [], 0
    while i < len(src):
        c = src[i]
        if c.isspace():
            i += 1
        elif c == ';':
            while i < len(src) and src[i] != '\n':
                i += 1
        elif c in '()':
            toks.append(c); i += 1
        else:
            j = i
            while j < len(src) and not src[j].isspace() and src[j] not in '();':
                j += 1
            toks.append(src[i:j]); i = j
    forms, stack = [], []
    for t in toks:
        if t == '(':
            stack.append([])
        elif t == ')':
            done = stack.pop()
            (stack[-1] if stack else forms).append(done)
        else:
            d = t[1:] if t.startswith('-') else t
            atom = int(t) if d.isdigit() else t
            (stack[-1] if stack else forms).append(atom)
    assert not stack, "missing ')'"
    return forms

# D21, D22: an operation is charged when it's applied, its operands
# already evaluated, before it checks or computes anything; every budget
# in force pays (D23), and the operation is refused if any has nothing
# left. Outside every `within` the list is empty and nothing is refused.
def charge(budgets):
    if 0 in budgets:
        raise Fault('budget spent')
    budgets[:] = [b - 1 for b in budgets]

# D24: the budget is an integer and not negative, checked before the
# body is evaluated.
def budget_of(n):
    if isinstance(n, bool):
        raise Fault('not an integer')
    if n < 0:
        raise Fault('bad budget')
    return n

# A parameter's value comes from the call's environment, a dict of the
# function's own parameters (D31): nothing else is in scope, and the
# program's expression has none.
def atom_value(f, env):
    if isinstance(f, int):
        return f
    if f == '#true':
        return True
    if f == '#false':
        return False
    return env[f]

# D34: the number of calls in progress, the program's expression at 0.
DEPTH = 10000

# Evaluation as a loop: a frame is a list form, how far along it is, the
# values so far, the parameters in scope, whether the form is in tail
# position (D33), and for a call the function. An `if` evaluates its
# test, then only the taken branch (D13), in tail position if the `if`
# is; an operator evaluates both arguments left to right, then is
# charged (D22), then applies (D25); a `within` evaluates its budget
# under the budgets already in force, checks it, puts it in force for
# its body, and takes it away after (D23, D24), neither part in tail
# position. A call (D32) evaluates its arguments left to right, is
# charged, is checked for depth (D34), and then waits on its body, which
# is in tail position; a call that is itself in tail position doesn't
# wait (D33): the frames between it and its caller's call, which can
# only be `if`s whose branch is the tail call, are dropped, and its body
# takes the place of its caller's, at the same depth. So a tail loop
# keeps the stack as it was, and the depth counts the calls that wait.
def ev(defs, form):
    if not isinstance(form, list):
        return atom_value(form, {})
    budgets = []
    depth = 0
    stack = [[form, 0, [], {}, False, defs.get(form[0])]]
    result = None
    while stack:
        fr = stack[-1]
        f, i, vals, env, tail, fn = fr
        head, args = f[0], f[1:]
        ntail, nenv = False, env
        if head == 'within':
            if i == 0:
                fr[1] = 1
                nxt = args[0]
            elif i == 1:
                budgets.append(budget_of(vals[0]))
                fr[1] = 2
                nxt = args[1]
            else:
                budgets.pop()
                result = vals[1]
                stack.pop()
                if stack:
                    stack[-1][2].append(result)
                continue
        elif head == 'if':
            if i == 0:
                fr[1] = 1
                nxt = args[0]
            elif i == 1:
                t = vals[0]
                if not isinstance(t, bool):
                    raise Fault('not a boolean')
                fr[1] = 2
                nxt = args[1] if t else args[2]
                ntail = tail
            else:
                result = vals[1]
                stack.pop()
                if stack:
                    stack[-1][2].append(result)
                continue
        elif fn is not None:
            params, body = fn
            if i < len(args):
                fr[1] = i + 1
                nxt = args[i]
            elif i == len(args):
                charge(budgets)
                if (depth if tail else depth + 1) > DEPTH:
                    raise Fault('stack')
                nenv = dict(zip(params, vals))
                nxt, ntail = body, True
                if tail:
                    stack.pop()
                    while stack[-1][5] is None or stack[-1][1] <= len(stack[-1][0]) - 1:
                        assert stack[-1][0][0] == 'if', stack[-1][0]
                        stack.pop()
                else:
                    depth += 1
                    fr[1] = i + 1
            else:
                depth -= 1
                result = vals[-1]
                stack.pop()
                if stack:
                    stack[-1][2].append(result)
                continue
        else:
            if i < 2:
                fr[1] = i + 1
                nxt = args[i]
            else:
                charge(budgets)
                result = BIN[head](vals[0], vals[1])
                stack.pop()
                if stack:
                    stack[-1][2].append(result)
                continue
        if isinstance(nxt, list):
            stack.append([nxt, 0, [], nenv, ntail, defs.get(nxt[0])])
        else:
            stack[-1][2].append(atom_value(nxt, nenv))
    return result

class Early(Exception):
    pass

KEYWORDS = set(BIN) | {'if', 'within', 'def'}

def is_name(x):
    return isinstance(x, str) and x not in ('#true', '#false')

# D31 and D28: a program is definitions and then one expression, and
# everything wrong with its shape or its names is an error before it
# runs. Such a program is never a golden test (D7), so the referee
# reports the error and exits 3, as for a program it doesn't cover. The
# walk is a loop over a list of forms to look at, as the evaluator is.
def check(forms):
    if not forms:
        raise Early('no expression')
    *ds, expr = forms
    if isinstance(expr, list) and expr and expr[0] == 'def':
        raise Early('definitions and no expression after them')
    defs = {}
    for d in ds:
        if not (isinstance(d, list) and d and d[0] == 'def'):
            raise Early('an expression before a definition, or two expressions')
        if len(d) != 3:
            raise Early(f'def takes 2 arguments, not {len(d) - 1}')
        sig = d[1]
        if not (isinstance(sig, list) and sig and all(is_name(x) for x in sig)):
            raise Early("a def's first part isn't a list of names")
        name, params = sig[0], sig[1:]
        if name in KEYWORDS:
            raise Early(f'{name} is not a name a function can have')
        if name in defs:
            raise Early(f'{name} is defined twice')
        if len(set(params)) != len(params):
            raise Early(f'{name} has two parameters with one name')
        defs[name] = (params, d[2])
    for name, (params, _) in defs.items():
        for p in params:
            if p in KEYWORDS or p in defs:
                raise Early(f'{p} is not a name a parameter can have')
    todo = [(body, set(params)) for params, body in defs.values()]
    todo.append((expr, set()))
    while todo:
        f, scope = todo.pop()
        if isinstance(f, int) or f in ('#true', '#false'):
            continue
        if not isinstance(f, list):
            if f in defs:
                raise Early(f'{f} is a function, used as a value')
            if f not in scope:
                raise Early(f'unknown name {f}')
            continue
        if not f or not isinstance(f[0], str) or f[0] in ('#true', '#false'):
            raise Early("a list whose head isn't an operator or a function")
        head, args = f[0], f[1:]
        if head == 'def':
            raise Early('a definition that is not at the top')
        if head in scope:
            raise Early(f'{head} is a parameter, used as a function')
        want = 3 if head == 'if' else 2 if head in BIN or head == 'within' else \
            len(defs[head][0]) if head in defs else None
        if want is None:
            raise Early(f'unknown name {head}')
        if len(args) != want:
            raise Early(f'{head} takes {want} arguments, not {len(args)}')
        todo.extend((a, scope) for a in args)
    return defs, expr

def show(v):
    return '#true' if v is True else '#false' if v is False else str(v)

if __name__ == '__main__':
    src = open(sys.argv[1]).read()
    try:
        defs, expr = check(read(src))
    except Early as e:
        print(f'referee: an error before running ({e}), not covered', file=sys.stderr)
        sys.exit(3)
    try:
        print(show(ev(defs, expr)))
    except Fault as e:
        print(f'fault: {e}')
        print('exit: 1')
