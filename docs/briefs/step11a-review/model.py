#!/usr/bin/env python3
"""A reviewer's model of step 11a's lexing rule for a double-quoted string
(docs/PLAN.md, "11a. Interpolation"), with Q1(a), Q2(a) and Q3(a) taken as
recommended.  It is written from the proposal's sentences and from nothing
else: where the text leaves a choice, a flag in `Opts` picks the reading.

lex(body, scalars, arrays, opts) gives ('refused', why) or ('ok', pieces),
where a piece is ('text', s), ('scalar', name), ('array', name),
('elem', name, index), ('slice', name, [item, ...]), ('last', name);
an index is ('n', int) or ('v', name); a slice's item is an index or
('range', index, index).

value(pieces, env) gives the string the proposal says is printed, or
('fault', why).
"""

import re

NAME = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')


class Opts:
    # "The number is decimal digits with a minus or without": read as written,
    # 010 is ten.  With refuse_leading_zero the model refuses 010 and 00 (F1).
    refuse_leading_zero = False
    # "blanks are allowed where perl allows them": between the minus and its
    # digits too?
    blank_after_minus = True
    # Does what Q2(a) refuses after `$#a` hold after `$#{a}`?  The text says
    # "after `${x}` and `@{a}` nothing" and does not name `$#{a}`.
    check_after_braced_last = False
    # A slice "has a comma or a range": is `@a[1,]` (one index, one comma) in?
    trailing_comma = False
    # the largest index's digits the model will read as a number
    max_digits = 18


class Refused(Exception):
    pass


def lex(body, scalars, arrays, opts=Opts):
    try:
        return ('ok', _lex(body, set(scalars), set(arrays), opts))
    except Refused as e:
        return ('refused', str(e))


def _escape(body, i):
    """body[i] is a backslash: the character it gives, and the next position.
    Only the escapes the fuzzer writes; any other is outside the model."""
    if i + 1 >= len(body):
        raise Refused('backslash at the end')
    c = body[i + 1]
    if c == 'n':
        return '\n', i + 2
    if c == 't':
        return '\t', i + 2
    if c.isalnum():
        raise Refused('an escape the model does not carry: \\' + c)
    if ord(c) > 126 or ord(c) < 32:
        raise Refused('backslash before a character the model does not carry')
    return c, i + 2          # a backslash before a punctuation mark or a space


def _after(body, i, what):
    """Q2(a): after a name, an element, a slice or $#a, the language refuses
    `::`, `{`, `[`, `->` before `[`, `{`, `@` or `$`, and a character past
    ASCII.  Everything else is text."""
    rest = body[i:]
    if rest.startswith('::'):
        raise Refused(f':: after {what}')
    if rest.startswith('{'):
        raise Refused(f'{{ after {what}')
    if rest.startswith('['):
        raise Refused(f'[ after {what}')
    if rest.startswith('->') and rest[2:3] in ('[', '{', '@', '$') and rest[2:3]:
        raise Refused(f'-> before {rest[2]} after {what}')
    if rest and ord(rest[0]) > 127:
        raise Refused(f'a character past ASCII after {what}')


def _blanks(body, i):
    while i < len(body) and body[i] in ' \t':
        i += 1
    return i


def _index(body, i, scalars, opts):
    """One index: a whole number, decimal digits with a minus or without, or a
    scalar variable.  Returns (index, next)."""
    if body[i:i + 1] == '$':
        m = NAME.match(body, i + 1)
        if not m:
            raise Refused('an index that is no number and no scalar')
        if m.group() not in scalars:
            raise Refused(f'${m.group()} is not declared')
        return ('v', m.group()), m.end()
    j = i
    neg = False
    if body[j:j + 1] == '-':
        neg = True
        j += 1
        if opts.blank_after_minus:
            j = _blanks(body, j)
    k = j
    while k < len(body) and body[k] in '0123456789':
        k += 1
    if k == j:
        raise Refused('an index that is no number and no scalar')
    digits = body[j:k]
    if opts.refuse_leading_zero and len(digits) > 1 and digits[0] == '0':
        raise Refused('a leading zero in an index')
    if len(digits) > opts.max_digits:
        raise Refused('an index too large')
    n = int(digits)
    return ('n', -n if neg else n), k


