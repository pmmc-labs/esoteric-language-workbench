#!/usr/bin/env python3
"""The mechanical checks: what the working rules say, enforced rather
than remembered. `make checks` runs them all; `make oracle` and `make
models` write what perl and the models say.

  oracle    perl 5.42 ($CURLY_PERL) is the source of every expected
            output that perl can give (D10), and this holds each golden
            test to it, by the test's kind:
              same     perl compiles the file without a word and runs it
                       with nothing on stderr; under eight hash seeds, each
                       of the full 256 bits, its stdout and exit status
                       are the same, and are the .expected.
              dies     the same, but perl's status is 255, and the
                       .expected is its stdout, then its stderr, then
                       `exit: 255`; and perl, run once more with every
                       warning that is not the program's own `warn`
                       marked (t/oracle/Warned.pm), marks none (D149).
              warns    as dies, for a program that writes to stderr and
                       ends otherwise: the .expected is perl's stdout,
                       its stderr, and its exit status if it isn't 0.
              fault    perl compiles the file, in silence; the compiled program's
                       stdout is the start of perl's, under each seed,
                       and what it wrote to stderr before the fault the
                       start of perl's stderr;
                       perl ends within the time allowed; the .expected
                       is that stdout, a `fault:` line, and `exit: 1`.
              refused  perl isn't asked. The .expected is one line,
                       FILE:LINE:COL: message, at a line the file has,
                       and `exit: 1`.
              new      perl isn't asked: its decision names its source.
            And a test compared with perl may not print a hash's order:
            `keys`, `values`, `each` or a whole hash must be sorted (the
            reading rule, below). A test's headers are checked too: one
            of each, a limit of 1 to 60 seconds, and no variable of
            perl's own in `# env:`.
            `--write` writes each same and dies test's .expected from
            perl instead of comparing (make oracle); it writes nothing
            for a test perl warns on, or whose output moves with the seed.
            The check has tests of its own, t/checks/ (README.md there):
            each is a Perl file, a .expected, and a line saying whether
            the check must pass it or how it must fail it. They run every
            time, so a check that stops failing what it should is caught.
  models    Every command in a model's docstring (a line that starts
            `python3 t/models/`, with `> file`) is run, and its output
            must equal the file. A file that was patched by hand, or a
            model that was changed without rerunning it, fails here.
            `--write` writes the files instead (make models).
  tests     Every t/*.pl, examples/*.pl and docs/guide/code/*.pl has a
            .expected and the other way round; a test that names a model
            (`t/models/x.py` in its comments) names one that exists and
            that lists the test's files.
  commits   Every commit in a range (BASE..HEAD, default origin/main..HEAD)
            that touches compiler/, runtime/, lib/ or bin/ names a
            decision (D12) or a plan step (step 3) in its subject, so
            that the change can be found from the log and the log from
            the change. `commit-msg FILE [--staged]` checks one message,
            for the git hook that `make hooks` installs.
  differences  docs/DIFFERENCES.md, which says where the language and perl
            differ (D103): each of its programs does under perl and under
            the compiler what its row says; each rated row has ratings
            from the lists and decisions that exist, in the section they
            belong to; and every decision of the log is cited in it or
            listed as saying nothing there.
  doctor    Each tool's version, and a failure for one the project can't
            use: perl that isn't 5.42 with 64-bit integers and doubles,
            Node before 22.18, no cc, no clang (make doctor).
"""

import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
IMPL = ('compiler/', 'runtime/', 'lib/', 'bin/')
TEST_DIRS = ['t', 'examples', 'docs/guide/code']
EXT = '.pl'
KINDS = ('same', 'dies', 'warns', 'fault', 'refused', 'new')
# Found once, so that the perl that is vetted is the perl that is run,
# whatever a test's `# env:` does.
PERL = shutil.which(os.environ.get('CURLY_PERL', 'perl')) or os.environ.get('CURLY_PERL', 'perl')
# Eight seeds of the full 256 bits. PERL_HASH_SEED=1 to 8 look like eight
# and are nearly one: a short seed sets the first byte and leaves the rest
# zero, and the part of perl's hash function that short keys go through
# reads later bytes, so every key lands in the same bucket under all of
# them (a review measured a sort with one tie, over six to ten keys,
# getting past eight such seeds about one time in ten).
SEEDS = [hashlib.sha256(str(n).encode()).hexdigest() for n in range(1, 9)]
# Seconds perl may take over one run of one test. A fault test has to be
# a program that ends under perl (D10), and the natural test of some
# faults doesn't: `for my $x (@a) { push @a, $x }`.
PERL_LIMIT = 10


# ---- models

def model_commands():
    """(model, args, path) for every regenerating command in every model."""
    out = []
    for model in sorted(glob.glob('t/models/*.py')):
        src = open(model).read()
        for line in src.splitlines():
            m = re.match(r'\s*python3 (t/models/\S+\.py)((?: \S+)*) > (\S+)$', line)
            if m:
                if m.group(1) != model:
                    out.append((model, None, f'{model} lists a command for {m.group(1)}'))
                else:
                    out.append((model, m.group(2).split(), m.group(3)))
    return out

# The models that are a part of another, and write no file of their own.
PARTS = {'t/models/merge.py'}

