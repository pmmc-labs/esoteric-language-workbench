#!/usr/bin/env node
// The driver: lex, parse, check, generate C next to the output, link it
// with the runtime. `node bin/curlyc.ts -o out file.pl`.
// Exit codes: 0 ok; 1 a refusal (`FILE:LINE:COL: message`, and no binary);
// 2 usage, the toolchain, or a file it can't read or write.
import { readFileSync, rmSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { lex } from '../compiler/src/lexer.ts';
import { parse } from '../compiler/src/parser.ts';
import { check } from '../compiler/src/checker.ts';
import { generate } from '../compiler/src/codegen.ts';
import { CompileError } from '../compiler/src/errors.ts';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const usage = () => { console.error('usage: curlyc -o out file.pl'); process.exit(2); };

const args = process.argv.slice(2);
const at = args.indexOf('-o');
if (at < 0 || args.length !== 3) usage();
const out = args[at + 1]!;
const src = args.find((a, i) => i !== at && i !== at + 1)!;
if (out.startsWith('-')) usage();

// Bytes that aren't UTF-8 become U+FFFD, which the lexer refuses as it
// does every character past ASCII.
let text: string;
try { text = readFileSync(src, 'utf8'); }
catch (e) { console.error(`curlyc: can't read ${src}: ${(e as Error).message}`); process.exit(2); }

// A refusal leaves no binary (D13), an old one included: a test that ran
// the last build's would pass for a program that no longer compiles.
let c: string;
try {
    const program = parse(lex(text));
    check(program);
    c = generate(program, src);
} catch (e) {
    try { rmSync(out, { force: true }); } catch { /* not a file of ours to remove */ }
    if (e instanceof CompileError) { console.error(`${src}:${e.line}:${e.col}: ${e.message}`); process.exit(1); }
    console.error(`curlyc: internal error: ${(e as Error).stack}`); process.exit(2);
}

try { writeFileSync(`${out}.c`, c); }
catch (e) { console.error(`curlyc: can't write ${out}.c: ${(e as Error).message}`); process.exit(2); }

const cc = (process.env.CURLY_CC ?? 'cc').split(' ');
const r = spawnSync(cc[0]!, [...cc.slice(1), '-O1', '-Wall', `-I${join(root, 'runtime')}`, '-o', out, `${out}.c`, join(root, 'runtime', 'rt.c')], { stdio: 'inherit' });
if (r.error) { console.error(`curlyc: can't run ${cc[0]}: ${r.error.message}`); process.exit(2); }
process.exit(r.status === 0 ? 0 : 2);
