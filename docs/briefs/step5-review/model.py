#!/usr/bin/env python3
"""A reviewer's model of step 5 as PROPOSED: variables, assignment, ++/--, late
reads, blocks, if/elsif/else/unless, statement modifiers.

The expression language that is already built (numbers, strings, booleans,
undef, comparison) is not modelled again: every operator of it is the built
runtime's own function, called through rt/librtm.so (rt.c with a fault that
can be caught and output into a buffer). What is new is written here from the
proposal's text alone.

A program is a tree of tuples (see the constructors below), printed by `show`
and run by `run`. `run` gives (stdout bytes, fault message or None).
"""
import ctypes, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')


def bridge():
    """rtm.c round the runtime as it stands (runtime/rt.c, its fault and its two
    writes replaced, each replacement asserted), built in a scratch directory."""
    import subprocess, tempfile
    work = os.path.join(tempfile.gettempdir(), 'curly-step5-review-%d' % os.getuid())
    os.makedirs(work, exist_ok=True)
    so = os.path.join(work, 'librtm.so')
    rt = os.path.join(ROOT, 'runtime', 'rt.c')
    if not os.path.exists(so) or os.path.getmtime(so) < max(os.path.getmtime(rt), os.path.getmtime(os.path.join(HERE, 'rtm.c'))):
        src = open(rt).read()
        fault = """void rt_fault(rt_ctx *cx, const char *what) {
    fflush(stdout);
    fprintf(stderr, "fault: %s at %s line %" PRId64 ".\\n", what, cx->file, cx->line);
    release(cx);
    exit(1);
}"""
        assert src.count(fault) == 1, 'rt_fault is not as this script knows it'
        src = src.replace(fault, 'void rt_fault(rt_ctx *cx, const char *what) {\n    (void)cx;\n    m_fault(what);\n}')
        write = """    fwrite(bytes, 1, len, stdout);
    if (newline) putc('\\n', stdout);"""
        assert src.count(write) == 1, 'emit is not as this script knows it'
        src = src.replace(write, '    m_write(bytes, len);\n    if (newline) m_write("\\n", 1);')
        open(os.path.join(work, 'rt_patched.c'), 'w').write(src)
        subprocess.run([os.environ.get('CURLY_CC', 'cc'), '-O1', '-shared', '-fPIC', '-w', '-I', os.path.join(ROOT, 'runtime'), '-I', work,
                        '-o', so + '.new', os.path.join(HERE, 'rtm.c'), '-lm'], check=True)
        os.replace(so + '.new', so)
    return ctypes.CDLL(so)


lib = bridge()


class V(ctypes.Structure):
    _fields_ = [('tag', ctypes.c_uint64), ('bits', ctypes.c_uint64)]


T_INT, T_NUM, T_STR, T_UNDEF, T_BOOL = 1, 2, 3, 4, 5
VP = ctypes.POINTER(V)
lib.m_op.argtypes = [ctypes.c_int, VP, VP, VP, VP]
lib.m_what.restype = ctypes.c_char_p
lib.m_mkstr.argtypes = [ctypes.c_char_p, ctypes.c_long, VP]
lib.m_strbytes.argtypes = [VP, ctypes.POINTER(ctypes.c_long)]
lib.m_strbytes.restype = ctypes.POINTER(ctypes.c_char)
lib.m_out.argtypes = [ctypes.POINTER(ctypes.c_long)]
lib.m_out.restype = ctypes.POINTER(ctypes.c_char)
lib.m_truth.argtypes = [VP, ctypes.POINTER(ctypes.c_int)]
lib.m_emit.argtypes = [VP, ctypes.c_int]
lib.m_numeric.argtypes = [VP, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_longlong),
                          ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

OPS = {name: i + 1 for i, name in enumerate(
    'ADD SUB MUL DIV MOD POW NEG CONCAT REPEAT LENGTH UC LC ORD CHR SUBSTR2 SUBSTR3 INDEX2 INDEX3 '
    'NOT XOR DEFINED NEQ NNE NLT NGT NLE NGE NCMP SEQ SNE SLT SGT SLE SGE SCMP'.split())}
