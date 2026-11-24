# The script an adversarial review of the first draft used to check D23's Int
# half against perl 5.38.2: 6,286 lines of + - * % and unary minus over the
# edge values, every one agreeing with Python's integers. Kept as a starting
# point for step 1's model (t/models/arith.py), which it is not: it writes no
# test files, and it takes its expected values and perl's in one run.
import subprocess, itertools
M = 2**63
vals = sorted(set([0,1,-1,2,-2,3,-3,7,-7,10, 2**31-1,2**31,2**31+1,-2**31, 2**32-1,2**32,2**32+1,-2**32, 3037000499,3037000500,-3037000500, 2**53-1,2**53,2**53+1,-(2**53),-(2**53)-1, 2**62-1, 2**62, 2**62+1, -(2**62), M-2, M-1, -(M-1), -M, 4611686018427387904, 6074001000, 1518500250, 4294967295*2+1, 9223372036854775807//3, 9223372036854775807//7, 1000000007, -1000000007, 10**15, 10**15+1, 10**18]))
def lit(v):
    if v == -M: return "(-9223372036854775807 - 1)"
    return f"({v})" if v < 0 else str(v)
lines=[]; exp=[]
ops = {'+': lambda a,b: a+b, '-': lambda a,b: a-b, '*': lambda a,b: a*b, '%': lambda a,b: a % b if b != 0 else None}
for a,b in itertools.product(vals, vals):
    for op,f in ops.items():
        r = f(a,b)
        if r is None or not (-M <= r < M): continue
        lines.append(f"say({lit(a)} {op} {lit(b)});"); exp.append(str(r))
for a in vals:
    if -M <= -a < M:
        lines.append(f"say(-{lit(a)});"); exp.append(str(-a))
src = "use v5.36;\n" + "\n".join(lines) + "\n"
open("arith_gen.pl","w").write(src)
p = subprocess.run(["perl","-CSDA","arith_gen.pl"],capture_output=True,text=True)
out = p.stdout.split("\n")[:-1]
print("lines", len(lines), "perl exit", p.returncode, "stderr bytes", len(p.stderr))
print(p.stderr[:500])
bad = [(l,e,o) for l,e,o in zip(lines,exp,out) if e!=o]
print("mismatches", len(bad))
for b in bad[:30]: print(b)