def check_models(write=False):
    bad = []
    commands = model_commands()
    for model, args, path in commands:
        if args is None:
            bad.append(path)
            continue
        r = subprocess.run(['python3', '-I', model, *args], capture_output=True)
        if r.returncode != 0:
            bad.append(f'{model} {" ".join(args)}: exit {r.returncode}\n{r.stderr.decode()}')
            continue
        if write:
            open(path, 'wb').write(r.stdout)
        elif not os.path.exists(path):
            bad.append(f'{path}: not written; `make models`')
        elif open(path, 'rb').read() != r.stdout:
            bad.append(f'{path}: differs from what {model} writes; rerun it (`make models`), don\'t patch the file')
    # (t/models/merge.py is perl's merge sort, which t/models/sort.py
    # imports: it writes no test, and holds itself to perl when it is run.)
    models_without = [m for m in sorted(glob.glob('t/models/*.py')) if m not in PARTS and not any(c[0] == m for c in commands)]
    bad += [f'{m}: lists no command that writes a file' for m in models_without]
    print(f'models: {len(commands)} files from {len(set(c[0] for c in commands))} models' + (' written' if write else ''))
    return bad


# ---- tests

def golden_tests():
    return [src for d in TEST_DIRS for src in sorted(glob.glob(f'{d}/*{EXT}'))]

def check_tests():
    bad = []
    listed = {path for _, _, path in model_commands() if path}
    for src in golden_tests():
        if not os.path.exists(src[:-len(EXT)] + '.expected'):
            bad.append(f'{src}: no .expected')
        text = open(src, encoding='utf-8', errors='replace').read()
        for model in set(re.findall(r't/models/\S+\.py', text)):
            if not os.path.exists(model):
                bad.append(f'{src}: names {model}, which doesn\'t exist')
            elif src not in listed:
                bad.append(f'{src}: names {model}, which doesn\'t list it')
    for d in TEST_DIRS:
        for exp in sorted(glob.glob(f'{d}/*.expected')):
            if not os.path.exists(exp[:-len('.expected')] + EXT):
                bad.append(f'{exp}: no {EXT} file')
        # In t/checks/ a .stdout stands for what a binary printed. Beside
        # a real test it would be taken for nothing, and looks like more.
        bad += [f'{s}: a .stdout belongs to the check\'s own tests, in t/checks/' for s in sorted(glob.glob(f'{d}/*.stdout'))]
    return bad


# ---- the oracle

def headers(path):
    """A test's headers: `# name: value` among the comments before its
    first statement, as t/run.sh reads them."""
    return headers_and_problems(path)[0]

def headers_and_problems(path):
    """The headers, and what is wrong with them. Lines end at a newline
    and nowhere else, as they do for awk and for perl: Python would end
    one at a carriage return too, and read a header t/run.sh doesn't."""
    found, problems = {}, []
    for line in open(path, encoding='utf-8', errors='replace', newline='').read().split('\n'):
        if not line.strip(' \t'):
            continue
        if not line.lstrip(' \t').startswith('#'):
            break
        m = re.match(r'# (\w+): (.*)$', line)
        if not m:
            continue
        name, value = m.group(1), m.group(2)
        if name in found:
            problems.append(f'more than one `# {name}:` header')
        found[name] = value
        if name == 'limit' and not re.fullmatch(r'[1-9]|[1-5][0-9]|60', value):
            problems.append(f'`# limit: {value}`: a whole number of seconds, 1 to 60')
        if name == 'env':
            for pair in words(value):
                # A test's environment is the program's. perl's own knobs
                # in it would be a test turning the oracle's seeds off.
                if '=' not in pair or re.match(r'PERL|PATH=|LD_|DYLD_', pair):
                    problems.append(f'`# env: {pair}`: NAME=value, and a test may not set perl\'s own variables, PATH or the loader\'s')
    return found, problems

def words(text):
    """A header's value split as the shell splits it in t/run.sh: at
    spaces, tabs and newlines, and at nothing else Python calls a space."""
    return [w for w in re.split(r'[ \t\n]+', text) if w]

def printf_b(text):
    """What the shell's printf %b makes of `text`, a `# stdin:` header's
    bytes: the shell's, as in t/run.sh, since printf the program reads
    some escapes differently."""
    return subprocess.run(['sh', '-c', 'printf %b "$1"', 'sh', text], capture_output=True, check=True).stdout if text else b''

def perl_problem():
    """Why $CURLY_PERL can't be the oracle, or None. The checks fail
    without the pinned perl; they don't skip (D10)."""
    try:
        r = subprocess.run([PERL, '-MConfig', '-e', 'print "$^V ivsize $Config{ivsize} nvsize $Config{nvsize}"'],
                           capture_output=True, text=True)
    except OSError as e:
        return f'CURLY_PERL ({PERL}) does not run: {e}'
    if not re.fullmatch(r'v5\.42\.\d+ ivsize 8 nvsize 8', r.stdout):
        return (f'CURLY_PERL ({PERL}) is {r.stdout or r.stderr.strip()!r}: the oracle is perl 5.42 '
                f'with 64-bit integers and doubles (CLAUDE.md, Toolchain)')
    return None

def knobs():
    """What every test assumes of the runtime, from t/knobs.sh, where
    t/run.sh has it from too: a variable already set stands."""
    found = dict(re.findall(r'^: "\$\{(\w+)=(\w*)\}"$', open('t/knobs.sh').read(), re.M))
    assert found, 't/knobs.sh has no knob in the shape this reads'
    return {name: os.environ.get(name, value) for name, value in found.items()}

# What a program may print before it is stopped. A loop that prints without
# end would otherwise fill this process's memory in the seconds it is
# allowed: perl carries on where the language faults, so a test whose loop
# only the fault would end is such a loop (step 6).
OUTPUT_LIMIT = 16 * 1024 * 1024

class Runaway(Exception):
    pass