BINOP = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV', '%': 'MOD', '**': 'POW', '.': 'CONCAT', 'x': 'REPEAT',
         '==': 'NEQ', '!=': 'NNE', '<': 'NLT', '>': 'NGT', '<=': 'NLE', '>=': 'NGE', '<=>': 'NCMP',
         'eq': 'SEQ', 'ne': 'SNE', 'lt': 'SLT', 'gt': 'SGT', 'le': 'SLE', 'ge': 'SGE', 'cmp': 'SCMP', 'xor': 'XOR'}
FN1 = {'defined': 'DEFINED', 'length': 'LENGTH', 'uc': 'UC', 'lc': 'LC', 'ord': 'ORD', 'chr': 'CHR'}


class Fault(Exception):
    pass


def I(n):
    v = V(); v.tag = T_INT; v.bits = n & 0xFFFFFFFFFFFFFFFF; return v


def N(x):
    v = V(); v.tag = T_NUM
    v.bits = ctypes.c_uint64.from_buffer_copy(ctypes.c_double(x)).value
    return v


def S(b):
    if isinstance(b, str): b = b.encode('ascii')
    v = V(); lib.m_mkstr(b, len(b), ctypes.byref(v)); return v


def U():
    v = V(); v.tag = T_UNDEF; v.bits = 0; return v


def B(t):
    v = V(); v.tag = T_BOOL; v.bits = 1 if t else 0; return v


def as_int(v):
    return ctypes.c_int64(v.bits).value


def as_num(v):
    return ctypes.c_double.from_buffer_copy(ctypes.c_uint64(v.bits)).value


def as_bytes(v):
    n = ctypes.c_long()
    p = lib.m_strbytes(ctypes.byref(v), ctypes.byref(n))
    return ctypes.string_at(p, n.value)


def describe(v):
    if v.tag == T_INT: return 'Int %d' % as_int(v)
    if v.tag == T_NUM: return 'Num %r' % as_num(v)
    if v.tag == T_STR: return 'Str %r' % as_bytes(v)
    if v.tag == T_UNDEF: return 'undef'
    return 'Bool %d' % v.bits


def rt(name, a, b=None, c=None):
    out = V()
    if lib.m_op(OPS[name], ctypes.byref(a), ctypes.byref(b) if b is not None else None,
                ctypes.byref(c) if c is not None else None, ctypes.byref(out)):
        raise Fault(lib.m_what().decode())
    return out


def truth(v):
    out = ctypes.c_int()
    if lib.m_truth(ctypes.byref(v), ctypes.byref(out)): raise Fault(lib.m_what().decode())
    return bool(out.value)


def numeric(v):
    """The runtime's own string-to-number rule: ('i', int) or ('n', float), and the double."""
    a, i, n, d = ctypes.c_int(), ctypes.c_longlong(), ctypes.c_double(), ctypes.c_double()
    if lib.m_numeric(ctypes.byref(v), ctypes.byref(a), ctypes.byref(i), ctypes.byref(n), ctypes.byref(d)):
        raise Fault(lib.m_what().decode())
    return (('i', i.value) if a.value else ('n', n.value)), d.value


TWO53 = 2.0 ** 53
IMAX, IMIN = 2 ** 63 - 1, -2 ** 63


# ---- what is new: ++ and --, as the proposal words them

