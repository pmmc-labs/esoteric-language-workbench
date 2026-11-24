#!/usr/bin/env python3
"""Does perl read a decimal literal to the same double the C library (and
Python, and JavaScript) does? And does it print a double as C's %.15g
does, with `0` for either zero and `Inf` for an infinity? Step 2's
proposal assumes both; on the cloud machine's perl 5.42.0 both hold for
60,029 literals. Run it on any new machine before trusting a float there:

    python3 docs/briefs/step2-literals.py

Not part of make test.
"""
import math, os, random, struct, subprocess, sys, tempfile
P = os.environ.get('CURLY_PERL', 'perl')
os.chdir(tempfile.mkdtemp())
rng = random.Random(2)
lits = ['0.1', '0.2', '0.3', '1e23', '1e22', '9007199254740993.0', '9007199254740993e0', '1.7976931348623157e308', '4.9e-324',
        '2.2250738585072011e-308', '2.2250738585072014e-308', '0.000001', '123456789012345678901234567890.0', '1e-5', '5e-324',
        '1.0000000000000002', '1.00000000000000011102230246251565404236316680908203125', '1.00000000000000011102230246251565404236316680908203126',
        '9223372036854775808.0', '18446744073709551615.0', '18446744073709551616.0', '0.30000000000000004', '8.41e21', '1e15', '1e16', '.5', '5.', '1e+3', '1E3']
for _ in range(60000):
    digits = rng.randrange(1, 22)
    mant = ''.join(rng.choice('0123456789') for _ in range(digits)).lstrip('0') or '1'
    k = rng.randrange(0, len(mant) + 1)
    s = (mant[:k] or '0') + '.' + (mant[k:] or '0')
    if rng.random() < 0.6:
        s += 'e' + str(rng.randrange(-330, 310))
    lits.append(s)
src = 'use v5.42;\nno warnings;\n' + ''.join(f'say unpack("H16", pack "d>", {l}), " ", {l};\n' for l in lits)
open('atof.pl', 'w').write(src)
out = subprocess.run([P, 'atof.pl'], capture_output=True, text=True)
assert out.returncode == 0, out.stderr[:500]
rows = out.stdout.split('\n')[:-1]
bits_differ = print_differ = 0
shown = 0
for l, row in zip(lits, rows):
    hexbits, printed = row.split(' ')
    want = struct.pack('>d', float(l)).hex()
    x = struct.unpack('>d', bytes.fromhex(hexbits))[0]
    if hexbits != want:
        bits_differ += 1
        if shown < 8: print('literal', l, 'perl', hexbits, 'correctly rounded', want); shown += 1
    c = 'Inf' if x == math.inf else '-Inf' if x == -math.inf else ('0' if x == 0 else '%.15g' % x)
    if printed != c:
        print_differ += 1
        if print_differ < 8: print('print', hexbits, 'perl', printed, '%.15g', c)
print(len(lits), 'literals:', bits_differ, 'read to another double than correct rounding;', print_differ, 'printed otherwise than %.15g')
sys.exit(1 if bits_differ or print_differ else 0)