def run_capped(argv, env, stdin, limit):
    """A program run to its end, with what it printed. None if it didn't
    end in `limit` seconds. What it prints goes to two files, each with
    the system's limit on its size: past it the program is stopped
    (SIGXFSZ), and that is a Runaway."""
    import resource, signal, tempfile
    def cap():
        resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT_LIMIT, OUTPUT_LIMIT))
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        try:
            r = subprocess.run(argv, env=env, input=stdin, stdout=out, stderr=err, timeout=limit, preexec_fn=cap)
        except subprocess.TimeoutExpired:
            return None
        if r.returncode == -signal.SIGXFSZ:
            raise Runaway(f'{os.path.basename(argv[0])} printed more than {OUTPUT_LIMIT >> 20} MB, and was stopped: a test ends, and says little')
        out.seek(0)
        err.seek(0)
        return subprocess.CompletedProcess(argv, r.returncode, out.read(), err.read())

def run_perl(flags, path, hdr, seed, limit):
    """perl on a test, from the repository's root and by the path the
    compiler is given, with the test's stdin, arguments and environment
    and nothing else of this process's. None if it didn't end in time."""
    env = {'PATH': os.environ.get('PATH', ''), 'PERL_HASH_SEED': str(seed)}
    env.update(pair.split('=', 1) for pair in words(hdr.get('env', '')))
    return run_capped([PERL, *flags, path, *words(hdr.get('args', ''))], env, printf_b(hdr.get('stdin', '')), limit)

def clip(data, n=300):
    text = data.decode('utf-8', 'replace')
    return text if len(text) <= n else text[:n] + '...'

# The reading rule (D10). Seeds agree by luck on a small hash, two of
# them on a two-key hash about half the time, so a test whose output is
# compared with perl's may not show a hash's order at all, and that is
# checked by reading it. Reading Perl with patterns can't be exact, so
# this errs one way: a use it can't see to be safe is rejected, and the
# test is rewritten until it can. What it takes to be safe:
#   keys, values, each or a whole hash (%h, %$r, %{...}, ->%*) as the
#   operand of `sort`, directly or through map, grep and reverse and
#   their blocks; or of `scalar`; or
#   a whole hash after my, state, keys, values, each, exists, delete or
#   a backslash, or on the left of `=`.
# `scalar` counts only when it is right against its operand, and never for
# `each`; one opening bracket may stand between a word and its operand,
# since `sort((keys %h)[0])` sorts one key and not the keys; a double-
# quoted string that runs code (`@{[ ... ]}`, `${\ ... }`) is rejected
# with a hash in it or not.
# Its holes: a sort that doesn't settle the order (a tie, `sort { 0 }`),
# which only the seeds catch; quotes it can't pair (a heredoc, `q()`, an
# apostrophe in a pattern), which can hide the rest of a file; a hash
# written with a space in it (`% h`). And it knows nothing of what else
# can show an order: a dumper, `each` behind a sub. Behind it stands the
# compiler, which a test must also pass and which refuses most of that,
# and the eight seeds. TRAPS.md, "The checks themselves", has the list,
# by the step that brings each construct.
ORDERED = re.compile(r'\b(?:keys|values|each)\b|->%\*|%(?=[A-Za-z_${])')
THROUGH = ('map', 'grep', 'reverse')
OWNERS = ('my', 'state', 'keys', 'values', 'each', 'exists', 'delete')

def strip_strings_and_comments(text):
    """The program with its quoted strings emptied and its comments gone,
    so that a `%s` in a format or a `keys` in a sentence isn't read as
    code. Heredocs, `q()` and patterns are left as they are, which mostly
    adds rejections; a `#` inside one is taken for a comment, and hides
    the rest of its line."""
    out = []
    i = 0
    while i < len(text):
        c = text[i]
        if c in '"\'':
            j = i + 1
            while j < len(text) and text[j] != c:
                j += 2 if text[j] == '\\' else 1
            # A string that runs code keeps a mark that the reader rejects.
            runs_code = c == '"' and re.search(r'@\{\s*\[|\$\{\s*\\\\', text[i:j])
            out.append(c + ('\0' if runs_code else '') + c)
            i = j + 1
        elif c == '#' and (i == 0 or text[i - 1] not in '$'):
            while i < len(text) and text[i] != '\n':
                i += 1
        else:
            out.append(c)
            i += 1
    return ''.join(out)

def word_before(code, i):
    """The word that ends just before position i, skipping blanks and
    one opening bracket, and where it starts. A block `{ ... }` there is
    stepped over, to the word that owns it. A name with a sigil or an
    arrow before it (`$sort`, `->sort`) is no word."""
    brackets = 0
    while i > 0 and (code[i - 1] in ' \t\n' or (code[i - 1] == '(' and brackets == 0)):
        brackets += code[i - 1] == '('
        i -= 1
    if i > 0 and code[i - 1] == '}':
        depth = 0
        while i > 0:
            i -= 1
            depth += {'}': 1, '{': -1}.get(code[i], 0)
            if depth == 0:
                break
        while i > 0 and code[i - 1] in ' \t\n':
            i -= 1
    j = i
    while j > 0 and (code[j - 1].isalnum() or code[j - 1] == '_'):
        j -= 1
    if j > 0 and code[j - 1] in '$@%&>:':
        return '', j
    return code[j:i], j

# What a block between a `sort` and its `keys` may not do, and a `sort`'s
# own block: anything but work a value out. A block that prints, stores or
# counts shows the order its values came in (step 12's review, C1).
EFFECT = re.compile(r'\b(?:say|print|printf|push|unshift|pop|shift|splice|delete|die|warn)\b|\+\+|--|(?<![=!<>])=(?![=~>])')
COMPARES = re.compile(r'\$[ab]\b.*(?:<=>|\bcmp\b).*\$[ab]\b', re.S)

