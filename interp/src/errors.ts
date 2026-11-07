// The two ways a run ends badly, each with its own exit status (D34).

// An error before running (D28, D33): the reader or the checker found it, at a
// position in the file. The driver reports it as FILE:LINE:COL: message, exit 2.
export class CheckError extends Error {
  readonly line: number;
  readonly col: number;
  constructor(line: number, col: number, message: string) {
    super(message);
    this.line = line;
    this.col = col;
  }
}

// A fault (D6): the program ran and stopped. The driver prints `fault: ` and the
// message, exit 1, and nothing on stdout, since a value is printed only at the end.
export class Fault extends Error {}
