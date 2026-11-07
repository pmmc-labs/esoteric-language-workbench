// The two ways a program ends without a value (D6, D28).

// An error found before anything runs: FILE:LINE:COL: message, exit 2.
export class CompileError extends Error {
  line: number;
  col: number;
  constructor(message: string, line: number, col: number) {
    super(message);
    this.line = line;
    this.col = col;
  }
}

// A fault: the program ends, `fault: message` on stderr, exit 1 (D6).
export class Fault extends Error {}
