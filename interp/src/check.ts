// The checker: every error D28 says comes before running, found over the whole
// program, a branch never taken included, before anything is evaluated (D33).
// Step 0 has no operators or forms yet, so any list is an operator that isn't
// there; later steps add the table of what each head takes.
import { CheckError } from './errors.ts';
import type { Form } from './reader.ts';

export function check(f: Form): void {
  switch (f.kind) {
    case 'int':
    case 'bool':
      return;
    case 'sym':
      throw new CheckError(f.line, f.col, `unknown name ${f.name}`);
    case 'list': {
      const head = f.items[0];
      if (head === undefined) throw new CheckError(f.line, f.col, 'expected an operator');
      if (head.kind === 'sym') throw new CheckError(head.line, head.col, `unknown operator ${head.name}`);
      const what = head.kind === 'list' ? 'a list' : head.kind === 'int' ? 'an integer' : 'a boolean';
      throw new CheckError(head.line, head.col, `expected an operator, not ${what}`);
    }
  }
}
