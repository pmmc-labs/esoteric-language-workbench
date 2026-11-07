// The driver (D28, D34): reads a program, checks it, evaluates it, and reports
// the result with the exit status D34 gives. Nothing is written to stdout but the
// value, and the status is set with process.exitCode, never process.exit(), so
// output in flight to a pipe is flushed.
import { readFileSync } from 'node:fs';
import { CheckError, Fault } from '../interp/src/errors.ts';
import { read } from '../interp/src/reader.ts';
import { check } from '../interp/src/check.ts';
import { evaluate, show } from '../interp/src/evaluate.ts';

function run(args: string[]): number {
  if (args.length !== 1) {
    process.stderr.write('usage: node bin/lang.ts FILE\n');
    return 2;
  }
  const file = args[0]!;
  let text: string;
  try {
    text = readFileSync(file, 'utf8');
  } catch (e) {
    process.stderr.write(`${file}: cannot read: ${(e as Error).message}\n`);
    return 2;
  }
  try {
    const form = read(text);
    check(form);
    process.stdout.write(`${show(evaluate(form))}\n`);
    return 0;
  } catch (e) {
    if (e instanceof CheckError) {
      process.stderr.write(`${file}:${e.line}:${e.col}: ${e.message}\n`);
      return 2;
    }
    if (e instanceof Fault) {
      process.stderr.write(`fault: ${e.message}\n`);
      return 1;
    }
    process.stderr.write(`lang: internal error: ${(e as Error).stack ?? String(e)}\n`);
    return 3;
  }
}

process.exitCode = run(process.argv.slice(2));