def block_before(code, i):
    """The text of the block that ends just before position i, behind
    blanks and one opening bracket as `word_before` reads them; None if
    there is none."""
    brackets = 0
    while i > 0 and (code[i - 1] in ' \t\n' or (code[i - 1] == '(' and brackets == 0)):
        brackets += code[i - 1] == '('
        i -= 1
    if i == 0 or code[i - 1] != '}':
        return None
    end, depth = i, 0
    while i > 0:
        i -= 1
        depth += {'}': 1, '{': -1}.get(code[i], 0)
        if depth == 0:
            break
    return code[i + 1:end - 1]

def counted(code, m):
    """Whether the hash, or the `keys` or `values`, at match m stands where
    only how many there are is asked, or where it is copied or declared:
    no order shows (step 12's review, C2)."""
    before, rest = code[:m.start()], code[m.start():]
    name = r'%[\w]+' if m.group(0)[0] == '%' else r'(?:keys|values)\s*\(?\s*%\w+\s*\)?'
    # The whole test of an if, an unless, a while or an until.
    if re.search(r'\b(?:if|unless|while|until)\s*\(\s*!?\s*$', before) and re.match(name + r'\s*\)', rest):
        return True
    # Assigned to a scalar, as its count; or to another hash, as a copy.
    target = r'\$\w+' if m.group(0)[0] != '%' else r'[$%]\w+'
    if re.search(r'(?:^|[;{}\s])(?:my\s+)?' + target + r'\s*=\s*$', before) and re.match(name + r'\s*;', rest):
        return True
    # Compared with a number.
    if re.match(name + r'\s*(?:==|!=|<=|>=|<(?!=>)|>)\s*\d+\s*[;)]', rest) and not re.search(r'\bsort\b[^;]*$', before):
        return True
    # In the list a hash is assigned: copied, into a hash of its own order.
    if re.search(r'%\w+\s*=\s*\([^;]*$', before):
        return True
    # An operand of arithmetic, of a dot or of a comparison: its count.
    operator = r'(?:[-+*/]|(?<!\.)\.(?!\.)|==|!=|<=|>=)'
    if re.search(operator + r'\s*\(*\s*$', before) or re.match(name + r'\s*\)*\s*' + operator, rest):
        return True
    # Copied whole into an array of its own, `my @v = values %h;`, that is
    # only ever sorted or counted: every other place the array stands has
    # `sort` or `scalar` for the word before it, and no element of it is
    # read. (Until step 12b a hash may not stand in a sort's own list.)
    into = re.search(r'\bmy\s+@(\w+)\s*=\s*\(?\s*$', before)
    if into and re.match(name + r'\s*\)?\s*;', rest):
        array = into.group(1)
        uses = [u for u in re.finditer(r'@' + array + r'\b', code) if u.start() != into.start(1) - 1]
        if uses and not re.search(r'\$' + array + r'\s*\[|\$#' + array + r'\b', code) \
                and all(word_before(code, u.start())[0] in ('sort', 'scalar') for u in uses):
            return True
    # The whole list of a loop, or of a `map`, whose block never reads the
    # value it is handed (step 12b: the tests of what a loop over a hash
    # freezes). A `"` in the block may hold the variable, so it is no such
    # block; a `grep` and a `sort` hand their list on, and are not here.
    def unread(body, variable):
        return body is not None and '"' not in body and not re.search(re.escape(variable) + r'(?![A-Za-z0-9_\[{])', body)
    def block_after(text):
        depth = 0
        for k, ch in enumerate(text):
            depth += {'{': 1, '}': -1}.get(ch, 0)
            if depth == 0:
                return text[1:k]
        return None
    loop = re.search(r'\bfor(?:each)?\s+(?:my\s+(\$\w+)\s*)?\(\s*$', before)
    after = re.match(name + r'\s*\)\s*(?=\{)', rest)
    if loop and after and unread(block_after(rest[after.end():]), loop.group(1) or '$_'):
        return True
    if word_before(code, m.start())[0] == 'map' and re.match(name + r'\s*[;)]', rest) and unread(block_before(code, m.start()), '$_'):
        return True
    modifier = re.search(r'(?:^|[;{}]\s*\n?)([^;\n]*)\bfor\s+\(?\s*$', before)
    if modifier and re.match(name + r'\s*\)?\s*;', rest) and unread(modifier.group(1), '$_'):
        return True
    # Handed to a sub of the file's whose last parameter is a hash: copied
    # into it, whatever the order.
    call = re.search(r'\b(\w+)\([^()]*$', before)
    if m.group(0)[0] == '%' and call and re.search(r'\bsub\s+' + call.group(1) + r'\s*\([^{;]*%\w*\s*\)\s*\{', code):
        return True
    # Tested, by `? :` or behind a `!`: whether it has any.
    if re.match(name + r'\s*\?', rest) or re.search(r'!\s*$', before):
        return True
    # The last target of a `my (...)`: declared, and filled.
    if m.group(0)[0] == '%' and re.search(r'\bmy\s*\([^()]*$', before) and re.match(name + r'\s*\)\s*=', rest):
        return True
    # What a sub gives back: the order shows where the call stands, if it
    # does, and the seeds are left to see it.
    if re.search(r'\breturn\s+$', before):
        return True
    # A parameter of a sub.
    if m.group(0)[0] == '%' and re.search(r'\bsub\s+\w+\s*\([^{;]*$', before):
        return True
    return False

