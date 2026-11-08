#!/usr/bin/env python3
"""Random Ditto program generator. Usage: gen.py SEED [--else]
Integers carry a magnitude bound so ordinary expressions cannot overflow;
faults and compile errors are injected on purpose (about 15% / 5%)."""
import random, sys

MAX = 9223372036854775807
MINS = "(-9223372036854775807 - 1)"
B2 = 2**63
VB = 1000003  # bound of every stored small int

class G:
    def __init__(s, seed, use_else):
        s.r = random.Random(seed)
        s.use_else = use_else
        s.n = 0
        s.env = [[]]          # scopes of (name, type, bound)
        s.out = []
        s.ind = 0
        s.loop = 0
        s.fns = []            # available functions: (name, ptypes, rtype, rbound)
        s.feat = set()
    # ---- helpers
    def ch(s, xs): return s.r.choice(xs)
    def p(s, x=0.5): return s.r.random() < x
    def fresh(s, base="v"):
        s.n += 1; return f"{base}{s.n}"
    def emit(s, line): s.out.append("  " * s.ind + line)
    def vars(s, t):
        return [(n, b) for sc in s.env for (n, ty, b) in sc if ty == t]
    def declare(s, n, t, b=0): s.env[-1].append((n, t, b))
    def push(s): s.env.append([])
    def pop(s): s.env.pop()
    def f(s, name): s.feat.add(name)

    # ---- ints: return (text, bound)
    def edge(s):
        s.f("edge")
        return s.ch([
            (str(MAX), MAX), (MINS, B2), (f"({MAX} - 1)", MAX), (f"({MINS} + 1)", MAX),
            (f"-{MAX}", MAX), (f"({MAX} / 2)", MAX // 2), (f"({MAX} % 1000)", 999),
            (f"({MINS} % 7)", 6), (f"({MAX} + {MINS})", 1), ("4611686018427387904", 2**62),
            ("3037000499", 3037000499), (f"({MINS} / 2)", B2 // 2), (f"({MAX} * 1)", MAX),
            (f"({MINS} * 1)", B2), (f"({MINS} % -1)", 0), (f"({MAX} / -1)", MAX),
            (f"({MINS} + 1) / -1", MAX), ("9223372036854775806", MAX), ("-9223372036854775807", MAX),
            (f"({MAX} - {MAX})", 0), ("4294967296 * 2147483647", MAX), ("1_000_000_007", 10**9 + 7),
        ])
    def small_lit(s):
        return (str(s.ch([0, 0, 1, 1, 2, 3, 5, 7, 10, 13, 42, 100, 255, 1000, 65536])), 65536) \
            if False else (lambda v: (str(v), v))(s.ch([0, 1, 2, 3, 5, 7, 9, 10, 13, 42, 100, 255, 1000, 65536]))
    def int_(s, d=2, maxb=None):
        """int expression; bound <= maxb (default 2^63-1)."""
        maxb = MAX if maxb is None else maxb
        t, b = s.int_raw(d, maxb)
        if b > maxb:   # should be rare; wrap
            m = min(maxb, VB)
            return f"({t} % {m + 1})", m
        return t, b
    def int_raw(s, d, maxb):
        r = s.r
        c = r.random()
        if d <= 0 or c < 0.25:
            k = r.random()
            if k < 0.35:
                v = s.vars("int")
                if v:
                    n, b = s.ch(v); return n, b
            if k < 0.45 and maxb >= B2 - 1:
                return s.edge()
            if k < 0.55:
                v = s.vars("big")
                if v and maxb >= B2 - 1:
                    n, b = s.ch(v); return n, b
            if k < 0.65:
                x = s.data_int()
                if x: return x
            if k < 0.72:
                v = r.randint(1, 5)
                return f"-{v}" if False else (f"(-{v})", v)
            return s.small_lit()
        k = r.random()
        if k < 0.30:
            (a, ba), (b, bb) = s.int_(d-1, maxb//2 if maxb < MAX else MAX // 2), s.int_(d-1, maxb//2 if maxb < MAX else MAX // 2)
            op = s.ch(["+", "-"]); s.f("arith")
            return f"({a} {op} {b})", ba + bb
        if k < 0.45:
            lim = min(maxb, MAX)
            (a, ba) = s.int_(d-1, 10**9)
            (b, bb) = s.int_(d-1, max(1, min(10**9, lim // max(ba, 1))))
            if ba * bb > MAX:
                return a, ba
            s.f("mul")
            return f"({a} * {b})", ba * bb
        if k < 0.65:
            (a, ba) = s.int_(d-1, MAX)
            op = s.ch(["/", "%"]); s.f("divmod")
            dv = s.divisor(ba)
            return f"({a} {op} {dv[0]})", (ba if op == "/" else min(ba, dv[1]))
        if k < 0.70:
            (a, ba) = s.int_(d-1, MAX)
            if ba >= B2: return a, ba
            return f"(-{a})", ba
        if k < 0.75:
            (a, ba) = s.int_(d-1, MAX)
            if ba >= B2: return a, ba
            return f"(-({a}))", ba
        if k < 0.82:
            return s.len_expr()
        if k < 0.87:
            e, b = s.int_(d-1, MAX)
            s.f("int()")
            return f"int(str({e}))", b
        if k < 0.97:
            c = s.call_int(d-1)
            if c: return c
        (a, ba) = s.int_(d-1, 10**6)
        s.f("int()")
        return f"int(\"{s.ch(['12','-7','0','007','-0','99'])}\")", 99
    def divisor(s, ba):
        k = s.r.random()
        if k < 0.5:
            v = s.ch([-7, -3, -2, 1, 2, 3, 7, 10, 3, -5])
            if v == -1 and ba >= B2: v = 2
            return (f"({v})" if v < 0 else str(v)), abs(v)
        e, b = s.int_(1, 1000)
        return f"({e} % 5 + 6)", 10
    def data_int(s):
        c = s.r.random()
        if c < 0.3:
            v = s.vars("li")
            if v:
                n, _ = s.ch(v); return f"{n}[{s.r.randint(0,2)}]", VB
        if c < 0.5:
            v = s.vars("mi")
            if v:
                n, _ = s.ch(v); k = s.ch("abc")
                return (f"{n}.{k}" if s.p() else f"{n}[\"{k}\"]"), VB
        if c < 0.7:
            v = s.vars("rec")
            if v:
                n, _ = s.ch(v)
                return s.ch([f"{n}.n", f"{n}.inner.k", f"{n}.xs[{s.r.randint(0,2)}]",
                             f"{n}[\"inner\"][\"k\"]"]), VB
        if c < 0.82:
            v = s.vars("ll")
            if v:
                n, _ = s.ch(v); return f"{n}[{s.r.randint(0,1)}][{s.r.randint(0,2)}]", VB
        if c < 0.9:
            v = s.vars("lr")
            if v:
                n, _ = s.ch(v); return f"{n}[{s.r.randint(0,2)}].age", VB
        if s.use_else and c < 0.97:
            v = s.vars("li")
            if v:
                n, _ = s.ch(v)
                s.f("else")
                return f"({n}[{s.r.randint(0, 9)}] else {s.r.randint(-3, 3)})".replace("else -", "else -"), VB
        return None
    def len_expr(s):
        r = s.r
        c = r.random()
        if c < 0.4:
            return f"len({s.str_(1)})", 100000
        if c < 0.7:
            return f"len({s.list_any(1)})", 100000
        if c < 0.85:
            return f"len({s.map_any(1)})", 100000
        return f"len({s.ch(['\"\"', '[]', '{}', '\"héllo\"'])})", 6
    def call_int(s, d):
        c = [f for f in s.fns if f[2] == "int"]
        if not c: return None
        name, pts, _, rb = s.ch(c)
        args = s.args(name, pts, d)
        if args is None: return None
        s.f("call:" + name)
        return f"{name}({args})", rb
    def args(s, name, pts, d):
        out = []
        for t in pts:
            if t == "int":
                if name in ("fact",):
                    e, _ = s.int_(d, 1000); out.append(f"({e}) % 21")
                elif name in ("fib",):
                    e, _ = s.int_(d, 1000); out.append(f"({e}) % 12")
                elif name == "pw1":
                    e, _ = s.int_(d, 1000); out.append(f"({e}) % 10")
                elif name == "pw2":
                    e, _ = s.int_(d, 1000); out.append(f"({e}) % 6")
                elif name in ("collatz",):
                    e, _ = s.int_(d, 100000); out.append(f"(({e}) % 50 + 50) % 50 + 1")
                elif name in ("down", "isEven", "isOdd"):
                    e, _ = s.int_(d, 1000); out.append(f"({e}) % 60")
                elif name == "rep":
                    e, _ = s.int_(d, 1000); out.append(f"({e}) % 5")
                else:
                    e, _ = s.int_(d, 10**6); out.append(e)
            elif t == "li": out.append(s.li_(d))
            elif t == "str": out.append(s.str_(d))
            elif t == "mi": out.append(s.mi_(d))
            else: return None
        return ", ".join(out)

    # ---- strings
    def strlit(s):
        s.f("string")
        return s.ch(['"abc"', '"Hello, World"', '""', '"a,b,,c"', '"  two  words\\tand\\nlines "',
                     '"ünï ✓"', '"back\\\\slash"', '"q\\"uote"', '"\\{braces\\}"', '"x"', '"Zebra"',
                     '"apple"', '"app"', '"10"', '"-42"', '"12x"', '"tab\\there"', '"cr\\rlf"',
                     '"line1\\nline2"', '"MiXeD CaSe 123"', '","', '" "'])
    def str_(s, d=2):
        r = s.r; c = r.random()
        if d <= 0 or c < 0.25:
            v = s.vars("str")
            if v and s.p(0.6): return s.ch(v)[0]
            return s.strlit()
        if c < 0.40: return f"({s.str_(d-1)} + {s.str_(d-1)})"
        if c < 0.58: return s.interp(d-1)
        if c < 0.64:
            s.f("str()"); return f"str({s.any_(d-1)})"
        if c < 0.70: return f"{s.ch(['upper', 'lower'])}({s.str_(d-1)})"
        if c < 0.76:
            x = s.str_(d-1); return f"slice({x}, {s.ch(['0','len('+x+') / 3'])}, len({x}))"
        if c < 0.80:
            s.f("str-index"); return f"({s.str_(d-1)} + \"ab\")[{r.randint(0,1)}]"
        if c < 0.86:
            return f"join({s.ls_(d-1)}, {s.ch(['\",\"', '\"\"', '\" - \"'])})"
        if c < 0.90 and s.vars("rec"):
            n = s.ch(s.vars("rec"))[0]; return s.ch([f"{n}.name", f"{n}.inner.tag", f"{n}[\"name\"]"])
        if c < 0.94:
            v = s.vars("lr")
            if v: return f"{s.ch(v)[0]}[{r.randint(0,2)}].name"
        if c < 0.97 and s.use_else:
            s.f("else"); return f"({s.mi_(1)}.{s.ch('abz')}.name else \"?\")" if False else f"(\"k\" + str({s.int_(1,1000)[0]} % 3) else \"z\")" if False else s.interp(d-1)
        return s.interp(d-1)
    def interp(s, d):
        s.f("interp")
        parts = []
        for _ in range(s.r.randint(1, 3)):
            c = s.r.random()
            if c < 0.4: parts.append(s.ch(["v=", "x:", " ", "[", "->", "\\{", "\\}\\\\", ""]))
            elif c < 0.7: parts.append("{" + s.int_(d, 10**6)[0] + "}")
            elif c < 0.85:
                s.f("nested-interp"); parts.append("{" + s.str_(max(d, 1)) + "}")
            else: parts.append("{" + s.any_(max(d-1, 0)) + "}")
        return '"' + "".join(parts) + '"'
    def ls_(s, d=1):
        v = s.vars("ls"); c = s.r.random()
        if v and c < 0.4: return s.ch(v)[0]
        if c < 0.55: s.f("words()"); return f"words({s.str_(d)})"
        if c < 0.7: s.f("split()"); return f"split({s.str_(d)}, {s.ch(['\",\"', '\" \"', '\"a\"'])})"
        if c < 0.8 and s.vars("mi"): return f"keys({s.ch(s.vars('mi'))[0]})"
        return "[" + ", ".join(s.str_(0) for _ in range(s.r.randint(0, 4))) + "]"

    # ---- lists / maps / any
    def li_(s, d=1):
        v = s.vars("li"); c = s.r.random()
        if v and c < 0.4: return s.ch(v)[0]
        if c < 0.55: return f"sort({s.li_(d-1) if d > 0 else '[3, 1, 2]'})"
        if c < 0.65 and d > 0: return f"({s.li_(d-1)} + [{s.int_(1, 1000)[0]}])"
        if c < 0.72 and d > 0: return f"({s.li_(d-1)} + {s.li_(d-1)})"
        if c < 0.78 and d > 0:
            s.f("call:bump"); 
            if any(f[0] == "bump" for f in s.fns): return f"bump({s.li_(d-1)})"
        k = s.r.randint(3, 6)
        return "[" + ", ".join(s.int_(1, 1000)[0] for _ in range(k)) + "]"
    def mi_(s, d=1):
        v = s.vars("mi")
        if v and s.p(0.5): return s.ch(v)[0]
        return "{a: %s, b: %s, c: %s}" % tuple(s.int_(1, 1000)[0] for _ in range(3))
    def list_any(s, d=1):
        c = s.r.random()
        if c < 0.3: return s.li_(d)
        if c < 0.45: return s.ls_(d)
        if c < 0.6:
            x = s.li_(d); s.f("slice()"); return f"slice({x}, 1, len({x}) - 1)"
        if c < 0.7: return "[]"
        if c < 0.8: return s.mixed_list()
        v = s.vars("ll") + s.vars("lr")
        if v: return s.ch(v)[0]
        return s.li_(d)
    def mixed_list(s):
        s.f("mixed-list")
        items = [s.ch(["1", "\"a\"", "nil", "true", "[2, \"b\"]", "{k: 1}", "-3", "[]", "{}", "\"q\\\"t\\n\"",
                       "[[1], [[2]]]", "{x: [1, {y: nil}]}", "false", "\"\""]) for _ in range(s.r.randint(1, 5))]
        return "[" + ", ".join(items) + "]"
    def map_any(s, d=1):
        c = s.r.random()
        v = s.vars("mi") + s.vars("mx") + s.vars("rec")
        if v and c < 0.5: return s.ch(v)[0]
        if c < 0.6: return "{}"
        if c < 0.7: s.f("int-keys"); return "{1: \"a\", -3: true, \"k\": nil, 007: [1]}".replace("007: [1]", "7: [1]")
        if c < 0.8 and s.vars("mi"): return f"remove({s.ch(s.vars('mi'))[0]}, \"{s.ch('abz')}\")"
        return s.mi_(d)
    def bool_(s, d=2):
        r = s.r; c = r.random()
        if d <= 0 or c < 0.2:
            v = s.vars("bool")
            if v and s.p(0.5): return s.ch(v)[0]
            return s.ch(["true", "false"])
        if c < 0.45:
            op = s.ch(["==", "!=", "<", "<=", ">", ">="])
            a = s.int_(d-1, 10**9)[0]; b = s.int_(d-1, 10**9)[0]
            if s.p(0.15):
                a, _ = s.int_(0, MAX); b, _ = s.int_(0, MAX); s.f("big-compare")
            return f"({a} {op} {b})"
        if c < 0.55:
            op = s.ch(["==", "!=", "<", "<=", ">", ">="])
            s.f("str-compare")
            return f"({s.str_(d-1)} {op} {s.str_(d-1)})"
        if c < 0.62:
            op = s.ch(["==", "!=", "<", "<=", ">", ">="])
            s.f("list-compare")
            return f"({s.li_(d-1)} {op} {s.li_(d-1)})"
        if c < 0.68:
            s.f("equality-any")
            return f"({s.any_(d-1)} {s.ch(['==','!='])} {s.any_(d-1)})"
        if c < 0.78:
            s.f("in")
            k = s.r.random()
            neg = "not in" if s.p(0.3) else "in"
            if k < 0.35: return f"({s.int_(1,10)[0]} {neg} {s.li_(d-1)})"
            if k < 0.6: return f"({s.str_(1)} {neg} {s.str_(d-1)})"
            if k < 0.8: return f"({s.ch(['\"a\"','\"zz\"','1','7', '[1]', 'nil'])} {neg} {s.map_any(d-1)})"
            return f"({s.str_(1)} {neg} {s.ls_(d-1)})"
        if c < 0.86: return f"(not {s.bool_(d-1)})"
        if c < 0.95:
            s.f("and/or")
            return f"({s.bool_(d-1)} {s.ch(['and','or'])} {s.bool_(d-1)})"
        s.f("short-circuit")
        return s.ch([f"(false and (1 / {s.zero()} == 0))", f"(true or (1 % {s.zero()} == 0))",
                     f"(true or {s.listoob()})"]) 
    def zero(s): return s.ch(["0", "(1 - 1)", "(2 * 0)"])
    def listoob(s): return "([1][5] == 0)"
    def any_(s, d=1):
        c = s.r.random()
        if c < 0.3: return s.int_(d, MAX)[0]
        if c < 0.45: return s.str_(d)
        if c < 0.55: return s.bool_(d)
        if c < 0.6: return "nil"
        if c < 0.75: return s.list_any(d)
        if c < 0.9: return s.map_any(d)
        return s.mixed_list()

    # ---- statements
    def block(s, n, loop=False):
        s.push(); s.ind += 1
        if loop: s.loop += 1
        for _ in range(n): s.stmt(depth=1)
        if loop: s.loop -= 1
        s.ind -= 1; s.pop()
    def stmt(s, depth=0):
        c = s.r.random()
        kinds = [
            (6, s.st_print), (4, s.st_let_int), (3, s.st_let_str), (2, s.st_let_bool), (3, s.st_let_li),
            (2, s.st_let_ls), (2, s.st_let_mi), (3, s.st_let_rec), (2, s.st_let_ll), (2, s.st_let_lr),
            (2, s.st_let_mx), (5, s.st_assign), (4, s.st_copy), (3, s.st_nested), (3, s.st_call),
            (1, s.st_edge), (2, s.st_cmp), (2, s.st_funcs),
        ]
        if depth < 3:
            kinds += [(4, s.st_if), (3, s.st_for_range), (2, s.st_for_each), (2, s.st_while)]
        if s.loop: kinds += [(2, s.st_brk)]
        tot = sum(w for w, _ in kinds); x = s.r.random() * tot
        for w, fn in kinds:
            x -= w
            if x < 0:
                return fn() if fn not in (s.st_if, s.st_for_range, s.st_for_each, s.st_while) else fn(depth)
        s.st_print()
    def st_print(s):
        n = s.r.randint(1, 4)
        items = []
        for _ in range(n):
            c = s.r.random()
            if c < 0.3: items.append(s.int_(2)[0])
            elif c < 0.5: items.append(s.str_(2))
            elif c < 0.6: items.append(s.bool_(2))
            else: items.append(s.any_(2))
        s.emit("print(" + ", ".join(items) + ")")
        if s.p(0.03): s.emit("print()")
    def st_let_int(s):
        e, b = s.int_(3)
        n = s.fresh("i")
        if b > VB: e = f"({e}) % {VB}" if b < B2 or True else e; b = VB - 1
        if s.p(0.1) and b <= VB:
            pass
        s.emit(f"let {n} = {e}"); s.declare(n, "int", VB)
    def st_edge(s):
        n = s.fresh("big"); e, b = s.edge()
        s.emit(f"let {n} = {e}"); s.declare(n, "big", b)
        s.emit(f"print({n}, {n} == {e}, str({n}), \"{{{n}}}\")")
        if b < MAX and s.p(0.5):
            pass
    def st_let_str(s):
        n = s.fresh("s"); s.emit(f"let {n} = {s.str_(2)}"); s.declare(n, "str")
    def st_let_bool(s):
        n = s.fresh("b"); s.emit(f"let {n} = {s.bool_(2)}"); s.declare(n, "bool")
    def st_let_li(s):
        n = s.fresh("xs"); s.emit(f"let {n} = {s.li_(1) if s.p(0.5) else '[' + ', '.join(s.int_(1,1000)[0] for _ in range(s.r.randint(3,6))) + ']'}")
        s.declare(n, "li")
    def st_let_ls(s):
        n = s.fresh("ws"); s.emit(f"let {n} = {s.ls_(1)}"); s.declare(n, "ls")
    def st_let_mi(s):
        n = s.fresh("m"); s.emit(f"let {n} = {s.mi_(1) if s.p(.3) else '{a: %s, b: %s, c: %s}' % tuple(s.int_(1,1000)[0] for _ in range(3))}")
        s.declare(n, "mi")
    def st_let_rec(s):
        n = s.fresh("r"); s.f("record")
        s.emit(f"let {n} = {{name: {s.str_(1)}, xs: [{s.int_(1,1000)[0]}, {s.int_(1,1000)[0]}, 3], n: {s.int_(1,1000)[0]}, inner: {{k: {s.int_(1,100)[0]}, tag: \"t\"}}}}")
        s.declare(n, "rec")
    def st_let_ll(s):
        n = s.fresh("g"); s.f("nested-list")
        s.emit(f"let {n} = [[1, 2, 3], [{s.int_(1,100)[0]}, 5, 6]]"); s.declare(n, "ll")
    def st_let_lr(s):
        n = s.fresh("people"); s.f("list-of-records")
        s.emit(f"let {n} = [{{name: \"ann\", age: {s.int_(1,90)[0]}}}, {{name: \"bob\", age: 7}}, {{name: {s.str_(0)}, age: 0}}]")
        s.declare(n, "lr")
    def st_let_mx(s):
        n = s.fresh("mx"); s.f("mixed-keys")
        s.emit(f"let {n} = {{}}")
        s.declare(n, "mx")
        for _ in range(s.r.randint(1, 4)):
            k = s.ch(["1", "-5", "\"a\"", "\"k\"", "0", "007", "\"\"", "42"])
            s.emit(f"{n}[{k}] = {s.any_(1)}")
        s.emit(f"print({n}, len({n}), keys({n}), {s.ch(['1', '\"a\"', '0'])} in {n})")
    def st_assign(s):
        v = s.vars("int")
        r = s.r
        if v and s.p(0.7):
            n, _ = s.ch(v)
            c = r.random()
            if c < 0.4:
                e, b = s.int_(2, 10**6); s.emit(f"{n} = {e}")
            else:
                op = s.ch(["+=", "-=", "*=", "/=", "%="])
                if op in ("/=", "%="): e = s.divisor(10**6)[0]
                elif op == "*=": e = s.ch(["2", "3", "(-1)", "0", "1"]) 
                else: e, _ = s.int_(2, 10**6)
                s.emit(f"{n} {op} {e}")
                s.emit(f"{n} %= {VB}")
            s.emit(f"print({n})")
            return
        v = s.vars("str")
        if v:
            n = s.ch(v)[0]
            if s.p(0.5): s.emit(f"{n} += {s.str_(1)}")
            else: s.emit(f"{n} = {s.str_(2)}")
            s.emit(f"print({n}, len({n}))")
            return
        s.st_let_int()
    def st_copy(s):
        r = s.r; c = r.random(); s.f("copy-semantics")
        if c < 0.25 and s.vars("li"):
            a = s.ch(s.vars("li"))[0]; b = s.fresh("cp")
            s.emit(f"let {b} = {a}")
            s.declare(b, "li")
            s.emit(f"{b}[{r.randint(0,2)}] = {s.int_(1,1000)[0]}")
            if s.p(0.5): s.emit(f"{b} += [{r.randint(0,9)}]")
            s.emit(f"print({a}, {b}, {a} == {b})")
        elif c < 0.45 and s.vars("mi"):
            a = s.ch(s.vars("mi"))[0]; b = s.fresh("cm")
            s.emit(f"let {b} = {a}"); s.declare(b, "mi")
            s.emit(f"{b}.{s.ch('abc')} = {s.int_(1,1000)[0]}")
            if s.p(0.5): s.emit(f"{b}[\"extra\"] = [1]")
            s.emit(f"print({a}, {b}, {a} == {b})")
        elif c < 0.65 and s.vars("rec"):
            a = s.ch(s.vars("rec"))[0]; b = s.fresh("cr")
            s.emit(f"let {b} = {a}"); s.declare(b, "rec")
            s.emit(f"{b}.xs[{r.randint(0,2)}] = 99")
            s.emit(f"{b}.inner.k += 1")
            s.emit(f"print({a}, {b})")
        elif c < 0.8 and s.vars("ll"):
            a = s.ch(s.vars("ll"))[0]; b = s.fresh("cg")
            s.emit(f"let {b} = {a}"); s.declare(b, "ll")
            s.emit(f"{b}[1][0] = -1")
            s.emit(f"let inner{b} = {a}[1]")
            s.emit(f"inner{b}[2] = 77")
            s.emit(f"print({a}, {b}, inner{b})")
        elif c < 0.9 and s.vars("li") and s.vars("mi"):
            xs = s.ch(s.vars("li"))[0]; m = s.ch(s.vars("mi"))[0]; t = s.fresh("cm")
            s.emit(f"let {t} = {{items: {xs}, m: {m}}}")
            s.emit(f"{xs}[0] = 555")
            s.emit(f"{t}.m.a = 556")
            s.emit(f"print({t}, {xs}, {m})")
        else:
            xs = s.fresh("lp")
            s.emit(f"let {xs} = [1, 2, 3]")
            s.declare(xs, "li")
            s.emit(f"for x{xs} in {xs} {{")
            s.emit(f"  {xs} += [x{xs} * 10]")
            s.emit(f"  {xs}[0] += 1")
            s.emit("}")
            s.emit(f"print({xs})")
    def st_nested(s):
        r = s.r; c = r.random(); s.f("nested-update")
        if c < 0.25 and s.vars("rec"):
            n = s.ch(s.vars("rec"))[0]
            p = s.ch([f"{n}.n", f"{n}.xs[{r.randint(0,2)}]", f"{n}.inner.k", f"{n}[\"inner\"][\"k\"]"])
            op = s.ch(["=", "+=", "-="])
            e = s.int_(1, 1000)[0]
            s.emit(f"{p} {op} {e}")
            s.emit(f"{p} %= {VB}")
            s.emit(f"print({n})")
        elif c < 0.4 and s.vars("rec"):
            n = s.ch(s.vars("rec"))[0]
            s.emit(f"{n}.{s.ch(['extra','tag2'])} = {s.any_(1)}")
            s.emit(f"{n}.inner[{s.ch(['\"z\"', '5', '-1'])}] = {s.any_(1)}")
            s.emit(f"print({n}, len({n}), keys({n}))")
        elif c < 0.55 and s.vars("lr"):
            n = s.ch(s.vars("lr"))[0]
            i = r.randint(0, 2)
            s.emit(f"{n}[{i}].age += {s.int_(1, 100)[0]}")
            s.emit(f"{n}[{i}].tags = [{i}, \"t\"]")
            s.emit(f"{n}[{i}].tags[1] = \"u\"")
            s.emit(f"{n}[{i}].name += \"!\"" if False else f"{n}[{i}].name = {s.str_(0)}")
            s.emit(f"print({n}, {n}[{i}].tags)")
            tt = s.fresh("tot"); pp = s.fresh("p"); s.emit(f"let {tt} = 0")
            s.emit(f"for p in {n} {{ tot{s.n} += p.age }}" if False else f"for p{s.n} in {n} {{")
            s.emit(f"  {tt} += {pp}.age")
            s.emit("}")
            s.emit(f"print({tt})")
        elif c < 0.7 and s.vars("ll"):
            n = s.ch(s.vars("ll"))[0]
            s.emit(f"{n}[{r.randint(0,1)}][{r.randint(0,2)}] = {s.int_(1,100)[0]}")
            s.emit(f"{n}[{r.randint(0,1)}][{r.randint(0,2)}] *= 2")
            s.emit(f"print({n})")
        elif c < 0.85 and s.vars("mx"):
            n = s.ch(s.vars("mx"))[0]
            k = s.ch(["1", "\"a\"", "-5", "\"new\"", "99"])
            s.emit(f"{n}[{k}] = {s.any_(1)}")
            if s.p(0.5): s.emit(f"{n} = remove({n}, {s.ch(['1', '\"a\"', '-5', '\"nokey\"', '[1]'])})")
            s.emit(f"print({n}, len({n}))")
            kk = s.fresh("mk")
            s.emit(f"for {kk} in {n} {{")
            s.emit(f"  print({kk}, {n}[{kk}])")
            s.emit("}")
        elif s.vars("mi"):
            n = s.ch(s.vars("mi"))[0]
            s.emit(f"{n}[\"{s.ch('abc')}\"] {s.ch(['+=','-=','*='])} {s.ch(['2','3','1'])}")
            s.emit(f"print({n})")
            s.emit(f"{n} = remove({n}, \"{s.ch('abz')}\")")
            s.emit(f"print({n}, keys({n}))")
            s.emit(f"{n}.a = 1")
            s.emit(f"{n}.b = 2")
            s.emit(f"{n}.c = 3")
        else:
            s.st_print()
    def st_call(s):
        fs = [f for f in s.fns if f[2] != "int"]
        if not fs: return s.st_print()
        name, pts, rt, _ = s.ch(fs)
        a = s.args(name, pts, 1)
        if a is None: return s.st_print()
        s.f("call:" + name)
        s.emit(f"print({name}({a}))" if s.p(0.8) else f"{name}({a})")
    def st_cmp(s):
        s.f("cmp-matrix")
        a = s.ch(["-1", "0", "1", "2", "10"]); b = s.ch(["-1", "0", "1", "2", "10"])
        s.emit(f"print({a} < {b}, {a} <= {b}, {a} == {b}, {a} != {b}, {a} > {b}, {a} >= {b})")
        x = s.strlit(); y = s.strlit()
        s.emit(f"print({x} < {y}, {x} <= {y}, {x} == {y}, {x} > {y}, {x} in {y})")
        s.emit(f"print([1, 2] < [1, 2, 0], [1, 3] < [1, 2, 9], [] < [0], [[1]] == [[1]], 1 == \"1\", nil == nil, [] == {{}}, {{a: 1, b: 2}} == {{b: 2, a: 1}})")
        s.emit(f"print(-7 / 2, -7 % 2, 7 / -2, 7 % -2, -7 / -2, -7 % -2, 0 / -5, 0 % -5, {MAX} / -1, {MINS} % -1)")
    def st_funcs(s):
        r = s.r; c = r.random()
        s.f("builtins")
        if c < 0.15: s.emit(f"print(sort({s.ch(['[3, 1, 2]', '[\"b\", \"a\", \"B\"]', '[[2], [1, 5], [1]]', '[]', '[-1, 0, -5, 5]', '[2, 2, 1]'])}))")
        elif c < 0.3: s.emit(f"print(slice({s.ch(['\"hello\"', '[1,2,3,4]', '\"\"'])}, 0, 0), slice({s.ch(['\"hello\"', '[1,2,3,4]'])}, 1, 3), slice(\"abc\", 3, 3))")
        elif c < 0.45: s.emit(f"print(words(\"  a  b\\tc\\n\"), words(\"\"), words({s.str_(1)}), split(\"a,,b\", \",\"), split(\"\", \",\"), split(\"abc\", \"abc\"))")
        elif c < 0.55: s.emit(f"print(join([\"a\", \"b\"], \"-\"), join([], \",\"), join([\"x\"], \"\"), upper(\"aZ-é\"), lower(\"AZ-É\"))")
        elif c < 0.7: s.emit(f"print(int(\"-0\"), int(\"007\"), int(\"9223372036854775807\"), int(\"-9223372036854775808\"), int(\"0\"))")
        elif c < 0.8: s.emit(f"print(str(nil), str(true), str([\"a\\\\b\", \"c\\nd\", \"e\\\"f\", \"t\\tr\\r\"]), str({{a: \"x\", 1: [nil]}}), str(\"s\"), str(-5))")
        elif c < 0.9: s.emit(f"print(len(\"héllo\"), len([[]]), len({{}}), keys({{b: 1, a: 2}}), remove({{a: 1}}, \"a\"), remove({{a: 1}}, [1]), remove({{a: 1}}, \"z\"))")
        else: s.emit(f"print(\"{{1 + 1}} {{\"in{{2}}\"}} \\{{x\\}} {{[1, \"a\"]}} {{{{k: 1}}}} {{nil}} {{true}}\")")
    def st_if(s, depth):
        s.f("if")
        s.emit(f"if {s.bool_(2)} {{"); s.block(s.r.randint(1, 3))
        while s.p(0.35):
            s.emit(f"}} else if {s.bool_(1)} {{"); s.block(s.r.randint(1, 2))
        if s.p(0.6):
            s.emit("} else {"); s.block(s.r.randint(1, 3))
        s.emit("}")
    def st_for_range(s, depth):
        s.f("for-range")
        i = s.fresh("k"); r = s.r; c = r.random()
        if c < 0.3:
            a = s.int_(1, 1000)[0]; hdr = f"{a}..({a}) + {r.randint(0, 6)}"
        elif c < 0.5: hdr = f"0..({s.int_(1, 1000)[0]}) % 7"
        elif c < 0.65: hdr = f"{r.randint(-4, 0)}..={r.randint(-1, 4)}"
        elif c < 0.75: hdr = f"5..={r.randint(0, 3)}"
        elif c < 0.85 and s.vars("li"): hdr = f"0..len({s.ch(s.vars('li'))[0]})"
        elif c < 0.9: hdr = f"3..3"
        else: hdr = f"1..={r.randint(1, 8)}"
        s.emit(f"for {i} in {hdr} {{")
        s.push(); s.declare(i, "int", 1000); s.ind += 1; s.loop += 1
        s.emit(f"print(\"{i}\", {i}, {i} * {i} % 7)")
        for _ in range(s.r.randint(0, 2)): s.stmt(depth + 1)
        s.loop -= 1; s.ind -= 1; s.pop(); s.emit("}")
        if s.p(0.2): s.emit(f"let {i} = 0"); s.declare(i, "int", VB)
    def st_for_each(s, depth):
        s.f("for-each")
        i = s.fresh("e"); c = s.r.random()
        if c < 0.35 and s.vars("li"): src, t = s.ch(s.vars("li"))[0], "int"
        elif c < 0.55: src, t = s.str_(1), "str"
        elif c < 0.7: src, t = s.ls_(1), "str"
        elif c < 0.85: src, t = s.map_any(1), "any"
        else: src, t = s.li_(1), "int"
        s.emit(f"for {i} in {src} {{")
        s.push(); s.ind += 1; s.loop += 1
        if t == "int": s.declare(i, "int", VB)
        elif t == "str": s.declare(i, "str")
        s.emit(f"print({i})")
        for _ in range(s.r.randint(0, 2)): s.stmt(depth + 1)
        s.loop -= 1; s.ind -= 1; s.pop(); s.emit("}")
    def st_while(s, depth):
        s.f("while")
        w = s.fresh("w"); s.emit(f"let {w} = 0"); s.declare(w, "ctr", 20)
        s.emit(f"while {w} < {s.r.randint(2, 6)} {{")
        s.push(); s.ind += 1; s.loop += 1
        s.emit(f"{w} += 1")
        if s.p(0.4): s.emit(f"if {w} == 2 {{ continue }}" if False else f"if {w} % 2 == 0 {{\n{'  '*(s.ind+1)}continue\n{'  '*s.ind}}}")
        s.emit(f"print(\"{w}\", {w})")
        for _ in range(s.r.randint(0, 2)): s.stmt(depth + 1)
        if s.p(0.3): s.emit(f"if {w} >= 4 {{\n{'  '*(s.ind+1)}break\n{'  '*s.ind}}}")
        s.loop -= 1; s.ind -= 1; s.pop(); s.emit("}")
    def st_brk(s):
        s.f("break/continue")
        s.emit(f"if {s.bool_(1)} {{\n{'  '*(s.ind+1)}{s.ch(['break', 'continue'])}\n{'  '*s.ind}}}")

# ---- function library (text, signature)
LIB = {
 "fact": ("fn fact(n) {\n  if n <= 1 {\n    return 1\n  }\n  return n * fact(n - 1)\n}", ["int"], "int", 2432902008176640000),
 "fib": ("fn fib(n) {\n  if n < 2 { return n }\n  return fib(n - 1) + fib(n - 2)\n}", ["int"], "int", 100),
 "gcd": ("fn gcd(a, b) {\n  while b != 0 {\n    let t = b\n    b = a % b\n    a = t\n  }\n  return a\n}", ["int", "int"], "int", VB),
 "pw1": None,
 "collatz": ("fn collatz(n) {\n  let steps = 0\n  while n != 1 {\n    if n % 2 == 0 { n = n / 2 } else { n = 3 * n + 1 }\n    steps += 1\n  }\n  return steps\n}", ["int"], "int", 1000),
 "down": ("fn down(n) {\n  if n <= 0 { return 0 }\n  return 1 + down(n - 1)\n}", ["int"], "int", 1000),
 "isEven": ("fn isEven(n) {\n  if n == 0 { return true }\n  if n < 0 { return isEven(-n) }\n  return isOdd(n - 1)\n}\nfn isOdd(n) {\n  if n == 0 { return false }\n  if n < 0 { return isOdd(-n) }\n  return isEven(n - 1)\n}", ["int"], "bool", 0),
 "sumlist": ("fn sumlist(xs) {\n  let t = 0\n  for x in xs { t += x }\n  return t\n}", ["li"], "int", 10**9),
 "rsum": ("fn rsum(xs, i) {\n  if i >= len(xs) { return 0 }\n  return xs[i] + rsum(xs, i + 1)\n}", None, "int", 10**9),
 "bump": ("fn bump(xs) {\n  xs[0] += 1\n  xs += [len(xs)]\n  return xs\n}", ["li"], "li", 0),
 "show": ("fn show(x) {\n  print(\"show:\", x)\n}", ["int"], "nil", 0),
 "rev": ("fn rev(s) {\n  let r = \"\"\n  for c in s { r = c + r }\n  return r\n}", ["str"], "str", 0),
 "rep": ("fn rep(s, n) {\n  let r = \"\"\n  for i in 0..n { r += s }\n  return r\n}", None, "str", 0),
 "count": ("fn count(xs, x) {\n  let c = 0\n  for y in xs { if y == x { c += 1 } }\n  return c\n}", None, "int", 1000),
 "classify": ("fn classify(n) {\n  if n < 0 { return \"neg\" } else if n == 0 { return \"zero\" }\n  return \"pos\"\n}", ["int"], "str", 0),
 "mutm": ("fn mutm(m) {\n  m.a = 100\n  m[\"zz\"] = 1\n  return m\n}", ["mi"], "map", 0),
 "swap": ("fn swap(a, b) {\n  let t = a\n  a = b\n  b = t\n  return [a, b]\n}", ["int", "int"], "li", 0),
 "early": ("fn early(n) {\n  for i in 0..10 {\n    if i == n { return i * 2 }\n  }\n  return -1\n}", ["int"], "int", 100),
 "fnl": ("fn fnl(n) {\n  if n > 0 { return }\n  print(\"fnl\", n)\n}", ["int"], "nil", 0),
}

def gen_fn(s, k):
    """a random generic function over two ints returning int"""
    g = G(s.r.random(), s.use_else); g.r = s.r; g.use_else = s.use_else
    g.n = 1000 * (k + 1); g.fns = []
    g.env = [[("a", "int", VB), ("b", "int", VB)]]
    g.out = []; g.ind = 1
    name = f"g{k}"
    for _ in range(s.r.randint(2, 5)): g.stmt(depth=2)
    e, _ = g.int_(2, 10**6)
    g.emit(f"return ({e}) % {VB}")
    s.feat |= g.feat
    return f"fn {name}(a, b) {{\n" + "\n".join(g.out) + "\n}", (name, ["int", "int"], "int", VB)

def inject_fault(s, r):
    nm = lambda: s.ch(s.vars("mi"))[0] if s.vars("mi") else "{a: 1, b: 2, c: 3}"
    li = lambda: s.ch(s.vars("li"))[0] if s.vars("li") else "[1, 2, 3]"
    ss = lambda: s.ch(s.vars("str"))[0] if s.vars("str") else "\"abc\""
    z = s.zero()
    opts = [
     ("overflow-add", f"print({MAX} + 1)"), ("overflow-sub", f"print({MINS} - 1)"),
     ("overflow-mul", f"print(4294967296 * 2147483648)"), ("overflow-neg", f"print(-{MINS})"),
     ("overflow-div", f"print({MINS} / -1)"), ("overflow-mulneg", f"print({MINS} * -1)"),
     ("overflow-compound", f"let q = {MAX}\nq += 1"), ("overflow-fact", "print(fact(21))" if "fact" in LIBUSED else f"print({MAX} * 2)"),
     ("overflow-big", f"let q = 3037000500\nprint(q * q)"),
     ("divzero", f"print(5 / {z})"), ("modzero", f"print(5 % {z})"), ("divzero-compound", f"let q = 3\nq /= {z}"),
     ("missing-key", f"print({nm()}.zz)"), ("missing-key2", f"print({nm()}[\"q\"])"),
     ("missing-int-key", "print({a: 1}[7])"),
     ("oob", f"print({li()}[10])"), ("oob-neg", f"print({li()}[-1])"), ("oob-str", f"print(\"abc\"[3])"),
     ("oob-assign", f"let q = [1, 2]\nq[2] = 0"),
     ("type-add", "print(1 + \"a\")"), ("type-sub", "print(\"a\" - 1)"), ("type-neg", "print(-\"s\")"),
     ("type-not", "print(not 1)"), ("type-and", "print(1 and true)"), ("type-or", "print(false or 0)"),
     ("type-if", "if 1 {\n  print(1)\n}"), ("type-while", "while \"x\" {\n  print(1)\n}"),
     ("type-cmp", "print([1] < 2)"), ("type-cmp2", "print(1 < \"a\")"), ("type-cmp3", "print([1, \"a\"] < [1, 2])"),
     ("type-in", "print(1 in 5)"), ("type-in2", "print(1 in \"abc\")"), ("type-for", "for x in 5 {\n  print(x)\n}"),
     ("type-len", "print(len(5))"), ("type-int", "print(int(5))"), ("type-keys", "print(keys([1]))"),
     ("type-sort", "print(sort([1, \"a\"]))"), ("type-sort2", "print(sort([\"a\", 2, 1]))"),
     ("type-field", "print([1].x)"), ("type-index", "print(5[0])"), ("type-index2", "print(true[0])"),
     ("type-listidx", f"print({li()}[\"a\"])"), ("type-mapkey", f"print({nm()}[[1]])"),
     ("type-assign-str", f"let q = \"abc\"\nq[0] = \"x\""), ("type-assign-field", "let q = [1]\nq.a = 1"),
     ("type-assign-mapkey", "let q = {}\nq[[1]] = 1"), ("assign-int", "let q = 5\nq.a = 1"),
     ("range-str", "for i in \"a\"..3 {\n  print(i)\n}"), ("range-str2", "for i in 1..=nil {\n  print(i)\n}"),
     ("slice-oob", "print(slice([1, 2, 3], 2, 9))"), ("slice-rev", "print(slice(\"abc\", 2, 1))"),
     ("slice-neg", "print(slice(\"abc\", -1, 2))"), ("slice-type", "print(slice(5, 0, 1))"),
     ("slice-type2", "print(slice(\"abc\", \"a\", 1))"),
     ("split-empty", "print(split(\"abc\", \"\"))"), ("join-bad", "print(join([1, 2], \",\"))"),
     ("join-bad2", "print(join(\"ab\", \",\"))"), ("join-bad3", "print(join([\"a\"], 1))"),
     ("fail", "fail(\"boom\")"), ("fail2", "fail([1, \"a\"])"), ("fail3", "fail(42)"),
     ("int-bad", "print(int(\"12x\"))"), ("int-bad2", "print(int(\"\"))"), ("int-bad3", "print(int(\"+5\"))"),
     ("int-bad4", "print(int(\" 5\"))"), ("int-bad5", "print(int(\"9223372036854775808\"))"),
     ("int-bad6", "print(int(\"1_0\"))"), ("int-bad7", "print(int(\"-\"))"),
     ("upper-type", "print(upper(5))"), ("words-type", "print(words(nil))"), ("remove-type", "print(remove([1], 1))"),
     ("compound-missing", "let q = {}\nq.a += 1"), ("compound-str", "let q = 1\nq += \"a\""),
     ("compound-oob", "let q = [1]\nq[3] += 1"), ("compound-type", "let q = \"s\"\nq -= 1"),
     ("path-missing", "let q = {a: 1}\nq.b.c = 1"), ("path-oob", "let q = [[1]]\nq[1][0] = 1"),
     ("path-type", "let q = {a: 1}\nq.a.c = 1"),
     ("print-in-fault", f"print(\"before\", {ss()})\nprint(1 / {z})"),
     ("down-overflow", "print(down(1000))" if "down" in LIBUSED else None),
     ("stack-overflow2", "print(down(5000))" if "down" in LIBUSED else None),
     ("not-in-fault", "print(1 not in 5)"), ("neg-index-str", "print(\"abc\"[-1])"),
     ("cond-order", "print([][0] + (1 / 0))"), ("arg-order", f"print(1 / {z}, [][0])"),
     ("mixed-eq-then-fault", "print([1] == [1], 1 % 0)"),
     ("interp-fault", "print(\"a{1 / 0}b{[][2]}\")"), ("interp-fault2", "print(\"x{[1][5]}\")"),
     ("in-fault-first", "print(1 in {a: 1}, [1] in \"abc\")"),
     ("list-add", "print([1] + 1)"), ("str-add", "print(\"a\" + [1])"), ("nil-add", "print(nil + nil)"),
     ("map-add", "print({} + {})"), ("bool-add", "print(true + true)"), ("cmp-nil", "print(nil < nil)"),
     ("cmp-bool", "print(true < false)"), ("cmp-map", "print({} < {})"),
     ("recursion-in-fn-missing", "fn badf(m) {\n  return m.nope\n}\nprint(badf({a: 1}))") ,
     ("mapkey-order", "let q = {b: 1}\nq.a = 2\nprint(q.c)"),
     ("index-float", "print([1, 2][1 - 2])"),
     ("minus-min", f"let q = {MINS}\nprint(-q)"), ("abs-min", f"let q = {MINS}\nprint(q - 1)"),
     ("neg-range-bound", "for i in 0..[1] {\n  print(i)\n}"),
     ("mod-min", f"print(5 % ({MINS} + 1 - 1 - {MINS} + {MINS} - {MINS} + {MAX} - {MAX}))"),
    ]
    opts = [o for o in opts if o[1] is not None]
    kind, text = s.ch(opts)
    s.f("FAULT:" + kind)
    return text

def inject_compile(s, use_else):
    opts = [
     "print(undefined_var)", "let zz = 1\nlet zz = 2", "print(1 < 2 < 3)", "x = 1", "return 5",
     "break", "continue", "let f1 = 1\nprint(nofunc(1))", "print(len())", "print(len(1, 2))",
     "print(12ab)", "print(99999999999999999999)", "print(\"bad\\q\")", "print(\"unterminated)",
     "if true {\n  fn inner() {\n  }\n}", "print({a: 1, a: 2})", "print(\"{}\")", "1 + 2", "f(x) = 1",
     "1 = 2", "print(print)", "let if = 1", "print(@)", "let a b", "while true print(1)", "print((1)",
     "fn print() {\n}", "fn dup() {\n}\nfn dup() {\n}", "fn pp(a, a) {\n}", "print(\"{1 + }\")",
     "let q = q + 1", "for i in 1..3 {\n  let i = 2\n}", "print(1_)", "print(1__0)", "let 1x = 2",
     "print(not)", "print(1 == not true)", ";", "let x = 1;;", "{ print(1) }", "print({1 + 2: 3})",
     "print({a 1})", "if 1 == 1 print(1)", "else { }", "print(\"a\\\"", "print('c')", "print(1 $ 2)",
     "print(\"{\\\"x\\\"}\")" , "fn fq() {\n  return topv\n}\nlet topv = 1\nfq()", "print(1 +)", "print(,)",
     "for i in 0..3\n{\n}", "let t = nil\nt.x.y = ", "let c1 = 1\nc1()", "print(0..3)", "x += 1",
     "let ww = {\n  a: 1,\n  b: 2,\n}\nprint(ww)",  # valid -- not an error (control)
     "print(\x01)", "print(é)",
    ]
    if use_else:
        opts += ["print(1 else 2)", "print((1 + 2) else 3)", "let q = [1]\nprint(len(q) else 0)"]
    t = s.ch(opts)
    s.f("COMPILE:" + t.split("\n")[0][:30])
    return t

LIBUSED = set()

def main():
    seed = int(sys.argv[1]); use_else = "--else" in sys.argv[2:]
    s = G(seed, use_else); r = s.r
    kind_roll = r.random()
    mode = "fault" if kind_roll < 0.15 else "compile" if kind_roll < 0.20 else "ok"
    names = [n for n in LIB if LIB[n]]
    chosen = r.sample(names, r.randint(4, 9))
    if "isEven" in chosen: chosen.append("isOdd") if False else None
    LIBUSED.clear(); LIBUSED.update(chosen)
    fn_texts = []
    for n in chosen:
        t, pts, rt, rb = LIB[n]
        fn_texts.append(t)
        if n == "rsum": s.fns.append(("rsum", ["li", "int0"], "int", rb)); continue
        if n == "rep": s.fns.append(("rep", ["str", "int"], "str", 0)); continue
        if n == "count": s.fns.append(("count", ["li", "int"], "int", 1000)); continue
        if n == "isEven": s.fns.append(("isEven", pts, "bool", 0)); continue
        s.fns.append((n, pts, rt, rb))
    # rsum / count special args
    for k in range(r.randint(0, 2)):
        t, sig = gen_fn(s, k); fn_texts.append(t); s.fns.append(sig)
    # fix pseudo-types
    fixed = []
    for f in s.fns:
        if f[0] == "rsum":
            fixed.append(f)
        else: fixed.append(f)
    s.fns = [f for f in fixed if f[0] != "rsum"]   # rsum handled in statements below
    s.fns = [f for f in s.fns if f[0] not in ("isEven",)]
    s.fns = [f for f in s.fns if f[0] not in ("rep",)]
    s.fns = [f for f in s.fns if f[0] not in ("count",)]
    # place functions: some above, some below
    above = [t for t in fn_texts if r.random() < 0.5]; below = [t for t in fn_texts if t not in above]
    out = ["// seed %d" % seed]
    out += above
    body_n = r.randint(18, 40)
    fault_at = r.randrange(body_n) if mode != "ok" else -1
    for i in range(body_n):
        s.out = []; s.ind = 0
        if i == fault_at:
            if mode == "fault": s.out.append(inject_fault(s, r))
            else: s.out.append(inject_compile(s, use_else))
        else:
            s.stmt(0)
        out += s.out
        if i % 7 == 6 and "rsum" in chosen:
            if s.vars("li"):
                xs = s.ch(s.vars("li"))[0]; out.append(f"print(rsum({xs}, 0))")
        if i % 9 == 4:
            if "rep" in chosen: out.append(f"print(rep({s.str_(0)}, {r.randint(0, 4)}))")
            if "count" in chosen: out.append(f"print(count([1, 2, 1, 3, 1], {r.randint(0, 3)}), count([\"a\", \"b\"], \"a\"), count([[1], [1]], [1]))")
            if "isEven" in chosen: out.append(f"print(isEven({r.randint(-5, 40)}), isOdd({r.randint(0, 31)}))")
            if "down" in chosen: out.append(f"print(down({s.ch([0, 1, 10, 500, 999])}))")
            if "show" in chosen: out.append(f"print(show({r.randint(0, 9)}))")
            if "fnl" in chosen: out.append(f"print(fnl({r.randint(-1, 1)}))")
            if "fact" in chosen: out.append(f"print(fact({s.ch([0, 1, 5, 20, -3])}))")
            if "mutm" in chosen and s.vars("mi"):
                m = s.ch(s.vars("mi"))[0]; out.append(f"print({m}, mutm({m}), {m})")
            if "swap" in chosen: out.append(f"print(swap({r.randint(0,9)}, {r.randint(0,9)}))")
            if "bump" in chosen and s.vars("li"):
                xs = s.ch(s.vars("li"))[0]; out.append(f"print({xs}, bump({xs}), {xs})")
            if "rev" in chosen: out.append(f"print(rev({s.str_(0)}), rev(\"\"))")
            if "classify" in chosen: out.append(f"print(classify({r.randint(-2, 2)}))")
            if "early" in chosen: out.append(f"print(early({r.randint(-1, 12)}))")
            if "pw" in chosen: pass
    out += below
    sys.stdout.write("\n".join(out) + "\n")
    # features to stderr is avoided; written via env if requested
    import os
    if os.environ.get("GEN_FEATURES"):
        with open(os.environ["GEN_FEATURES"], "w") as fh:
            fh.write(mode + "\n" + "\n".join(sorted(s.feat)) + "\n")

main()