def step(v, sign):
    """What `++` (sign 1) or `--` (sign -1) stores in a variable that holds v."""
    if v.tag == T_UNDEF: return I(sign)
    if v.tag == T_BOOL: return I(v.bits + sign)
    if v.tag == T_INT:
        n = as_int(v) + sign
        if n > IMAX or n < IMIN: raise Fault('integer overflow')
        return I(n)
    if v.tag == T_NUM:
        x = as_num(v)
        whole = x == math.trunc(x)
        if x + sign == x: raise Fault('the step is lost')
        if sign == 1:
            if whole and abs(x) < TWO53: return I(int(x) + 1)
            return N(x + 1.0)
        if whole and abs(x) < TWO53 and abs(x - 1.0) >= TWO53: raise Fault('-- of a whole Num to 2^53')
        return N(x - 1.0)
    # a Str
    _, d = numeric(v)
    whole = d == math.trunc(d)
    r = d + sign
    if whole and (abs(d) >= TWO53 or abs(r) >= TWO53): raise Fault('++/-- of a string this large')
    if sign == 1:
        b = as_bytes(v)
        if len(b) > 1 and b.isdigit() and b[:1] == b'0': raise Fault('++ of digits with a leading zero')
    return N(r)


class Cell:
    __slots__ = ('v', 'name')

    def __init__(self, name, v):
        self.name = name; self.v = v


def rd(r):
    """An operand, read now: the variable's value if it is the variable itself."""
    return r.v if isinstance(r, Cell) else r


class Interp:
    def __init__(self):
        self.scopes = [{}]
        self.pending = None      # `my` variables of the condition being evaluated

    def lookup(self, name):
        for s in reversed(self.scopes):
            if name in s: return s[name]
        raise KeyError('model: no variable $' + name)

    # -- expressions: a Cell (the variable itself) or a value
    def ev(self, e):
        k = e[0]
        if k == 'lit':
            kind, val = e[2], e[3]
            if kind == 'i': return I(val)
            if kind == 'n': return N(val)
            if kind == 's': return S(val)
            if kind == 'b': return B(val)
            return U()
        if k == 'var': return self.lookup(e[1])
        if k == 'paren' or k == 'uplus': return self.ev(e[1])
        if k == 'neg': return rt('NEG', rd(self.ev(e[1])))
        if k == 'not' or k == 'lnot': return rt('NOT', rd(self.ev(e[1])))
        if k == 'fn1': return rt(FN1[e[1]], rd(self.ev(e[2])))
        if k == 'fn':
            rs = [self.ev(a) for a in e[2]]
            vs = [rd(r) for r in rs]
            name = {('substr', 2): 'SUBSTR2', ('substr', 3): 'SUBSTR3', ('index', 2): 'INDEX2', ('index', 3): 'INDEX3'}[(e[1], len(vs))]
            return rt(name, *vs)
        if k == 'bin':
            a = self.ev(e[2]); b = self.ev(e[3])
            return rt(BINOP[e[1]], rd(a), rd(b))
        if k == 'log':
            a = self.ev(e[2])
            op = e[1]
            if op in ('&&', 'and'): take_right = truth(rd(a))
            elif op in ('||', 'or'): take_right = not truth(rd(a))
            else: take_right = rd(a).tag == T_UNDEF
            return self.ev(e[3]) if take_right else a
        if k == 'tern':
            return self.ev(e[2]) if truth(rd(self.ev(e[1]))) else self.ev(e[3])
        if k == 'asg': return self.assign(e)
        if k in ('pre', 'post'):
            cell = self.lookup(e[2])
            sign = 1 if e[1] == '++' else -1
            old = cell.v
            cell.v = step(old, sign)
            if k == 'pre': return cell
            if old.tag == T_UNDEF: return I(0) if sign == 1 else U()
            return old
        raise KeyError('model: no such node ' + k)

    def target(self, t):
        if t[0] == 'var': return self.lookup(t[1])
        cell = Cell(t[1], U())          # ('my', name): not visible until the condition is done
        self.pending.append(cell)
        return cell

    def assign(self, e):
        op, t, rhs = e[1], e[2], e[3]
        if op == '=':
            cell = self.target(t) if t[0] == 'my' else None
            v = rd(self.ev(rhs))
            if cell is None: cell = self.target(t)
            cell.v = v
            return cell
        cell = self.lookup(t[1])
        if op in ('||=', '&&=', '//='):
            if op == '||=': go = not truth(cell.v)
            elif op == '&&=': go = truth(cell.v)
            else: go = cell.v.tag == T_UNDEF
            if go: cell.v = rd(self.ev(rhs))
            return cell
        b = self.ev(rhs)
        left, right = cell.v, rd(b)      # the variable is read when the operator runs
        o = op[:-1]
        if left.tag == T_UNDEF:
            if o in ('+', '-'): left = I(0)
            elif o == '.': left = S(b'')
            else: raise Fault('undef on the left of ' + op)
        cell.v = rt(BINOP[o], left, right)
        return cell

    # -- statements
    def block(self, stmts):
        self.scopes.append({})
        try:
            for s in stmts: self.stmt(s)
        finally:
            self.scopes.pop()

    def cond(self, e):
        self.pending = []
        t = truth(rd(self.ev(e)))
        for cell in self.pending: self.scopes[-1][cell.name] = cell
        self.pending = None
        return t

    def stmt(self, s):
        k = s[0]
        if k == 'my':
            v = rd(self.ev(s[2])) if s[2] is not None else U()
            self.scopes[-1][s[1]] = Cell(s[1], v)
        elif k == 'expr': self.ev(s[1])
        elif k in ('say', 'print'):
            v = rd(self.ev(s[1]))
            if lib.m_emit(ctypes.byref(v), 1 if k == 'say' else 0): raise Fault(lib.m_what().decode())
        elif k == 'block': self.block(s[1])
        elif k == 'if':
            self.scopes.append({})       # the chain's own scope, for a `my` in a condition
            try:
                done = False
                for c, body in s[1]:
                    if done:
                        # a later condition's `my` is declared whether or not it runs
                        for name in my_names(c): self.scopes[-1][name] = Cell(name, U())
                        continue
                    if self.cond(c):
                        self.block(body); done = True
                if not done and s[2] is not None: self.block(s[2])
            finally:
                self.scopes.pop()
        elif k == 'unless':
            self.scopes.append({})
            try:
                if not self.cond(s[1]): self.block(s[2])
            finally:
                self.scopes.pop()
        elif k == 'mod':
            t = truth(rd(self.ev(s[3])))
            if (s[2] == 'if') == t: self.stmt(s[1])
        else:
            raise KeyError('model: no such statement ' + k)


