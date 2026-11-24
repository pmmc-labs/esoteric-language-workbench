// A refusal (D13): a diagnostic with a position, raised where it is found
// and never kept in the tree (D29). This is the one class in the compiler;
// it plays the part of `die`.
import type { Pos } from './ast.ts';

export class CompileError extends Error {
    readonly line: number;
    readonly col: number;
    constructor(message: string, line: number, col: number) {
        super(message);
        this.line = line;
        this.col = col;
    }
}

export const refuse = (message: string, pos: Pos): never => {
    throw new CompileError(message, pos.line, pos.col);
};
