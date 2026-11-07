// The reader: text to forms, each with the line and column of its first
// character. It also refuses what the language can't have before running (D33).
import { CheckError } from './errors.ts';

// How deeply a program may nest (D30). The host's stack is about 10,000 frames of
// plain recursion on Node 22 and 24, and the reader, checker and evaluator each
// take a few per level, so a fixed limit well under that is the same on both.
export const MAX_DEPTH = 1000;

// The 63-bit range (D4).
export const INT_MIN = -(2n ** 62n);
export const INT_MAX = 2n ** 62n - 1n;

export type Form =
  | { kind: 'int'; value: bigint; line: number; col: number }
  | { kind: 'bool'; value: boolean; line: number; col: number }
  | { kind: 'sym'; name: string; line: number; col: number }
  | { kind: 'list'; items: Form[]; line: number; col: number };

type Tok = { t: '(' | ')' | 'atom'; text: string; line: number; col: number };

// Whitespace is any \s, so a form feed can't stall the scan. An atom ends at
// whitespace, a parenthesis or a semicolon, and `;` runs to the end of the line.
function tokenize(text: string): { toks: Tok[]; line: number; col: number } {
  const toks: Tok[] = [];
  let line = 1;
  let col = 1;
  let i = 0;
  while (i < text.length) {
    const c = text[i]!;
    if (c === '\n') { line++; col = 1; i++; continue; }
    if (/\s/.test(c)) { col++; i++; continue; }
    if (c === ';') {
      while (i < text.length && text[i] !== '\n') { i++; col++; }
      continue;
    }
    if (c === '(' || c === ')') {
      toks.push({ t: c, text: c, line, col });
      i++; col++;
      continue;
    }
    const start = i;
    const sl = line;
    const sc = col;
    while (i < text.length && !/[\s();]/.test(text[i]!)) { i++; col++; }
    toks.push({ t: 'atom', text: text.slice(start, i), line: sl, col: sc });
  }
  return { toks, line, col };
}

type State = { toks: Tok[]; p: number };

// An integer is an optional `-` and decimal digits; `007` and `-0` read as the
// integer they name (D33). Any other `#` word is an unknown name.
function atom(tok: Tok): Form {
  const { text: s, line, col } = tok;
  if (/^-?[0-9]+$/.test(s)) {
    const value = BigInt(s);
    if (value < INT_MIN || value > INT_MAX) throw new CheckError(line, col, 'integer out of range');
    return { kind: 'int', value, line, col };
  }
  if (s === '#true' || s === '#false') return { kind: 'bool', value: s === '#true', line, col };
  if (s.startsWith('#')) throw new CheckError(line, col, `unknown name ${s}`);
  return { kind: 'sym', name: s, line, col };
}

// Recursive on purpose: the nesting limit (D30) is what keeps it inside the stack.
function form(s: State, depth: number): Form {
  const tok = s.toks[s.p++]!;
  if (tok.t === ')') throw new CheckError(tok.line, tok.col, 'unexpected )');
  if (tok.t === 'atom') return atom(tok);
  if (depth + 1 > MAX_DEPTH) throw new CheckError(tok.line, tok.col, `nested more than ${MAX_DEPTH} deep`);
  const items: Form[] = [];
  for (;;) {
    const next = s.toks[s.p];
    // Reported at the innermost open paren, the one the scan reaches the end under.
    if (next === undefined) throw new CheckError(tok.line, tok.col, 'unclosed (');
    if (next.t === ')') {
      s.p++;
      return { kind: 'list', items, line: tok.line, col: tok.col };
    }
    items.push(form(s, depth + 1));
  }
}

// A program is one expression (LANGUAGE.md), and nothing may follow it.
export function read(text: string): Form {
  const { toks, line, col } = tokenize(text);
  const s: State = { toks, p: 0 };
  if (s.p === toks.length) throw new CheckError(line, col, 'expected an expression');
  const f = form(s, 0);
  if (s.p < toks.length) {
    const extra = toks[s.p]!;
    throw new CheckError(extra.line, extra.col, 'expected end of file after the expression');
  }
  return f;
}
