// The command line (D31): build FILE -o EXE, run FILE, c FILE.
import { spawnSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { codegen } from './codegen.ts';
import { formatError, isCompileError } from './errors.ts';
import { lex } from './lexer.ts';
import { parse } from './parser.ts';
import { resolve } from './resolve.ts';

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..');

// Source text is bytes held as a latin1 string (see lexer.ts).
export function compile(src: string, path: string): string {
  return codegen(resolve(parse(lex(src))), path);
}

const USAGE = `usage: ditto build FILE -o EXE
       ditto run FILE
       ditto c FILE`;

function usage(): never {
  console.error(USAGE);
  process.exit(2);
}

function readSource(path: string): string {
  try {
    return readFileSync(path, 'latin1');
  } catch {
    console.error(`ditto: cannot read ${path}`);
    process.exit(2);
  }
}

function toC(path: string): string {
  try {
    return compile(readSource(path), path);
  } catch (e) {
    if (!isCompileError(e)) throw e;
    console.error(formatError(path, e));
    process.exit(2);
  }
}

// Writes EXE.c and compiles it with the runtime. Exit 3 if the C compiler
// fails, which is always a compiler bug (D31).
function build(path: string, exe: string) {
  const c = toC(path);
  mkdirSync(dirname(exe), { recursive: true });
  writeFileSync(exe + '.c', c);
  const cc = process.env.LANG_CC || 'cc';
  const flags = (process.env.LANG_CFLAGS || '').split(/\s+/).filter((f) => f !== '');
  const r = spawnSync(cc, ['-std=c11', '-O1', ...flags, '-I', join(root, 'runtime'),
    exe + '.c', join(root, 'runtime', 'ditto.c'), '-o', exe], { stdio: ['ignore', 'inherit', 'inherit'] });
  if (r.status !== 0) {
    console.error(`ditto: the C compiler failed on ${exe}.c (a compiler bug)`);
    process.exit(3);
  }
}

export function main(argv: string[]) {
  const [cmd, file, ...rest] = argv;
  if (cmd === 'c' && file !== undefined && rest.length === 0) {
    process.stdout.write(toC(file));
  } else if (cmd === 'build' && file !== undefined && rest.length === 2 && rest[0] === '-o') {
    build(file, rest[1]);
  } else if (cmd === 'run' && file !== undefined && rest.length === 0) {
    const exe = join(root, 'build', 'run', basename(file).replace(/\.ditto$/, ''));
    build(file, exe);
    const r = spawnSync(exe, { stdio: 'inherit' });
    process.exit(r.status ?? 1);
  } else {
    usage();
  }
}