def hash_order_shown(path):
    """Where a test shows a hash's order, by the reading rule: a list of
    `line N: what`."""
    code = strip_strings_and_comments(open(path, encoding='utf-8', errors='replace').read())
    found = [f'line {code.count(chr(10), 0, m.start()) + 1}: a string with code in it, which the check can\'t read, without sort'
             for m in re.finditer('"\0"', code)]
    for m in ORDERED.finditer(code):
        what = m.group(0)
        whole = what[0] in '%-'
        line = code.count('\n', 0, m.start()) + 1
        if what[0] == '%' and m.start() > 0 and code[m.start() - 1] == '\\':
            # `\%h` is a reference: the order shows where it is used.
            continue
        # A word that is a key, alone in braces or before `=>`, is a string.
        if what[0] not in '%-' and (re.match(r'\s*=>', code[m.end():]) or (re.match(r'[ \t]*\}', code[m.end():]) and re.search(r'\{[ \t]*$', code[:m.start()]))):
            continue
        if counted(code, m):
            continue
        # A variable called `$keys` or `@values` is a name.
        if what[0] != '%' and m.start() > 0 and code[m.start() - 1] in '$@':
            continue
        word, at = word_before(code, m.start())
        if word == 'scalar' and what != 'each':
            continue
        # `(keys %h)[0]`: one of them, picked before any sort.
        if re.match(r'(?:keys|values)?\s*\(?\s*%?\w*\s*\)?\s*\)\s*\[', code[m.start():]) and re.search(r'\(\s*$', code[:m.start()]):
            found.append(f'line {line}: {what} sliced before any sort, without sort')
            continue
        block = block_before(code, m.start())
        while word in THROUGH:
            if block is not None and EFFECT.search(block):
                found.append(f'line {line}: a {word} block that does more than work a value out, between {what} and any sort: without sort')
                word = ''
                break
            block = block_before(code, at)
            word, at = word_before(code, at)
        if word == 'sort':
            if block is not None and (EFFECT.search(block) or not COMPARES.search(block)):
                found.append(f'line {line}: a sort whose block does not only compare $a with $b shows the order it was given: without sort')
            continue
        if word == '' and found and found[-1].startswith(f'line {line}: a ') and 'block that does more' in found[-1]:
            continue
        if whole and word in OWNERS:
            continue
        if what[0] == '%' and re.match(r'%[\w$]+\s*=(?![=~>])', code[m.start():]):
            continue
        found.append(f'line {line}: {"a whole hash" if whole else what} without sort')
    return found

def perl_compiles(path, hdr, limit, silent):
    """Why `perl -c` isn't satisfied, or None. `silent`: not a word on
    stderr but perl's own `syntax OK` (a warning while compiling is a
    refusal, D15)."""
    r = run_perl(['-c'], path, hdr, 1, limit)
    if r is None:
        return f'perl -c did not finish in {limit} seconds'
    if r.returncode != 0:
        return f'perl does not compile it: {clip(r.stderr)}'
    if silent and r.stderr != f'{path} syntax OK\n'.encode():
        return f'perl does not compile it in silence: {clip(r.stderr)}'
    return None

def perl_says(path, hdr, kind, limit):
    """(problem, expected): what a same or dies test's .expected must be,
    by running perl, or why perl won't say."""
    outputs = []
    for seed in SEEDS:
        r = run_perl([], path, hdr, seed, limit)
        if r is None:
            return f'perl did not finish in {limit} seconds', None
        if r.returncode < 0:
            return f'perl was killed by signal {-r.returncode}', None
        if kind == 'same':
            if r.stderr:
                return f'perl wrote to stderr, so the language should fault or refuse (D15): {clip(r.stderr)}', None
            outputs.append(r.stdout + (f'exit: {r.returncode}\n'.encode() if r.returncode else b''))
        elif kind == 'warns':
            if r.returncode == 255:
                return 'perl\'s exit status is 255: an uncaught die, which is a dies test (D149)', None
            outputs.append(r.stdout + r.stderr + (f'exit: {r.returncode}\n'.encode() if r.returncode else b''))
        else:
            if r.returncode != 255:
                return f'perl\'s exit status is {r.returncode}, not 255: not an uncaught die (D12)', None
            outputs.append(r.stdout + r.stderr + b'exit: 255\n')
    # stderr is the program's own `warn`s and `die`, and no warning of
    # perl's (D15, D149): perl once more, with every other warning marked.
    marked = None if kind == 'same' else run_perl(['-I' + os.path.join(ROOT, 't', 'oracle'), '-MWarned'], path, hdr, SEEDS[0], limit)
    if marked is not None and b'PERL WARNED: ' in marked.stderr:
        return f'perl warned as it ran, so the language should fault or refuse (D15): {clip(marked.stderr)}', None
    if len(set(outputs)) > 1:
        return 'perl\'s output changes from run to run: with the hash seed, or with something else D14 lists', None
    return None, outputs[0]

def program_stdout(path, hdr, errors=False):
    """(problem, stdout) of the compiled program, and with `errors` what
    it wrote to stderr before a fault's line too. For the check's own
    tests, and only those, a file PATH.stdout stands in for it: they are
    Perl the language can't compile yet, with what a binary would have
    printed, and PATH.stderr for what it wrote to stderr first."""
    stood = path[:-len(EXT)] + '.stdout'
    if path.startswith('t/checks/') and os.path.exists(stood):
        err = path[:-len(EXT)] + '.stderr'
        warned = open(err, 'rb').read() if os.path.exists(err) else b''
        return (None, open(stood, 'rb').read(), warned) if errors else (None, open(stood, 'rb').read())
    os.makedirs('build/oracle', exist_ok=True)
    binary = 'build/oracle/' + os.path.basename(path)[:-len(EXT)]
    c = subprocess.run(['node', 'bin/curlyc.ts', '-o', binary, path], capture_output=True)
    if c.returncode != 0:
        return f'it does not compile: {clip(c.stderr)}', None
    env = dict(os.environ)
    env.update(knobs())
    env.update(pair.split('=', 1) for pair in words(hdr.get('env', '')))
    r = run_capped([binary, *words(hdr.get('args', ''))], env, printf_b(hdr.get('stdin', '')), int(os.environ.get('TIMEOUT', '60')))
    if r is None:
        return ('the compiled program did not finish', None, None) if errors else ('the compiled program did not finish', None)
    cut = r.stderr.rfind(b'fault: ')
    return (None, r.stdout, r.stderr[:cut] if cut >= 0 else r.stderr) if errors else (None, r.stdout)

