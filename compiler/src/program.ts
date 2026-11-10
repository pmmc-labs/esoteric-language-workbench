// A program is the prelude's statements, then the program's own. The prelude
// is SMOL source in lib/prelude.smol, which makes Class and Object the way a
// program makes any class, so they are objects 1 and 2.
import { readFileSync } from 'node:fs';
import type { Stmt } from './ast.ts';
import { parse } from './parser.ts';

const PRELUDE = new URL('../../lib/prelude.smol', import.meta.url);

export const program = (text: string): Stmt[] => [...parse(readFileSync(PRELUDE, 'utf8')), ...parse(text)];
