// The reader: text to forms, each with its line and column (1-based).
// It keeps its own stack, so how deep a program nests is its rule
// (D30) and not the host's. A column counts code points (D31): the host's
// index counts UTF-16 units, so the reader steps a code point at a time.

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

// White space is these four and nothing else (D31): the host's \s would
// take U+00A0 and U+FEFF. A quote ends a name or an integer, as a bracket
// does (D31), so `(str/len"a")` reads.
const SPACE = new Set([" ", "\t", "\n", "\r"]);
const DELIMS = new Set([" ", "\t", "\n", "\r", "(", ")", ";", '"']);
const HEX = /^[0-9a-fA-F]$/;

export function read(src: string): Form {
  let i = 0, line = 1, col = 1;
  const stack: { items: Form[]; line: number; col: number }[] = [];
  let top: Form | undefined;

  // One code point: a surrogate pair is two units of the host's string
  // and one column (D31).
  const adv = () => {
    const cp = src.codePointAt(i)!;
    i += cp > 0xffff ? 2 : 1;
    if (cp === 0x0a) { line++; col = 1; } else col++;
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
    else if (SPACE.has(c)) adv();
    else if (c === "(") {
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
    } else if (c === '"') put(literal());
    else {
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

  // A literal from its opening quote, which is at i, to its closing one
  // (D31). The escapes are D31's; each error is D34's, at its place.
  function literal(): Form {
    const sl = line, sc = col;
    adv();
    let v = "";
    for (;;) {
      if (i >= src.length) throw new CheckError("unclosed string", sl, sc);
      const d = src[i];
      if (d === '"') { adv(); return { t: "str", v, line: sl, col: sc }; }
      if (d === "\n") throw new CheckError("newline in string", line, col);
      if (d !== "\\") {
        v += String.fromCodePoint(src.codePointAt(i)!);
        adv();
        continue;
      }
      const bl = line, bc = col;
      adv();
      if (i >= src.length) throw new CheckError("unclosed string", sl, sc);
      const e = src[i];
      if (e === '"' || e === "\\") v += e;
      else if (e === "n") v += "\n";
      else if (e === "t") v += "\t";
      else if (e === "u") v += unicodeEscape(bl, bc);
      else throw new CheckError("bad escape", bl, bc);
      if (e !== "u") adv();
    }
  }

  // At the `u` of \u{X}: one to six hex digits, a code point (not past
  // 10FFFF, not a surrogate). Leaves i past the closing brace.
  function unicodeEscape(bl: number, bc: number): string {
    adv();
    if (src[i] !== "{") throw new CheckError("bad escape", bl, bc);
    adv();
    let hex = "";
    while (i < src.length && HEX.test(src[i])) { hex += src[i]; adv(); }
    if (src[i] !== "}" || hex.length < 1 || hex.length > 6)
      throw new CheckError("bad escape", bl, bc);
    adv();
    const cp = parseInt(hex, 16);
    if (cp > 0x10ffff || (cp >= 0xd800 && cp <= 0xdfff))
      throw new CheckError("bad escape", bl, bc);
    return String.fromCodePoint(cp);
  }

  if (stack.length) {
    const l = stack[stack.length - 1];
    throw new CheckError("unclosed (", l.line, l.col);
  }
  if (top === undefined) throw new CheckError("expected an expression", line, col);
  return top;
}
