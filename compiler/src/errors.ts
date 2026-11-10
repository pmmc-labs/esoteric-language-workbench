// The one class in the interpreter: it plays the part of `raise`. A syntax
// error carries its position; a fault doesn't, because the program has run.
import type { Pos } from './ast.ts';

export class Failure extends Error {
    readonly pos: Pos | undefined;
    constructor(message: string, pos?: Pos) {
        super(message);
        this.pos = pos;
    }
}
