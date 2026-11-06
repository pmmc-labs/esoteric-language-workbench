#!/usr/bin/env node
// The driver: read, compile to C, write it next to the output, link it
// with the runtime. `node bin/langc.ts -o out file.lang`.
// Exit codes: 0 ok, 1 compile error, 2 usage, toolchain or file error.
import { readFileSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { read } from '../compiler/src/reader.ts';
import { compileProgram } from '../compiler/src/codegen.ts';
import { CompileError } from '../compiler/src/errors.ts';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const usage = () => { console.error('usage: langc -o out file.lang'); process.exit(2); };

const args = process.argv.slice(2);
const at = args.indexOf('-o');
if (at < 0 || args.length !== 3) usage();
const out = args[at + 1]!;
const src = args.find((a, i) => i !== at && i !== at + 1)!;
if (out.startsWith('-')) usage();

let text: string;
try { text = readFileSync(src, 'utf8'); }
catch (e) { console.error(`langc: can't read ${src}: ${(e as Error).message}`); process.exit(2); }

let c: string;
try { c = compileProgram(read(text)); }
catch (e) {
    if (e instanceof CompileError) { console.error(`${src}:${e.line}:${e.col}: ${e.message}`); process.exit(1); }
    console.error(`langc: internal error: ${(e as Error).stack}`); process.exit(2);
}

try { writeFileSync(`${out}.c`, c); }
catch (e) { console.error(`langc: can't write ${out}.c: ${(e as Error).message}`); process.exit(2); }

const cc = (process.env.LANG_CC ?? 'cc').split(' ');
const r = spawnSync(cc[0]!, [...cc.slice(1), '-O1', '-Wall', `-I${join(root, 'runtime')}`, '-o', out, `${out}.c`, join(root, 'runtime', 'rt.c')], { stdio: 'inherit' });
if (r.error) { console.error(`langc: can't run ${cc[0]}: ${r.error.message}`); process.exit(2); }
process.exit(r.status === 0 ? 0 : 2);