def my_names(e):
    out = []
    def walk(x):
        if isinstance(x, tuple):
            if x and x[0] == 'my' and len(x) == 2: out.append(x[1])
            for y in x: walk(y)
        elif isinstance(x, list):
            for y in x: walk(y)
    walk(e)
    return out


def run(prog):
    """(stdout, fault or None) for a list of statements."""
    lib.m_reset()
    it = Interp()
    fault = None
    try:
        for s in prog: it.stmt(s)
    except Fault as f:
        fault = str(f)
    n = ctypes.c_long()
    p = lib.m_out(ctypes.byref(n))
    out = ctypes.string_at(p, n.value) if n.value else b''
    return out, fault


# ---- printing a tree as source. Every operand that is not an atom gets brackets,
# so the tree printed is the tree perl parses whatever the precedences are; a
# generator that wants to test precedence writes its text by hand.

def lit(text):
    """A literal from its source text."""
    if text == 'true': return ('lit', text, 'b', 1)
    if text == 'false': return ('lit', text, 'b', 0)
    if text == 'undef': return ('lit', '(undef)', 'u', None)
    if text[0] in '"\'':
        body = text[1:-1]
        assert '\\' not in body and '$' not in body and '@' not in body
        return ('lit', text, 's', body)
    t = text.replace('_', '')
    if all(ch in '0123456789' for ch in t): return ('lit', text, 'i', int(t))
    return ('lit', text, 'n', float(t))


ATOMS = ('lit', 'var', 'paren', 'fn', 'fn1')


