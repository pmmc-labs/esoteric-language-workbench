// The reader: text to forms, each with its line and column (1-based).
// It keeps its own stack, so how deep a program nests is its rule
// (D30) and not the host's. A program is a sequence of forms; whether
// they are definitions and then one expression is the checker's to say
// (D31), so the reader only needs to read them.

export type Form =
  | { t: "int"; v: bigint; line: number; col: number }
  | { t: "bool"; v: boolean; line: number; col: number }
  | { t: "sym"; name: string; line: number; col: number }
  | ListForm;

export type ListForm = { t: "list"; items: Form[]; line: number; col: number };

import { CheckError } from "./errors.ts";

export const MIN = -(1n << 62n);
export const MAX = (1n << 62n) - 1n;
export const MAX_DEPTH = 1000;

const DELIMS = new Set([" ", "\t", "\n", "\r", "(", ")", ";"]);

export function read(src: string): Form[] {
  let i = 0, line = 1, col = 1;
  const stack: { items: Form[]; line: number; col: number }[] = [];
  const top: Form[] = [];

  const adv = () => {
    if (src[i] === "\n") { line++; col = 1; } else col++;
    i++;
  };
  // A finished form goes into the list being read, or is a form of the program.
  const put = (f: Form) => {
    if (stack.length) stack[stack.length - 1].items.push(f);
    else top.push(f);
  };

  while (i < src.length) {
    const c = src[i];
    if (c === ";") { while (i < src.length && src[i] !== "\n") adv(); }
    else if (c === " " || c === "\t" || c === "\n" || c === "\r") adv();
    else if (c === "(") {
      if (stack.length >= MAX_DEPTH)
        throw new CheckError(`nested too deeply (limit ${MAX_DEPTH})`, line, col);
      stack.push({ items: [], line, col });
      adv();
    } else if (c === ")") {
      const l = stack.pop();
      if (!l) throw new CheckError("unmatched )", line, col);
      put({ t: "list", items: l.items, line: l.line, col: l.col });
      adv();
    } else {
      const sl = line, sc = col, start = i;
      while (i < src.length && !DELIMS.has(src[i])) adv();
      const text = src.slice(start, i);
      if (/^-?[0-9]+$/.test(text)) {
        const v = BigInt(text);
        if (v < MIN || v > MAX)
          throw new CheckError(`integer ${text} is out of range (63 bits)`, sl, sc);
        put({ t: "int", v, line: sl, col: sc });
      } else if (text === "#true" || text === "#false") {
        put({ t: "bool", v: text === "#true", line: sl, col: sc });
      } else put({ t: "sym", name: text, line: sl, col: sc });
    }
  }
  if (stack.length) {
    const l = stack[stack.length - 1];
    throw new CheckError("unclosed (", l.line, l.col);
  }
  if (top.length === 0) throw new CheckError("expected an expression", line, col);
  return top;
}
