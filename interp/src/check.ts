// The checker: every error D28 says comes before running, found over the whole
// program, a branch never taken included, before anything is evaluated (D33).
// Pre-order, so the errors come in the order of the text: a form's own arity
// before the errors inside it.
import { CheckError } from './errors.ts';
import type { Form } from './reader.ts';
import { ARITY } from './table.ts';

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
      if (head.kind !== 'sym') {
        const what = head.kind === 'list' ? 'a list' : head.kind === 'int' ? 'an integer' : 'a boolean';
        throw new CheckError(head.line, head.col, `expected an operator, not ${what}`);
      }
      const arity = ARITY.get(head.name);
      if (arity === undefined) throw new CheckError(head.line, head.col, `unknown operator ${head.name}`);
      const n = f.items.length - 1;
      if (n !== arity) throw new CheckError(f.line, f.col, `${head.name} takes ${arity} arguments, not ${n}`);
      for (const arg of f.items.slice(1)) check(arg);
      return;
    }
  }
}