def show(e, top=False):
    k = e[0]
    if k == 'lit': return e[1]
    if k == 'var': return '$' + e[1]
    if k == 'my': return 'my $' + e[1]
    if k == 'paren': return '(' + show(e[1], True) + ')'
    def arg(x):
        return show(x) if x[0] in ATOMS else '(' + show(x, True) + ')'
    if k == 'uplus': return '+' + arg(e[1])
    if k == 'neg': return '-' + arg(e[1])
    if k == 'not': return '!' + arg(e[1])
    if k == 'lnot':
        assert e[1][0] in ('var', 'lit')
        return 'not ' + show(e[1])
    if k == 'fn1': return e[1] + '(' + show(e[2], True) + ')'
    if k == 'fn': return e[1] + '(' + ', '.join(arg(a) for a in e[2]) + ')'
    if k == 'bin' or k == 'log': return arg(e[2]) + ' ' + e[1] + ' ' + arg(e[3])
    if k == 'tern': return arg(e[1]) + ' ? ' + arg(e[2]) + ' : ' + arg(e[3])
    if k == 'asg': return show(e[2]) + ' ' + e[1] + ' ' + arg(e[3])
    if k == 'pre': return e[1] + '$' + e[2]
    if k == 'post': return '$' + e[2] + e[1]
    raise KeyError(k)


def show_stmt(s, ind=''):
    k = s[0]
    if k == 'my':
        if s[2] is None: return ind + 'my $' + s[1] + ';'
        loose = s[2][0] == 'lnot' or (s[2][0] in ('log', 'bin') and s[2][1] in ('and', 'or', 'xor'))
        return ind + 'my $' + s[1] + ' = ' + ('(' + show(s[2], True) + ')' if loose else show(s[2], True)) + ';'
    if k == 'expr': return ind + show(s[1], True) + ';'
    if k in ('say', 'print'): return ind + k + '(' + show(s[1], True) + ');'
    if k == 'block': return ind + '{\n' + show_block(s[1], ind + '    ') + ind + '}'
    if k == 'if':
        out = ''
        for n, (c, body) in enumerate(s[1]):
            out += (ind + 'if' if n == 0 else ' elsif') + ' (' + show(c, True) + ') {\n' + show_block(body, ind + '    ') + ind + '}'
        if s[2] is not None: out += ' else {\n' + show_block(s[2], ind + '    ') + ind + '}'
        return out
    if k == 'unless': return ind + 'unless (' + show(s[1], True) + ') {\n' + show_block(s[2], ind + '    ') + ind + '}'
    if k == 'mod': return ind + show_stmt(s[1])[:-1] + ' ' + s[2] + ' ' + show(s[3], True) + ';'
    raise KeyError(k)


def show_block(stmts, ind):
    return ''.join(show_stmt(s, ind) + '\n' for s in stmts)


def source(prog):
    return 'use v5.42;\n' + show_block(prog, '')


# ---- the proposal's refusal of `=` with a constant right side in truth position

def has_var(e):
    if isinstance(e, tuple):
        if e and e[0] in ('var', 'pre', 'post'): return True
        if e and e[0] == 'my' and len(e) == 2: return True
        return any(has_var(x) for x in e)
    if isinstance(e, list): return any(has_var(x) for x in e)
    return False


def truth_refused(e, strict=False):
    """True if `e`, standing in truth position, holds an assignment the proposal
    refuses there. With strict, also what perl warns of and the proposal lets
    by: through `!`, `not` and unary plus."""
    k = e[0]
    if k == 'paren': return truth_refused(e[1], strict)
    if k == 'asg' and e[1] == '=' and not has_var(e[3]): return True
    if k == 'log': return truth_refused(e[3], strict)       # its left is found by the walk below
    if k == 'tern': return truth_refused(e[2], strict) or truth_refused(e[3], strict)
    if strict and k in ('not', 'lnot', 'uplus'): return truth_refused(e[1], strict)
    return False


