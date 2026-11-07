// A compile error is a plain object thrown from any pass and caught once
// in main.ts (D24, D29).
export type CompileError = { line: number; col: number; msg: string };

export function fail(line: number, col: number, msg: string): never {
  throw { line, col, msg } satisfies CompileError;
}

export function isCompileError(e: unknown): e is CompileError {
  return typeof e === "object" && e !== null && "msg" in e && "line" in e && "col" in e;
}

export function formatError(e: CompileError): string {
  return `error at ${e.line}:${e.col}: ${e.msg}`;
}