def oracle_one(path, write=False):
    """What is wrong with one test, as a list; empty if nothing is."""
    hdr, problems = headers_and_problems(path)
    if problems:
        return problems
    try:
        return oracle_kind(path, hdr, write)
    except Runaway as e:
        return [str(e)]
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        # A header the shell or the system won't take: say so, and go on
        # to the next test.
        return [f'the check could not run it: {e}']

def oracle_kind(path, hdr, write):
    kind = hdr.get('kind', 'same')
    limit = int(hdr.get('limit', PERL_LIMIT))
    exp_path = path[:-len(EXT)] + '.expected'
    expected = open(exp_path, 'rb').read() if os.path.exists(exp_path) else None
    if kind not in KINDS:
        return [f'unknown kind: {kind}']
    if kind == 'new':
        return []
    if kind == 'refused':
        shape = re.escape(path).encode() + rb':([1-9]\d*):[1-9]\d*: [!-~][ -~]*\nexit: 1\n'
        m = re.fullmatch(shape, expected or b'')
        lines = open(path, 'rb').read().count(b'\n') + 1
        if not m or int(m.group(1)) > lines:
            return [f'the .expected is not `{path}:LINE:COL: message`, at a line the file has, and `exit: 1`']
        return []

    shown = hash_order_shown(path)
    if shown:
        return [f'{s}: perl\'s order is its own, and a test can\'t show it (D10, D14)' for s in shown]

    if kind in ('same', 'dies', 'warns'):
        problem = perl_compiles(path, hdr, limit, silent=True)
        if problem is None:
            problem, says = perl_says(path, hdr, kind, limit)
        if problem:
            return [problem]
        if write:
            if says != expected:
                open(exp_path, 'wb').write(says)
                print(f'wrote {exp_path}')
            return []
        if says != expected:
            return [f'the .expected differs from perl, which gives: {clip(says)!r}']
        return []

    # fault. perl compiles it in silence too: D10 asks only that perl
    # compile it, but a warning as perl compiles is a refusal (D15), and
    # a refused program is no fault test.
    problem = perl_compiles(path, hdr, limit, silent=True)
    if problem:
        return [problem]
    problem, printed, warned = program_stdout(path, hdr, errors=True)
    if problem:
        return [problem]
    shape = re.escape(printed + warned) + rb'fault: [^\n]+ at ' + re.escape(path).encode() + rb' line \d+\.\nexit: 1\n'
    if expected is None or not re.fullmatch(shape, expected):
        return [f'the .expected is not what the program printed, then wrote to stderr, `fault: MESSAGE at {path} line N.` and `exit: 1`']
    for seed in SEEDS:
        r = run_perl([], path, hdr, seed, limit)
        if r is None:
            return [f'perl did not finish in {limit} seconds: a fault test is a program that ends under perl (D10)']
        if not r.stdout.startswith(printed):
            return [f'the program printed something perl does not (D12); perl: {clip(r.stdout)!r}, the program: {clip(printed)!r}']
        # What it said on stderr before the fault is the start of perl's
        # stderr too (D148, D149).
        if not r.stderr.startswith(warned):
            return [f'the program wrote to stderr what perl does not (D148); perl: {clip(r.stderr)!r}, the program: {clip(warned)!r}']
    return []

def check_oracle_itself():
    """The check's own tests, t/checks/: each says, in a `# check:`
    header, `ok` or `fails: TEXT`, and the check must pass it, or fail it
    for a reason that has TEXT in it. A check that passes what it must
    fail is the one thing here that can't be seen from outside."""
    bad = []
    fixtures = sorted(glob.glob(f't/checks/*{EXT}'))
    for path in fixtures:
        want = headers(path).get('check', '')
        got = oracle_one(path)
        if want == 'ok':
            bad += [f'{path}: the check must pass it, and says: {g}' for g in got]
        elif want.startswith('fails: '):
            text = want[len('fails: '):]
            if not got:
                bad.append(f'{path}: the check passed a test it must fail ({text})')
            elif not all(text in g for g in got):
                bad.append(f'{path}: the check must fail it for "{text}", and says: {"; ".join(got)}')
        else:
            bad.append(f'{path}: no `# check: ok` or `# check: fails: TEXT` header')
    # program_stdout's other half, compiling and running, which no fault
    # test uses until the language can fault (step 1).
    problem, printed = program_stdout('t/000-say.pl', {})
    if problem or printed != b'42\n':
        bad.append(f't/000-say.pl compiled and run for the check gives {problem or printed!r}, not 42')
    return bad, len(fixtures)

def check_oracle(write=False):
    problem = perl_problem()
    if problem:
        return [problem]
    bad, fixtures = ([], 0) if write else check_oracle_itself()
    tests = golden_tests()
    counts = {}
    for path in tests:
        kind = headers(path).get('kind', 'same')
        counts[kind] = counts.get(kind, 0) + 1
        bad += [f'{path}: {b}' for b in oracle_one(path, write)]
    by_kind = ', '.join(f'{n} {k}' for k, n in sorted(counts.items()))
    print(f'oracle: {len(tests)} tests ({by_kind})' + (' written from perl' if write else f'; {fixtures} tests of the check itself'))
    return bad


# ---- commits

SUBJECT_OK = re.compile(r'\bD\d+\b|\bstep \d+\b', re.I)

def touches_impl(files):
    return any(f.startswith(IMPL) for f in files)

