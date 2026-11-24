// The one class in the compiler: it plays the part of `raise`. Everything
// else is functions over immutable data, so it can be ported to the
// language itself line by line.
export class CompileError extends Error {
    readonly line: number;
    readonly col: number;
    constructor(message: string, line: number, col: number) {
        super(message);
        this.line = line;
        this.col = col;
    }
}
