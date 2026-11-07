#!/usr/bin/env python3
"""The referee: an evaluator of the calculator from its decisions (D3 to
D7, D11 to D25, D31 to D33), on Python's unbounded integers, with the 63-bit range
and the division and shift rules applied as the decisions say. Written
from DECISIONS.md and not from the runtime, so that it is a second
implementation, and `make checks` runs it over every golden test and
fails where the two disagree. A program it doesn't cover (an operator
it has no entry for) is reported as such, exit 3, and the check skips
it; the large model extends it when a step's proposal says a referee
is wanted (docs/PROCESS.md, "The referee").

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

Strings (D31 to D33) are Python's `str`, which is a sequence of code
points, as D31's strings are; but the length, order and printing are
written out from the decisions here rather than left to Python where
the decision spells them out (`str_lt`, `show_str`). The source is read
as bytes and decoded as strict UTF-8, which refuses surrogates and
overlong forms, and stdout is written as UTF-8 whatever the locale.

An error before running (D28: arity, an unknown name, a literal past
the range, a bad string literal, a file that isn't UTF-8) can't be a
golden test (D7), so the referee doesn't judge one: it says what it
found on stderr and exits 3, as for a program it doesn't cover. It
checks the whole program before evaluating, untaken branches too, as
D28 says. Where the source does something no decision speaks to (a
string literal touching a name or another literal, white space other
than space, tab, newline and carriage return) it exits 3 as well.

    python3 t/referee/calc.py t/010-arith.lang
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1

class Fault(Exception):
    pass

# An error before running (D28); the referee exits 3 on it.
class Error(Exception):
    pass

# Source the decisions don't say how to read; exit 3 as well.
class Uncovered(Exception):
    pass

# A string literal as the reader gives it, so that it can't be taken
# for a name, which the reader gives as a `str`.
class Str:
    __slots__ = ('s',)
    def __init__(self, s):
        self.s = s

def fit(n):
    if n < MIN or n > MAX:
        raise Fault('overflow')
    return n

def need_int(v):
    if isinstance(v, bool) or not isinstance(v, int):
        raise Fault('not an integer')
    return v

def need_str(v):
    if not isinstance(v, str):
        raise Fault('not a string')
    return v

def is_scalar(n):
    return 0 <= n <= 0x10FFFF and not 0xD800 <= n <= 0xDFFF

# D33: each operand checked for its type, left to right, and only then
# the index or code point for its range.
def str_at(s, i):
    need_str(s)
    need_int(i)
    if i < 0 or i >= len(s):
        raise Fault('bad index')
    return s[i]

# D33: code point by code point; a string before any longer one it
# begins.
def str_lt(a, b):
    need_str(a)
    need_str(b)
    for k in range(min(len(a), len(b))):
        if ord(a[k]) != ord(b[k]):
            return ord(a[k]) < ord(b[k])
    return len(a) < len(b)

def str_code(s):
    need_str(s)
    if len(s) != 1:
        raise Fault('not a character')
    return ord(s)

def str_char(n):
    need_int(n)
    if not is_scalar(n):
        raise Fault('not a character')
    return chr(n)

# D12, D33: equal when the same type and the same value; two strings
# by their code points, with no normalising.
def same(a, b):
    return type(a) is type(b) and a == b

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
    '==': lambda a, b: same(a, b),
    '!=': lambda a, b: not same(a, b),
    'bit/and': lambda a, b: need_int(a) & need_int(b),
    'bit/or': lambda a, b: need_int(a) | need_int(b),
    'bit/xor': lambda a, b: need_int(a) ^ need_int(b),
    'bit/shl': lambda a, b: fit(need_int(a) << shift_count(need_int(b))),
    'bit/shr': lambda a, b: need_int(a) >> shift_count(need_int(b)),
    '**': lambda a, b: power(need_int(a), need_int(b)),
}

# D33's six, beside the seventeen; each one operation (D21).
OPS = dict(BIN)
OPS.update({
    'str/len': lambda s: len(need_str(s)),
    'str/at': str_at,
    'str/cat': lambda a, b: need_str(a) + need_str(b),
    'str/lt': str_lt,
    'str/code': str_code,
    'str/char': str_char,
})

# How many operands each takes (D3, D13, D24, D33).
ARITY = {name: 2 for name in OPS}
ARITY.update({'str/len': 1, 'str/code': 1, 'str/char': 1, 'if': 3, 'within': 2})

# The reader: integers, string literals, symbols, lists; `;` comments.
# `src` is the decoded source, a sequence of code points. A list is
# built on a stack of open lists, so depth costs nothing but memory.
SPACE = ' \t\n\r'
HEX = '0123456789abcdefABCDEF'

# D31: `\"`, `\\`, `\n`, `\t` and `\u{X}` (one to six hex digits, a
# scalar value); any other character but a newline stands for itself.
def read_string(src, i):
    out, i, n = [], i + 1, len(src)
    while True:
        if i >= n:
            raise Error('a string literal with no closing "')
        c = src[i]
        if c == '"':
            return ''.join(out), i + 1
        if c == '\n':
            raise Error('a newline inside a string literal')
        if c != '\\':
            out.append(c)
            i += 1
            continue
        e = src[i + 1] if i + 1 < n else ''
        if e in ('"', '\\'):
            out.append(e)
            i += 2
        elif e == 'n':
            out.append('\n')
            i += 2
        elif e == 't':
            out.append('\t')
            i += 2
        elif e == 'u' and i + 2 < n and src[i + 2] == '{':
            j = i + 3
            while j < n and src[j] in HEX:
                j += 1
            digits = src[i + 3:j]
            if j >= n or src[j] != '}' or not 1 <= len(digits) <= 6:
                raise Error('a \\u{X} that is empty, not hex or longer than six digits')
            v = int(digits, 16)
            if not is_scalar(v):
                raise Error(f'\\u{{{digits}}} is not a Unicode scalar value')
            out.append(chr(v))
            i = j + 1
        else:
            raise Error('a backslash before ' + (repr(e) if e else 'the end of the file'))

def is_int_token(t):
    d = t[1:] if t.startswith('-') else t
    return d != '' and all('0' <= c <= '9' for c in d)

def read(src):
    toks, i, n = [], 0, len(src)
    # Where the last name, number or string literal ended: one that
    # starts there touches it, which nothing decides the meaning of.
    end = -1
    while i < n:
        c = src[i]
        if c in SPACE:
            i += 1
        elif c.isspace():
            raise Uncovered(f'white space U+{ord(c):04X}, which no decision names')
        elif c == ';':
            while i < n and src[i] != '\n':
                i += 1
        elif c in '()':
            toks.append(c); i += 1
        elif c == '"':
            if end == i:
                raise Uncovered('a string literal touching what comes before it')
            s, i = read_string(src, i)
            toks.append(Str(s)); end = i
        else:
            if end == i:
                raise Uncovered('a name touching the string literal before it')
            j = i
            while j < n and src[j] not in '();"' and not src[j].isspace():
                j += 1
            toks.append(src[i:j]); i = j; end = j
    forms, stack = [], []
    for t in toks:
        if t == '(':
            stack.append([])
        elif t == ')':
            if not stack:
                raise Error("a ')' with no '('")
            done = stack.pop()
            (stack[-1] if stack else forms).append(done)
        else:
            atom = int(t) if isinstance(t, str) and is_int_token(t) else t
            (stack[-1] if stack else forms).append(atom)
    if stack:
        raise Error("missing ')'")
    return forms

# D28: what's an error before running is found before anything is
# evaluated, in every branch: a form's arity (D3, D13, D24, D33), an
# unknown name, a literal past the range (D4). A loop over a stack of
# forms still to look at.
def check(form):
    todo = [form]
    while todo:
        f = todo.pop()
        if isinstance(f, list):
            if not f or not isinstance(f[0], str) or f[0] not in ARITY:
                raise Error('a list that is not a form: ' + (repr(f[0]) if f else '()'))
            if len(f) - 1 != ARITY[f[0]]:
                raise Error(f'{f[0]} takes {ARITY[f[0]]}, not {len(f) - 1}')
            todo.extend(f[1:])
        elif isinstance(f, int):
            if f < MIN or f > MAX:
                raise Error(f'{f} is past the range')
        elif isinstance(f, Str) or f in ('#true', '#false'):
            pass
        else:
            raise Error(f'unknown name {f}')

# D21, D22: an operation is charged when it's applied, its operands
# already evaluated, before it checks or computes anything; every budget
# in force pays (D23), and the operation is refused if any has nothing
# left. Outside every `within` the list is empty and nothing is refused.
def charge(budgets):
    if any(b == 0 for b in budgets):
        raise Fault('budget spent')
    for k in range(len(budgets)):
        budgets[k] -= 1

# D24: the budget is an integer and not negative, checked before the
# body is evaluated. A string isn't an integer either (D24 names the
# boolean, D33 the seventeen operators; `not an integer` is the one
# fault for a value that isn't).
def budget_of(n):
    need_int(n)
    if n < 0:
        raise Fault('bad budget')
    return n

def atom_value(f):
    if isinstance(f, int):
        return f
    if isinstance(f, Str):
        return f.s
    if f == '#true':
        return True
    if f == '#false':
        return False
    raise KeyError(f)

# Evaluation as a loop: a frame is a list form, how far along it is, and
# the values so far. An `if` evaluates its test, then only the taken
# branch (D13); an operator evaluates its operands left to right, then
# is charged (D22), then applies (D25, D33); a `within` evaluates its budget
# under the budgets already in force, checks it, puts it in force for
# its body, and takes it away after (D23, D24).
def ev(form):
    if not isinstance(form, list):
        return atom_value(form)
    budgets = []
    stack = [[form, 0, []]]
    result = None
    while stack:
        f, i, vals = stack[-1]
        head, args = f[0], f[1:]
        if head == 'within':
            if i == 0:
                stack[-1][1] = 1
                nxt = args[0]
            elif i == 1:
                budgets.append(budget_of(vals[0]))
                stack[-1][1] = 2
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
                stack[-1][1] = 1
                nxt = args[0]
            elif i == 1:
                t = vals[0]
                if not isinstance(t, bool):
                    raise Fault('not a boolean')
                stack[-1][1] = 2
                nxt = args[1] if t else args[2]
            else:
                result = vals[1]
                stack.pop()
                if stack:
                    stack[-1][2].append(result)
                continue
        else:
            if i < len(args):
                stack[-1][1] = i + 1
                nxt = args[i]
            else:
                if head not in OPS:
                    raise KeyError(head)
                charge(budgets)
                result = OPS[head](*vals)
                stack.pop()
                if stack:
                    stack[-1][2].append(result)
                continue
        if isinstance(nxt, list):
            stack.append([nxt, 0, []])
        else:
            stack[-1][2].append(atom_value(nxt))
    return result

# D32, written out: in double quotes; `"` and `\` with a backslash
# before them, a newline `\n`, a tab `\t`, every other code point below
# U+0020 and U+007F as `\u{X}` in lowercase hex without leading zeros,
# and every other code point as itself.
def show_str(s):
    out = ['"']
    for c in s:
        o = ord(c)
        if c == '"' or c == '\\':
            out.append('\\' + c)
        elif c == '\n':
            out.append('\\n')
        elif c == '\t':
            out.append('\\t')
        elif o < 0x20 or o == 0x7F:
            out.append('\\u{' + format(o, 'x') + '}')
        else:
            out.append(c)
    out.append('"')
    return ''.join(out)

def show(v):
    if v is True:
        return '#true'
    if v is False:
        return '#false'
    if isinstance(v, str):
        return show_str(v)
    return str(v)

def out(text):
    sys.stdout.buffer.write((text + '\n').encode('utf-8'))

if __name__ == '__main__':
    try:
        # D31: the source is UTF-8; Python's strict decoder refuses
        # surrogates, overlong forms and stray bytes.
        src = open(sys.argv[1], 'rb').read().decode('utf-8')
        forms = read(src)
        if len(forms) != 1:
            raise Error(f'a program is one expression, not {len(forms)}')
        check(forms[0])
    except (Error, UnicodeDecodeError) as e:
        print(f'referee: error before running, not judged: {e}', file=sys.stderr)
        sys.exit(3)
    except Uncovered as e:
        print(f'referee: not covered: {e}', file=sys.stderr)
        sys.exit(3)
    try:
        out(show(ev(forms[0])))
    except Fault as e:
        out(f'fault: {e}')
        out('exit: 1')
    except KeyError as e:
        print(f'referee: no entry for {e}', file=sys.stderr)
        sys.exit(3)
