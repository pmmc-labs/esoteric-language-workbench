// The compiler's passes up to the checker, over many probes in one
// process: for each path on stdin, a line of JSON, `{ path, ok }` or `{
// path, at, refused }`. census.py asks this first, since most probes are
// refused and a process each would be most of the census's time; a probe
// that passes is compiled by the driver itself, which has the last word.
import { readFileSync } from 'node:fs';
import { lex } from '../../compiler/src/lexer.ts';
import { parse } from '../../compiler/src/parser.ts';
import { resolve } from '../../compiler/src/resolver.ts';
import { check } from '../../compiler/src/checker.ts';
import { CompileError } from '../../compiler/src/errors.ts';

for (const path of readFileSync(0, 'utf8').split('\n').filter(p => p !== '')) {
    let line: unknown;
    try {
        const program = parse(lex(readFileSync(path, 'utf8')));
        check(program, resolve(program));
        line = { path, ok: true };
    } catch (e) {
        // Anything else is the compiler's own failure: the driver is asked,
        // and says so.
        line = e instanceof CompileError ? { path, at: `${e.line}:${e.col}`, refused: e.message } : { path, ok: true };
    }
    console.log(JSON.stringify(line));
}
