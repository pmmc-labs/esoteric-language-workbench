// Bytes to tokens. The source is the file's bytes as a latin1 string, so one
// char is one byte and columns are byte columns (LANGUAGE.md, Programs).
import { compileError } from './errors.ts';
import type { Pos } from './errors.ts';

export type StringPart =
  | { kind: 'text'; value: string }
  // The tokens of one {expr}, without an end-of-file token; pos is the `{`.
  | { kind: 'interp'; pos: Pos; tokens: Token[] };

export type Token =
  | { kind: 'int'; text: string; pos: Pos; value: bigint }
  | { kind: 'string'; text: string; pos: Pos; parts: StringPart[] }
  | { kind: 'name' | 'kw' | 'op' | 'newline' | 'eof'; text: string; pos: Pos };

const KEYWORDS = new Set(
  'and break continue else false fn for if in let nil not or return true while'.split(' '),
);
// Longest first, so `..=` beats `..` and `==` beats `=`.
const OPERATORS = [
  '..=', '==', '!=', '<=', '>=', '+=', '-=', '*=', '/=', '%=', '..',
  '<', '>', '=', '+', '-', '*', '/', '%', '.', ',', ';', ':', '(', ')', '[', ']', '{', '}',
];
const MAX_INT = 9223372036854775807n;
const ESCAPES: Record<string, string> = { n: '\n', t: '\t', r: '\r', '\\': '\\', '"': '"', '{': '{', '}': '}' };

const isDigit = (c: string) => c >= '0' && c <= '9';
const isAlpha = (c: string) => (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c === '_';
const isWord = (c: string) => isAlpha(c) || isDigit(c);

export function lex(src: string): Token[] {
  let i = 0;
  let line = 1;
  let lineStart = 0;
  const pos = (): Pos => ({ line, col: i - lineStart + 1 });

  // Lex tokens until the end of the source, or, inside an interpolation,
  // until the `}` that closes it (consumed). Returns the tokens.
  function tokens(inInterp: boolean, open: Pos): Token[] {
    const out: Token[] = [];
    let parens = 0; // open ( and [ : newlines inside them are not statement ends
    let braces = 0; // open { inside an interpolation
    for (;;) {
      const c = src[i];
      if (c === undefined) {
        if (inInterp) throw compileError(open, 'unterminated interpolation');
        out.push({ kind: 'eof', text: '', pos: pos() });
        return out;
      }
      if (c === ' ' || c === '\t' || c === '\r') { i++; continue; }
      if (c === '\n') {
        if (inInterp) throw compileError(open, 'unterminated interpolation');
        const last = out[out.length - 1];
        if (parens === 0 && last !== undefined && last.kind !== 'newline') {
          out.push({ kind: 'newline', text: '\n', pos: pos() });
        }
        i++; line++; lineStart = i;
        continue;
      }
      if (c === '/' && src[i + 1] === '/') {
        while (i < src.length && src[i] !== '\n') i++;
        continue;
      }
      const start = pos();
      if (isDigit(c)) { out.push(number(start)); continue; }
      if (isAlpha(c)) {
        const from = i;
        while (i < src.length && isWord(src[i])) i++;
        const text = src.slice(from, i);
        out.push({ kind: KEYWORDS.has(text) ? 'kw' : 'name', text, pos: start });
        continue;
      }
      if (c === '"') { out.push(string(start, inInterp ? open : null)); continue; }
      const op = OPERATORS.find((o) => src.startsWith(o, i));
      if (op === undefined) {
        const code = c.charCodeAt(0);
        throw compileError(start, code >= 0x20 && code < 0x7f
          ? `unexpected character '${c}'`
          : `unexpected byte 0x${code.toString(16).toUpperCase().padStart(2, '0')}`);
      }
      if (inInterp && op === '}' && braces === 0) { i++; return out; }
      if (op === '(' || op === '[') parens++;
      else if ((op === ')' || op === ']') && parens > 0) parens--;
      else if (op === '{') braces++;
      else if (op === '}' && braces > 0) braces--;
      i += op.length;
      out.push({ kind: 'op', text: op, pos: start });
    }
  }

  function number(start: Pos): Token {
    const from = i;
    while (i < src.length && isWord(src[i])) i++;
    const text = src.slice(from, i);
    if (!/^[0-9]+(_[0-9]+)*$/.test(text)) throw compileError(start, 'malformed number');
    const value = BigInt(text.replace(/_/g, ''));
    if (value > MAX_INT) throw compileError(start, 'integer literal too large');
    return { kind: 'int', text, pos: start, value };
  }

  // `within` is the `{` of the interpolation this string is written in, if any:
  // a string that runs off the line there means the interpolation did.
  function string(start: Pos, within: Pos | null): Token {
    const unterminated = () =>
      compileError(within ?? start, within ? 'unterminated interpolation' : 'unterminated string');
    const from = i;
    i++; // the opening quote
    const parts: StringPart[] = [];
    let text = '';
    const flush = () => { if (text !== '') parts.push({ kind: 'text', value: text }); text = ''; };
    for (;;) {
      const c = src[i];
      if (c === undefined || c === '\n') throw unterminated();
      if (c === '"') { i++; break; }
      if (c === '\\') {
        const e = src[i + 1];
        if (e === undefined || e === '\n') throw unterminated();
        const esc = ESCAPES[e];
        if (esc === undefined) throw compileError(pos(), `unknown escape '\\${e}'`);
        text += esc;
        i += 2;
        continue;
      }
      if (c === '{') {
        const open = pos();
        i++;
        const inner = tokens(true, open);
        if (inner.length === 0) throw compileError(open, 'empty interpolation');
        flush();
        parts.push({ kind: 'interp', pos: open, tokens: inner });
        continue;
      }
      text += c;
      i++;
    }
    flush();
    return { kind: 'string', text: src.slice(from, i), pos: start, parts };
  }

  return tokens(false, { line: 1, col: 1 });
}
