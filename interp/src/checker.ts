// The checker: every error D28 says comes before running, found before
// anything is evaluated, in every branch whether taken or not.

import { CheckError } from "./errors.ts";
import type { Form } from "./reader.ts";

export function check(f: Form): void {
  if (f.t === "int") return;
  throw new CheckError("not an expression this interpreter knows", f.line, f.col);
}