def _lex(body, scalars, arrays, opts):
    pieces = []
    text = []
    i = 0

    def flush():
        if text:
            pieces.append(('text', ''.join(text)))
            text.clear()

    while i < len(body):
        c = body[i]
        if c == '\\':
            ch, i = _escape(body, i)
            text.append(ch)
            continue
        if c == '"':
            raise Refused('the string ends here')
        if c == '$':
            flush()
            if body[i + 1:i + 2] == '#':
                if body[i + 2:i + 3] == '{':
                    m = NAME.match(body, i + 3)
                    if not m or body[m.end():m.end() + 1] != '}':
                        raise Refused('$#{ with no name hard against both braces')
                    if m.group() not in arrays:
                        raise Refused(f'@{m.group()} is not declared')
                    pieces.append(('last', m.group()))
                    i = m.end() + 1
                    if opts.check_after_braced_last:
                        _after(body, i, '$#{a}')
                    continue
                m = NAME.match(body, i + 2)
                if not m:
                    raise Refused('$# begins no shape')
                if m.group() not in arrays:
                    raise Refused(f'@{m.group()} is not declared')
                pieces.append(('last', m.group()))
                i = m.end()
                _after(body, i, '$#a')
                continue
            if body[i + 1:i + 2] == '{':
                m = NAME.match(body, i + 2)
                if not m or body[m.end():m.end() + 1] != '}':
                    raise Refused('${ with no name hard against both braces')
                if m.group() not in scalars:
                    raise Refused(f'${m.group()} is not declared')
                pieces.append(('scalar', m.group()))
                i = m.end() + 1
                continue
            m = NAME.match(body, i + 1)
            if not m:
                raise Refused('a $ that begins no shape')
            name = m.group()
            i = m.end()
            if body[i:i + 1] == '[':
                if name not in arrays:
                    raise Refused(f'$%s[ and no @%s' % (name, name))
                j = _blanks(body, i + 1)
                idx, j = _index(body, j, scalars, opts)
                j = _blanks(body, j)
                if body[j:j + 1] != ']':
                    raise Refused('an index that is more than a number or a scalar')
                pieces.append(('elem', name, idx))
                i = j + 1
                _after(body, i, 'an element')
                continue
            if name not in scalars:
                raise Refused(f'${name} is not declared')
            pieces.append(('scalar', name))
            _after(body, i, 'a name')
            continue
        if c == '@':
            flush()
            if body[i + 1:i + 2] == '{':
                m = NAME.match(body, i + 2)
                if not m or body[m.end():m.end() + 1] != '}':
                    raise Refused('@{ with no name hard against both braces')
                if m.group() not in arrays:
                    raise Refused(f'@{m.group()} is not declared')
                pieces.append(('array', m.group()))
                i = m.end() + 1
                continue
            m = NAME.match(body, i + 1)
            if not m:
                raise Refused('an @ that begins no shape')
            name = m.group()
            i = m.end()
            if name not in arrays:
                raise Refused(f'@{name} is not declared')
            if body[i:i + 1] == '[':
                items = []
                j = i + 1
                commas = 0
                ranged = False
                while True:
                    j = _blanks(body, j)
                    if opts.trailing_comma and items and body[j:j + 1] == ']':
                        break
                    a, j = _index(body, j, scalars, opts)
                    j = _blanks(body, j)
                    if body[j:j + 2] == '..':
                        j = _blanks(body, j + 2)
                        b, j = _index(body, j, scalars, opts)
                        j = _blanks(body, j)
                        items.append(('range', a, b))
                        ranged = True
                    else:
                        items.append(a)
                    if body[j:j + 1] == ',':
                        commas += 1
                        j += 1
                        continue
                    if body[j:j + 1] == ']':
                        break
                    raise Refused('a slice that is more than numbers, scalars and ranges')
                if not ranged and commas == 0:
                    raise Refused('a slice by one index')
                pieces.append(('slice', name, items))
                i = j + 1
                _after(body, i, 'a slice')
                continue
            pieces.append(('array', name))
            _after(body, i, 'a name')
            continue
        if ord(c) < 32 and c not in '\n\t':
            raise Refused('a control character')
        text.append(c)
        i += 1
    flush()
    return pieces


class Fault(Exception):
    pass


def _str(v):
    if v is None:
        raise Fault('undef where a string is wanted')
    return str(v)


def _int(ix, env):
    if ix[0] == 'n':
        return ix[1]
    v = env['$' + ix[1]]
    if isinstance(v, int):
        return v
    raise Fault('an index that is no whole number')   # the fuzzer's other scalars are words


def _get(arr, n):
    if n < 0:
        n += len(arr)
    if 0 <= n < len(arr):
        return arr[n]
    return None


def value(pieces, env):
    out = []
    try:
        for p in pieces:
            if p[0] == 'text':
                out.append(p[1])
            elif p[0] == 'scalar':
                out.append(_str(env['$' + p[1]]))
            elif p[0] == 'array':
                out.append(' '.join(_str(v) for v in env['@' + p[1]]))
            elif p[0] == 'last':
                out.append(str(len(env['@' + p[1]]) - 1))
            elif p[0] == 'elem':
                out.append(_str(_get(env['@' + p[1]], _int(p[2], env))))
            elif p[0] == 'slice':
                arr = env['@' + p[1]]
                vals = []
                for it in p[2]:
                    if it[0] == 'range':
                        lo, hi = _int(it[1], env), _int(it[2], env)
                        vals += [_get(arr, n) for n in range(lo, hi + 1)]
                    else:
                        vals.append(_get(arr, _int(it, env)))
                out.append(' '.join(_str(v) for v in vals))
    except Fault as e:
        return ('fault', str(e))
    return ''.join(out)