def check_message(subject, files, what):
    if touches_impl(files) and not SUBJECT_OK.search(subject):
        return [f'{what}: changes {", ".join(sorted({f.split("/")[0] for f in files if f.startswith(IMPL)}))}/ '
                f'but its subject names no decision (D12) or plan step (step 3): "{subject}"']
    return []

def check_commits(rng):
    bad = []
    log = subprocess.run(['git', 'log', '--format=%H%x00%s', rng], capture_output=True, text=True, check=True).stdout
    for line in log.splitlines():
        sha, subject = line.split('\0')
        files = subprocess.run(['git', 'show', '--format=', '--name-only', sha], capture_output=True, text=True, check=True).stdout.split()
        bad += check_message(subject, files, sha[:10])
    print(f'commits: {len(log.splitlines())} in {rng}')
    return bad

def check_commit_msg(path, staged):
    subject = next((l for l in open(path).read().splitlines() if l and not l.startswith('#')), '')
    files = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True, check=True).stdout.split() if staged else []
    return check_message(subject, files, 'this commit')


# ---- doctor

def first_line(argv):
    try:
        r = subprocess.run(argv, capture_output=True, text=True)
    except OSError:
        return None
    return ((r.stdout + r.stderr).strip().splitlines() or [''])[0] if r.returncode == 0 else None

def doctor():
    bad = []
    node = first_line(['node', '--version'])
    m = re.match(r'v(\d+)\.(\d+)', node or '')
    print(f'node    {node}')
    if not m or (int(m.group(1)), int(m.group(2))) < (22, 18):
        bad.append('node: 22.18 or later runs the compiler\'s TypeScript as it is')
    for tool, why in (('cc', 'the C compiler the driver calls'), ('clang', 'make golden-clang and make sanitize')):
        version = first_line([tool, '--version'])
        print(f'{tool:7} {version}')
        if version is None:
            bad.append(f'{tool}: not found; it is {why}')
    print(f'python3 {sys.version.split()[0]}')
    perl = first_line([PERL, '-MConfig', '-e', 'print "$^V, ivsize $Config{ivsize}, nvsize $Config{nvsize}"'])
    print(f'perl    {perl} (CURLY_PERL={PERL})')
    problem = perl_problem()
    if problem:
        bad.append(problem)
    return bad


def check_census():
    """The census's file, held to the probes of t/census/run/, to no
    WRONG and to the last commit's (step 11b; t/census.py has the rules),
    and the census's own tests. No probe is run: `make census` does that."""
    import census
    failed, total = census.self_test()
    bad = [f'the census itself: {f}' for f in failed] + census.check()
    now = json.load(open(census.JSON, encoding='utf-8'))['counts'] if os.path.exists(census.JSON) else {}
    print(f'census: {sum(now.values())} probes (' + ', '.join(f'{n} {v}' for v, n in now.items() if n) + f'); {total} tests of the census itself')
    return bad

# ---- differences

DIFF = 'docs/DIFFERENCES.md'
FEEL = ('idiom', 'habit', 'accident')
MET = ('often', 'sometimes', 'rarely')
WHERE = ('loops', 'subs', 'printing', 'strings', 'numbers', 'data', 'control', 'variables', 'layout', 'errors',
         'objects', 'old code')

def table_cells(line):
    """A table row's cells, split at the pipes outside code spans; a
    backslash before a pipe makes it the cell's own."""
    out, cur, code, i = [], '', False, 0
    s = line.strip()[1:]
    while i < len(s):
        c = s[i]
        if c == '\\' and s[i + 1:i + 2] == '|':
            cur, i = cur + '|', i + 2
            continue
        if c == '`':
            code = not code
        if c == '|' and not code:
            out.append(cur.strip())
            cur = ''
        else:
            cur += c
        i += 1
    return out

def differences_example(n, program, perl_says, curly_says, tmp):
    """One row of "Run for this file": the program under perl and under
    the compiler, held to what the row says of each."""
    path = f'{tmp}/d{n}.pl'
    with open(path, 'w', encoding='utf-8') as f:
        f.write('use v5.42;\n' + program + '\n')
    what = f'{DIFF}: `{program}`'
    p = subprocess.run([PERL, path], capture_output=True, stdin=subprocess.DEVNULL, timeout=60)
    bad = []
    if perl_says.startswith('dies'):
        if p.returncode != 255:
            bad.append(f'{what}: perl is said to die, and exits {p.returncode}')
    else:
        lines = [''] if perl_says.startswith('an empty line') else re.findall(r'`([^`]*)`', perl_says)
        want = ''.join(l + '\n' for l in lines).encode()
        if p.stdout != want or p.returncode != 0:
            bad.append(f'{what}: perl is said to print {want!r}, and prints {p.stdout!r}, exit {p.returncode}')
        if bool(p.stderr) != ('warns' in perl_says):
            bad.append(f'{what}: perl {"warns" if p.stderr else "does not warn"}: {clip(p.stderr)}')
    c = subprocess.run(['node', 'bin/curlyc.ts', '-o', f'{tmp}/d{n}', path], capture_output=True)
    kind = curly_says.split(':')[0].split()[0] if curly_says else ''
    if kind == 'Refused':
        if c.returncode != 1:
            bad.append(f'{what}: said to be refused, and the compiler exits {c.returncode}')
        return bad
    if kind not in ('Fault', 'Same'):
        return bad + [f'{what}: its Curly cell begins with none of Refused, Fault, Same']
    if c.returncode != 0:
        return bad + [f'{what}: said to run, and it does not compile: {clip(c.stderr)}']
    env = dict(os.environ)
    env.update(knobs())
    r = run_capped([f'{tmp}/d{n}'], env, b'', 60)
    if r is None:
        return bad + [f'{what}: the compiled program did not finish']
    if kind == 'Same':
        if (r.stdout, r.returncode) != (p.stdout, p.returncode) or r.stderr:
            bad.append(f'{what}: said to be the same as perl, and prints {r.stdout!r}, exit {r.returncode}: {clip(r.stderr)}')
    else:
        said = re.search(r'`([^`]+)`', curly_says)
        if r.returncode != 1 or not said or f'fault: ' not in r.stderr.decode() or said.group(1) not in r.stderr.decode():
            bad.append(f'{what}: said to fault with {said.group(1) if said else "?"!r}, and exits {r.returncode}: {clip(r.stderr)}')
        if not p.stdout.startswith(r.stdout):
            bad.append(f'{what}: before its fault it prints {r.stdout!r}, which perl does not begin with')
    return bad

