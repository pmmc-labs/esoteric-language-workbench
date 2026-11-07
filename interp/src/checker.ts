// The checker: every error D28 says comes before running, found before
// anything is evaluated, in every branch whether taken or not (D7).
// It recurses; the reader has already bounded the depth (D30).

import { CheckError } from "./errors.ts";
import type { Form } from "./reader.ts";
import { OPERATORS } from "./evaluator.ts";

export function check(f: Form): void {
  switch (f.t) {
    case "int":
    case "bool":
      return;
    case "sym":
      throw new CheckError(`unknown name ${f.name}`, f.line, f.col);
    case "list": {
      const head = f.items[0];
      if (head === undefined || head.t !== "sym")
        throw new CheckError("a list must start with an operator", f.line, f.col);
      const arity = OPERATORS.has(head.name) ? 2 : head.name === "if" ? 3 : undefined;
      if (arity === undefined) throw new CheckError(`unknown name ${head.name}`, head.line, head.col);
      const n = f.items.length - 1;
      if (n !== arity)
        throw new CheckError(`${head.name} takes ${arity} arguments, not ${n}`, f.line, f.col);
      for (let k = 1; k <= n; k++) check(f.items[k]);
    }
  }
}
