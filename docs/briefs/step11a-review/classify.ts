// What the compiler makes of each string: refused, with its message, or
// the pieces its lexer found. Read by compiler.py, which holds them to the
// reviewer's model. JSON in ({ header, wrap, bodies }), JSON out.
//
//     node docs/briefs/step11a-review/classify.ts < bodies.json
import { readFileSync } from 'node:fs';
import { lex } from '../../../compiler/src/lexer.ts';
import type { Index } from '../../../compiler/src/lexer.ts';
import { parse } from '../../../compiler/src/parser.ts';
import { resolve } from '../../../compiler/src/resolver.ts';
import { check } from '../../../compiler/src/checker.ts';
import { CompileError } from '../../../compiler/src/errors.ts';

const { header, wrap, bodies } = JSON.parse(readFileSync(0, 'utf8')) as { header: string; wrap: [string, string]; bodies: string[] };
const index = (x: Index): unknown =>
    x.kind === 'var' ? ['v', x.name] : x.kind === 'range' ? ['range', index(x.from), index(x.to)] : ['n', (x.negative ? -1 : 1) * Number(x.text)];
const out = bodies.map(body => {
    const src = `${header}${wrap[0]}print "${body}";${wrap[1]}\n`;
    try {
        const tokens = lex(src);
        const at = tokens.findLastIndex(t => t.kind === 'word' && t.text === 'print');
        const s = tokens[at + 1]!;
        // The body is one string and then `;`, or it is not what was asked.
        if (s.kind !== 'str' || tokens[at + 2]?.kind !== ';' || s.text.length !== body.length + 2) return { no: 'the string ends before the body does' };
        const program = parse(tokens);
        check(program, resolve(program));
        const pieces = s.pieces === undefined ? (s.value === '' ? [] : [['text', s.value]]) : s.pieces.map(p =>
            p.kind === 'text' ? ['text', p.value]
            : p.kind === 'var' ? ['scalar', p.name]
            : p.kind === 'array' ? ['array', p.name]
            : p.kind === 'lastindex' ? ['last', p.name]
            : p.kind === 'elem' ? ['elem', p.name, index(p.index)]
            : ['slice', p.name, p.indexes.map(index)]);
        return { ok: pieces };
    } catch (e) {
        if (e instanceof CompileError) return { no: e.message };
        throw e;
    }
});
process.stdout.write(JSON.stringify(out));
