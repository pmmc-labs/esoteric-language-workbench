#!/usr/bin/env node
// The driver: read a SMOL program and run it. `node bin/smol.ts file.smol`.
// Exit codes: 0 ok, 1 a syntax error or a fault, 2 usage or a file it can't read.
import { readFileSync } from 'node:fs';
import { program } from '../compiler/src/program.ts';
import { evaluate, show } from '../compiler/src/eval.ts';
import { Failure } from '../compiler/src/errors.ts';

const main = (argv: string[]): number => {
    if (argv.length !== 1) {
        console.error('usage: smol file.smol');
        return 2;
    }
    const file = argv[0]!;
    let text: string;
    try { text = readFileSync(file, 'utf8'); }
    catch (e) {
        console.error(`smol: can't read ${file}: ${(e as Error).message}`);
        return 2;
    }
    try {
        const value = evaluate(program(text));
        if (value !== undefined) console.log(show(value));
        return 0;
    } catch (e) {
        if (e instanceof Failure) {
            if (e.pos) console.error(`${file}:${e.pos.line}:${e.pos.col}: ${e.message}`);
            else console.error(`fault: ${e.message}`);
            return 1;
        }
        console.error(`smol: internal error: ${(e as Error).stack}`);
        return 2;
    }
};

process.exitCode = main(process.argv.slice(2));
