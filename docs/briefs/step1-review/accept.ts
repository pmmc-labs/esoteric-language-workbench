// Which programs the compiler accepts, against the model's verdict on each
// (gen.py writes them). Run from anywhere: node docs/briefs/step1-review/accept.ts
import { readFileSync } from 'node:fs';
import { lex } from '../../../compiler/src/lexer.ts';
import { parse } from '../../../compiler/src/parser.ts';
import { check } from '../../../compiler/src/checker.ts';
import { CompileError } from '../../../compiler/src/errors.ts';
let n = 0, both = 0, neither = 0, onlyModel = 0, onlyMine = 0;
const shown: string[] = [];
for (const line of readFileSync(new URL('../../../build/step1-review/cands.jsonl', import.meta.url), 'utf8').split('\n')) {
    if (!line) continue;
    const v = JSON.parse(line);
    let mine = true, why = '';
    try { check(parse(lex(v.s))); } catch (e) { if (!(e instanceof CompileError)) throw e; mine = false; why = e.message; }
    n++;
    if (mine && v.ok) both++; else if (!mine && !v.ok) neither++;
    else { if (mine) onlyMine++; else onlyModel++; if (shown.length < 15) shown.push(`${mine ? 'only the compiler accepts' : 'only the model accepts'}: ${JSON.stringify(v.s)} ${why}`); }
}
console.log({ n, both, neither, onlyModel, onlyMine });
for (const s of shown) console.log(s);
process.exit(onlyModel + onlyMine === 0 ? 0 : 1);
