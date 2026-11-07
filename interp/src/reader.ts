// The reader: text to forms, each with its line and column (1-based).
// It keeps its own stack, so how deep a program nests is its rule
// (D30) and not the host's.

export type Form =
  | { t: "int"; v: bigint; line: number; col: number }
  | { t: "bool"; v: boolean; line: number; col: number }
  | { t: "str"; v: string; line: number; col: number }
  | { t: "sym"; name: string; line: number; col: number }
  | { t: "list"; items: Form[]; line: number; col: number };

import { CheckError } from "./errors.ts";

export const MIN = -(1n << 62n);
export const MAX = (1n << 62n) - 1n;
export const MAX_DEPTH = 1000;

// A `"` ends a name as a bracket does (D31).
const DELIMS = new Set([" ", "\t", "\n", "\r", "(", ")", ";", '"']);
const HEX = /^[0-9a-fA-F]$/;

export function read(src: string): Form {
  let i = 0, line = 1, col = 1;
  const stack: { items: Form[]; line: number; col: number }[] = [];
  let top: Form | undefined;

  // One code point at a time, so a column counts code points, not the
  // UTF-16 units the host indexes by (D31).
  const adv = () => {
    if (src[i] === "\n") { line++; col = 1; } else col++;
    i += src.codePointAt(i)! > 0xffff ? 2 : 1;
  };
  // A string literal; i is at the opening quote (D31).
  const readString = (): string => {
    const sl = line, sc = col;
    let v = "";
    adv();
    for (;;) {
      if (i >= src.length) throw new CheckError("unclosed string", sl, sc);
      const c = src[i];
      if (c === '"') { adv(); return v; }
      if (c === "\n") throw new CheckError("newline in a string (write \\n)", line, col);
      if (c !== "\\") { v += String.fromCodePoint(src.codePointAt(i)!); adv(); continue; }
      const el = line, ec = col;
      adv();
      const e = src[i];
      if (e === undefined) throw new CheckError("unclosed string", sl, sc);
      if (e === '"' || e === "\\") v += e;
      else if (e === "n") v += "\n";
      else if (e === "t") v += "\t";
      else if (e === "u") {
        adv();
        if (src[i] !== "{") throw new CheckError("bad escape \\u: expected {", el, ec);
        adv();
        let hex = "";
        while (i < src.length && src[i] !== "}" && src[i] !== '"' && src[i] !== "\n") { hex += String.fromCodePoint(src.codePointAt(i)!); adv(); }
        if (src[i] !== "}") throw new CheckError("unclosed \\u{", el, ec);
        if (hex === "") throw new CheckError("empty \\u{}", el, ec);
        if (hex.length > 6) throw new CheckError("\\u{...} longer than six digits", el, ec);
        if (![...hex].every((h) => HEX.test(h))) throw new CheckError(`\\u{${hex}} is not hex`, el, ec);
        const cp = parseInt(hex, 16);
        if (cp >= 0xd800 && cp <= 0xdfff) throw new CheckError(`\\u{${hex}} is a surrogate`, el, ec);
        if (cp > 0x10ffff) throw new CheckError(`\\u{${hex}} is past 10FFFF`, el, ec);
        v += String.fromCodePoint(cp);
      } else throw new CheckError(`bad escape \\${String.fromCodePoint(e.codePointAt(0)!)}`, el, ec);
      adv();
    }
  };
  // A finished form goes into the list being read, or is the program.
  const put = (f: Form) => {
    if (stack.length) stack[stack.length - 1].items.push(f);
    else if (top === undefined) top = f;
    else throw new CheckError("unexpected form after the program", f.line, f.col);
  };

  while (i < src.length) {
    const c = src[i];
    if (c === ";") { while (i < src.length && src[i] !== "\n") adv(); }
    else if (c === " " || c === "\t" || c === "\n" || c === "\r") adv();
    else if (c === '"') {
      const sl = line, sc = col;
      put({ t: "str", v: readString(), line: sl, col: sc });
    } else if (c === "(") {
      if (stack.length === 0 && top !== undefined)
        throw new CheckError("unexpected form after the program", line, col);
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
  if (top === undefined) throw new CheckError("expected an expression", line, col);
  return top;
}