def check_differences():
    """docs/DIFFERENCES.md (D103): each program of its "Run for this
    file" does under perl and under the compiler what its row says;
    each rated row has a Feel, a Met and a Where from the lists, names
    decisions that exist, and stands in a section its ratings belong
    to; and every decision of the log is cited in the file or listed
    under "Decisions that say nothing here"."""
    import concurrent.futures
    import tempfile
    text = open(DIFF, encoding='utf-8').read()
    log = open('docs/DECISIONS.md', encoding='utf-8').read()
    decided = set(int(n) for n in re.findall(r'(?m)^\*\*D(\d+)\.', log))
    bad, rated, examples, allowed, header = [], 0, [], None, None
    for line in text.split('\n'):
        m = re.match(r'<!-- rows: ([^;]*); (.*?) -->', line)
        if m:
            allowed = ([w.strip() for w in m.group(1).split(',')], [w.strip() for w in m.group(2).split(',')])
        if line.startswith('## '):
            allowed = None
        if not line.startswith('|'):
            header = None
            continue
        cells = table_cells(line)
        if header is None:
            header = cells
            continue
        if set(''.join(cells)) <= set('-: '):
            continue
        row = clip(cells[0].encode(), 60)
        if header == ['Program', 'perl 5.42', 'Curly']:
            program = re.fullmatch(r'`(.*)`', cells[0])
            if len(cells) != 3 or not program:
                bad.append(f'{DIFF}: a row of programs is not a program in a code span and two cells: {row}')
            else:
                examples.append((program.group(1), cells[1], cells[2]))
        elif header == ['Perl', 'Curly', 'Feel', 'Met', 'Where', 'Decision']:
            rated += 1
            if len(cells) != 6:
                bad.append(f'{DIFF}: a rated row has {len(cells)} cells, not 6: {row}')
                continue
            feel, met, where, ds = cells[2], cells[3], [w.strip() for w in cells[4].split(',')], re.findall(r'\bD(\d+)\b', cells[5])
            if feel not in FEEL or met not in MET or not where or any(w not in WHERE for w in where):
                bad.append(f'{DIFF}: Feel, Met or Where is not from the lists ({feel}; {met}; {cells[4]}): {row}')
            elif allowed is None:
                bad.append(f'{DIFF}: a rated row in a section that does not say which rows are its own: {row}')
            elif feel not in allowed[0] or met not in allowed[1]:
                bad.append(f'{DIFF}: rated {feel}, {met}, in the section for {", ".join(allowed[0])}; {", ".join(allowed[1])}: {row}')
            if not ds or any(int(d) not in decided for d in ds):
                bad.append(f'{DIFF}: names no decision, or one the log does not have ({cells[5]}): {row}')
    if not rated or not examples:
        bad.append(f'{DIFF}: {rated} rated rows and {len(examples)} programs: the file has lost its tables')
    cited = set(int(n) for n in re.findall(r'\bD(\d+)\b', text))
    for a, b in re.findall(r'\bD(\d+) to D(\d+)\b', text):
        cited.update(range(int(a), int(b) + 1))
    for n in sorted(decided - cited):
        bad.append(f'{DIFF}: D{n} is not in it: say what a Perl programmer will notice, or list it under '
                   f'"Decisions that say nothing here"')
    for n in sorted(cited - decided):
        bad.append(f'{DIFF}: it cites D{n}, which the log does not have')
    with tempfile.TemporaryDirectory() as tmp:
        with concurrent.futures.ThreadPoolExecutor(int(os.environ.get('JOBS', os.cpu_count() or 2))) as pool:
            for found in pool.map(lambda a: differences_example(a[0], *a[1], tmp), enumerate(examples)):
                bad += found
    print(f'differences: {rated} rated rows, {len(examples)} programs run under perl and the compiler, '
          f'{len(decided)} decisions accounted for')
    return bad

def main(argv):
    os.chdir(ROOT)
    what = argv[0] if argv else 'all'
    if what == 'models':
        bad = check_models('--write' in argv)
    elif what == 'tests':
        bad = check_tests()
    elif what == 'oracle':
        bad = check_oracle('--write' in argv)
    elif what == 'commits':
        upstream = subprocess.run(['git', 'rev-parse', '--verify', '-q', 'origin/main'], capture_output=True).returncode == 0
        bad = check_commits(argv[1] if len(argv) > 1 else 'origin/main..HEAD' if upstream else 'HEAD')
    elif what == 'commit-msg':
        bad = check_commit_msg(argv[1], '--staged' in argv)
    elif what == 'doctor':
        bad = doctor()
    elif what == 'census':
        bad = check_census()
    elif what == 'differences':
        bad = check_differences()
    elif what == 'all':
        bad = check_models() + check_tests() + check_oracle() + check_census() + check_differences()
    else:
        sys.exit(__doc__)
    for b in bad:
        print(f'FAIL {b}')
    print(f'{what}: {len(bad)} failed')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main(sys.argv[1:])
