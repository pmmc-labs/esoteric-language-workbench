#!/usr/bin/env node
// The driver: read a SMOL program and run it. `node bin/smol.ts file.smol`.
// Exit codes: 0 ok, 1 a syntax error or a fault, 2 usage or a file it can't read.
import { readFileSync } from 'node:fs';
import { program } from '../compiler/src/program.ts';
import { parse } from '../compiler/src/parser.ts';
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
    // The one writer of the program's output: print's lines and the last
    // value both go through it, so they come out in order (D38).
    const write = (line: string): void => console.log(line);
    try {
        const value = evaluate(program(text), write);
        // The prelude's last statement is an expression, so a program with no
        // statements of its own would print its value. Only a program with
        // statements of its own prints one.
        if (value !== undefined && parse(text).length > 0) write(show(value));
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
