// The generated C of every golden test that compiles, into a directory:
//   node docs/briefs/step7-review/gen.ts OUTDIR [t/NNN-name.pl ...]
// run from the repository's root, so that a fault names `t/NNN-name.pl`
// as the .expected has it. It is the driver's first half and no more.
import { readdirSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { basename, join } from 'node:path';
import { lex } from '../../../compiler/src/lexer.ts';
import { parse } from '../../../compiler/src/parser.ts';
import { check } from '../../../compiler/src/checker.ts';
import { resolve } from '../../../compiler/src/resolver.ts';
import { generate } from '../../../compiler/src/codegen.ts';

const [out, ...given] = process.argv.slice(2);
if (out === undefined) { console.error('usage: gen.ts OUTDIR [files]'); process.exit(2); }
mkdirSync(out, { recursive: true });
const files = given.length ? given : readdirSync('t').filter(f => f.endsWith('.pl')).sort().map(f => join('t', f));
let made = 0;
for (const src of files) {
    const text = readFileSync(src, 'utf8');
    if (/^# kind: refused$/m.test(text)) continue;
    try {
        const program = parse(lex(text));
        const names = resolve(program);
        check(program);
        writeFileSync(join(out, basename(src, '.pl') + '.c'), generate(program, names, src));
        made += 1;
    } catch (e) {
        console.error(`${src}: ${(e as Error).message}`);
    }
}
console.error(`${made} programs`);
