#!/usr/bin/env node
// The driver: lex, parse, check, generate C next to the output, compile
// it and the runtime, link them. `node bin/curlyc.ts -o out file.pl`.
// Exit codes: 0 ok; 1 a refusal (`FILE:LINE:COL: message`, and no binary);
// 2 usage, the toolchain, or a file it can't read or write.
import { readFileSync, rmSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { lex } from '../compiler/src/lexer.ts';
import { parse } from '../compiler/src/parser.ts';
import { check } from '../compiler/src/checker.ts';
import { resolve } from '../compiler/src/resolver.ts';
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

let bytes: Buffer;
try { bytes = readFileSync(src); }
catch (e) { console.error(`curlyc: can't read ${src}: ${(e as Error).message}`); process.exit(2); }

// The source is UTF-8 (D24), and a file that isn't is refused here, at
// the first byte that isn't: decoded leniently it would be U+FFFD, which
// is a character a string may hold. (Bytes that don't come back the same
// from a decoding and an encoding weren't UTF-8.)
const text = bytes.toString('utf8');
const back = Buffer.from(text, 'utf8');
if (!back.equals(bytes)) {
    let at = 0;
    while (at < bytes.length && bytes[at] === back[at]) at += 1;
    const before = bytes.subarray(0, at).toString('utf8').split('\n');
    rmSync(out, { force: true });
    console.error(`${src}:${before.length}:${[...before.at(-1)!].length + 1}: a byte that is not UTF-8`);
    process.exit(1);
}

// A refusal leaves no binary (D13), an old one included: a test that ran
// the last build's would pass for a program that no longer compiles.
let c: string;
try {
    const program = parse(lex(text));
    check(program);
    c = generate(program, resolve(program), src);
} catch (e) {
    try { rmSync(out, { force: true }); } catch { /* not a file of ours to remove */ }
    if (e instanceof CompileError) { console.error(`${src}:${e.line}:${e.col}: ${e.message}`); process.exit(1); }
    // The passes walk the tree by recursion, and Node's stack holds a few
    // thousand levels: brackets that deep, or an expression of that many
    // terms. Not a refusal (the program may be fine), but not a mystery.
    if (e instanceof RangeError) { console.error(`curlyc: ${src} nests too deeply for the compiler: an expression of thousands of terms, or of brackets`); process.exit(2); }
    console.error(`curlyc: internal error: ${(e as Error).stack}`); process.exit(2);
}

try { writeFileSync(`${out}.c`, c); }
catch (e) { console.error(`curlyc: can't write ${out}.c: ${(e as Error).message}`); process.exit(2); }

// The runtime is compiled for speed and the program is not: its C is a
// long run of calls with nothing in it to optimize, and gcc at -O1 takes
// more than proportionally longer over a long function (36 seconds for
// ten thousand statements, against 6 at -O0).
const cc = (process.env.CURLY_CC ?? 'cc').split(' ');
const run = (args: string[]): void => {
    const r = spawnSync(cc[0]!, [...cc.slice(1), '-Wall', `-I${join(root, 'runtime')}`, ...args], { stdio: 'inherit' });
    if (r.error) { console.error(`curlyc: can't run ${cc[0]}: ${r.error.message}`); process.exit(2); }
    if (r.status !== 0) process.exit(2);
};
run(['-O1', '-c', '-o', `${out}.rt.o`, join(root, 'runtime', 'rt.c')]);
// -lm: `**` is the C library's pow (D35).
run(['-O0', '-o', out, `${out}.c`, `${out}.rt.o`, '-lm']);
