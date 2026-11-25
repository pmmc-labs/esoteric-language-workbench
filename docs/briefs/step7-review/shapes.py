#!/usr/bin/env python3
"""Every line of the generated C of every golden test, against the shapes
the proposal's third place needs (`python3 shapes.py WORK/c`):

  - a runtime call that gives a value is the whole right side of an
    assignment to a temporary or a variable;
  - its arguments are a temporary, a variable, what a pointer points at,
    or a constant made in place (rt_int, rt_num_bits, rt_string, rt_undef,
    rt_bool): never another call's result;
  - a pointer is set to the address of a temporary or a variable, never
    of anything else.

Anything else is printed. It reads C and runs nothing, so it says only
what the code generator wrote for these programs, not what it could."""
import os
import re
import sys

ATOM = r'(?:t\d+|v\d+_\w+|\(\*p\d+\)|rt_int\(INT64_C\(\d+\)\)|rt_num_bits\(UINT64_C\(0x[0-9a-f]+\)\)|rt_string\(&s\d+\)|rt_undef\(\)|rt_bool\([01]\))'
PLACE = r'(?:t\d+|v\d+_\w+)'
SHAPES = [re.compile(s) for s in [
    rf'{PLACE} = rt_\w+\(cx(?:, {ATOM})+\);',                   # an operation, stored
    rf'{PLACE} = {ATOM};',                                      # a copy
    rf'p\d+ = &(?:{PLACE}|\(\*p\d+\));',                        # a pointer to a place
    rf'if \(rt_is_(?:true|false|undef)\(cx, (?:{ATOM}|\*p\d+)\)\) (?:\{{|break;)',
    rf'rt_(?:say|print)\(cx, {ATOM}\);',
    r'rt_use_open\(cx\);',
    r'rt_value t\d+ RT_UNUSED;',
    r'rt_value \*p\d+ RT_UNUSED;',
    r'rt_value v\d+_\w+ RT_UNUSED = rt_undef\(\);',
    r'cx->line = \d+;',
    r'\(void\)cx;',
    r'for \(;;\) \{', r'\{', r'\}', r'\} else \{',
    r'goto (?:next|last)_\d+;', r'(?:next|last)_\d+: RT_UNUSED;',
]]

lines = other = 0
kinds = {}
for name in sorted(os.listdir(sys.argv[1])):
    inside = False
    for line in open(os.path.join(sys.argv[1], name)):
        line = line.strip()
        if line.startswith('static void curly_main'):
            inside = True
            continue
        if line.startswith('int main(void)'):
            inside = False
        if not inside or not line:
            continue
        lines += 1
        for k, shape in enumerate(SHAPES):
            if shape.fullmatch(line):
                kinds[k] = kinds.get(k, 0) + 1
                break
        else:
            other += 1
            if other <= 20:
                print(f'{name}: {line}')
print(f'{lines} lines, {other} of no known shape')
print(f'{kinds.get(0, 0)} operations stored, {kinds.get(2, 0)} pointers set')
