// The reader: text to forms, each with its line and column (1-based).
// `;` starts a comment. A token is a run of anything but whitespace,
// brackets and `;`. Iterative, with a stack of its own, so a program can
// nest as deep as memory allows.
import { CompileError } from "./errors.ts";

export const MIN = -(1n << 62n);
export const MAX = (1n << 62n) - 1n;

type Pos = { line: number; col: number };
export type Form =
  | ({ kind: "int"; value: bigint } & Pos)
  | ({ kind: "sym"; name: string } & Pos)
  | ({ kind: "list"; items: Form[] } & Pos);

export function read(text: string): Form[] {
  const top: Form[] = [];
  // Open lists, innermost last.
  const open: Extract<Form, { kind: "list" }>[] = [];
  const push = (f: Form) => (open.length ? open[open.length - 1].items : top).push(f);
  let line = 1, col = 1, i = 0;
  const adv = () => {
    if (text[i++] === "\n") { line++; col = 1; } else col++;
  };
  while (i < text.length) {
    const c = text[i];
    if (c === ";") { while (i < text.length && text[i] !== "\n") adv(); }
    else if (/\s/.test(c)) adv();
    else if (c === "(") { open.push({ kind: "list", items: [], line, col }); adv(); }
    else if (c === ")") {
      const l = open.pop();
      if (!l) throw new CompileError("unexpected )", line, col);
      push(l);
      adv();
    } else {
      const at = { line, col };
      let j = i;
      while (j < text.length && !/[\s();]/.test(text[j])) j++;
      const tok = text.slice(i, j);
      while (i < j) adv();
      if (/^-?[0-9]+$/.test(tok)) {
        const value = BigInt(tok);
        if (value < MIN || value > MAX) throw new CompileError(`integer out of range: ${tok}`, at.line, at.col);
        push({ kind: "int", value, ...at });
      } else push({ kind: "sym", name: tok, ...at });
    }
  }
  if (open.length) {
    const l = open[open.length - 1];
    throw new CompileError("unclosed (", l.line, l.col);
  }
  return top;
}
