// The two ways a program ends badly, kept apart because the driver gives
// them different statuses (D6, D28). Anything else thrown is the
// interpreter's own fault (D30).

// An error before running: FILE:LINE:COL: message, exit 2.
export class CheckError extends Error {
  line: number;
  col: number;
  constructor(message: string, line: number, col: number) {
    super(message);
    this.line = line;
    this.col = col;
  }
}

// A fault at run time: `fault: NAME`, exit 1.
export class Fault extends Error {}