def any_truth_refused(x, strict=False):
    """Walk statements and expressions for a refused assignment in any truth position."""
    if isinstance(x, list): return any(any_truth_refused(y, strict) for y in x)
    if not isinstance(x, tuple) or not x: return False
    k = x[0]
    if k == 'if':
        return any(truth_refused(c, strict) or any_truth_refused(c, strict) or any_truth_refused(b, strict) for c, b in x[1]) \
            or (x[2] is not None and any_truth_refused(x[2], strict))
    if k == 'unless': return truth_refused(x[1], strict) or any_truth_refused(x[1], strict) or any_truth_refused(x[2], strict)
    if k == 'mod': return truth_refused(x[3], strict) or any_truth_refused(x[3], strict) or any_truth_refused(x[1], strict)
    if k == 'tern' and truth_refused(x[1], strict): return True
    if k == 'log' and truth_refused(x[2], strict): return True
    return any(any_truth_refused(y, strict) for y in x[1:] if isinstance(y, (tuple, list)))


# ---- the built compiler's list-context refusal (T104), which a program with
# variables meets too: `(...) x N` where say's list context reaches

def strip(e):
    while e[0] in ('paren', 'uplus'): e = e[1]
    return e


def list_refused(e):
    """e is the argument of say or print."""
    s = e
    while s[0] == 'uplus': s = s[1]
    inner = strip(e)
    if inner[0] == 'tern': return list_refused(inner[2]) or list_refused(inner[3])
    if inner[0] == 'log': return list_refused(inner[3])
    if inner[0] == 'bin' and inner[1] == 'x':
        return inner[2][0] not in ('lit', 'var', 'fn', 'fn1')     # `show` puts brackets round anything else
    return False


def any_list_refused(x):
    if isinstance(x, list): return any(any_list_refused(y) for y in x)
    if not isinstance(x, tuple) or not x: return False
    if x[0] in ('say', 'print'): return list_refused(x[1])
    return any(any_list_refused(y) for y in x[1:] if isinstance(y, (tuple, list)))


# ---- findings of this review, as predicates, so that a search can go on past them

def walk(x):
    if isinstance(x, list):
        for y in x: yield from walk(y)
    elif isinstance(x, tuple) and x:
        if isinstance(x[0], str): yield x
        for y in x:
            if isinstance(y, (tuple, list)): yield from walk(y)


WIDE_CHAIN = False     # also `$t .= A . B`, which the first search skipped and the second did not


def has_chain(prog):
    """A `.` whose left operand is a `.` (through brackets and unary plus): perl
    makes one operator of the chain and reads every operand at its end."""
    for e in walk(prog):
        if e[0] == 'bin' and e[1] == '.' and strip(e[2])[0] == 'bin' and strip(e[2])[1] == '.': return True
        if WIDE_CHAIN and e[0] == 'asg' and e[1] == '.=' and strip(e[3])[0] == 'bin' and strip(e[3])[1] == '.': return True
    return False


def has_append_of_assigned_concat(prog):
    """`T .= (U = A . B)`: perl 5.42 drops the assignment to U."""
    for e in walk(prog):
        if e[0] == 'asg' and e[1] == '.=':
            r = strip(e[3])
            if r[0] == 'asg' and r[1] == '=' and strip(r[3])[0] == 'bin' and strip(r[3])[1] == '.': return True
    return False


def folds_to_constant(e):
    """Does perl fold e to a constant though it holds a variable? (roughly)"""
    e = strip(e)
    if e[0] == 'lit': return e[2] != 'u'
    if e[0] in ('var', 'asg', 'pre', 'post', 'fn', 'my'): return False
    if e[0] == 'log':
        if not folds_to_constant(e[2]): return False
        return True          # a constant left side: perl takes one side at compile time; treat as folded
    if e[0] == 'tern':
        return folds_to_constant(e[1])
    if e[0] in ('neg', 'not', 'lnot'): return folds_to_constant(e[1])
    if e[0] == 'fn1': return folds_to_constant(e[2])
    if e[0] == 'bin': return folds_to_constant(e[2]) and folds_to_constant(e[3])
    return False
