import { fail } from "./errors.ts";

// k is "int" | "str" | "name" | "kw" | "op" | "eof". text is the source
// text (what error messages quote); val is the decoded string for "str",
// the digits for "int". Columns count bytes: the source is read as latin1.
export type Token = { k: string; text: string; val: string; line: number; col: number };

export const KEYWORDS = new Set([
  "fn", "let", "if", "else", "while", "return", "print", "write", "and", "or", "not",
]);

const INT64_MAX = 9223372036854775807n;

// Longest first, so `<-` is never `<` then `-` (LANGUAGE.md, lexical matters).
const OPS = ["<-", "<=", ">=", "!=", "+", "-", "*", "/", "%", "=", "<", ">", "@", "#",
  "(", ")", "[", "]", "{", "}", ","];

const ESCAPES: Record<string, string> = { n: "\n", t: "\t", '"': '"', "\\": "\\" };

const isDigit = (c: string) => c >= "0" && c <= "9";
const isLetter = (c: string) => (c >= "a" && c <= "z") || (c >= "A" && c <= "Z") || c === "_";

// A byte as an error message shows it: printable ASCII as itself, the
// rest as \xHH, so the message is always printable.
function show(c: string): string {
  const n = c.charCodeAt(0);
  return n >= 32 && n < 127 ? c : "\\x" + n.toString(16).padStart(2, "0");
}

export function lex(src: string): Token[] {
  const toks: Token[] = [];
  let i = 0, line = 1, lineStart = 0;
  const push = (k: string, text: string, val: string, at: number, ln: number, ls: number) =>
    toks.push({ k, text, val, line: ln, col: at - ls + 1 });

  while (i < src.length) {
    const c = src[i];
    if (c === "\n") { i++; line++; lineStart = i; continue; }
    if (c === " " || c === "\t" || c === "\r") { i++; continue; }
    if (c === ";") { while (i < src.length && src[i] !== "\n") i++; continue; }
    const start = i, col = i - lineStart + 1;
    if (isDigit(c)) {
      while (i < src.length && isDigit(src[i])) i++;
      const text = src.slice(start, i);
      if (BigInt(text) > INT64_MAX) fail(line, col, "integer literal out of range");
      push("int", text, text, start, line, lineStart);
    } else if (isLetter(c)) {
      while (i < src.length && (isLetter(src[i]) || isDigit(src[i]))) i++;
      const text = src.slice(start, i);
      push(KEYWORDS.has(text) ? "kw" : "name", text, text, start, line, lineStart);
    } else if (c === '"') {
      i++;
      let val = "";
      for (;;) {
        if (i >= src.length || src[i] === "\n") fail(line, col, "unterminated string");
        const d = src[i];
        if (d === '"') { i++; break; }
        if (d === "\\") {
          const e = src[i + 1];
          if (e === undefined || !(e in ESCAPES)) {
            // A newline or end of file after the backslash is an
            // unterminated string, not an escape.
            if (e === undefined || e === "\n") fail(line, col, "unterminated string");
            fail(line, i - lineStart + 1, `unknown escape \\${show(e)}`);
          }
          val += ESCAPES[e];
          i += 2;
        } else { val += d; i++; }
      }
      push("str", src.slice(start, i), val, start, line, lineStart);
    } else {
      const op = OPS.find((o) => src.startsWith(o, i));
      if (op === undefined) fail(line, col, `unexpected character '${show(c)}'`);
      i += op.length;
      push("op", op, op, start, line, lineStart);
    }
  }
  toks.push({ k: "eof", text: "", val: "", line, col: src.length - lineStart + 1 });
  return toks;
}
