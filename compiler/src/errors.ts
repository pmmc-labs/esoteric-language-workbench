// A compile error is a plain Error carrying a position; the first one
// stops compilation (D29).
export type Pos = { line: number; col: number };
export type CompileError = Error & { pos: Pos; isCompileError: true };

export function compileError(pos: Pos, message: string): CompileError {
  return Object.assign(new Error(message), { pos, isCompileError: true as const });
}

export function isCompileError(e: unknown): e is CompileError {
  return e instanceof Error && (e as any).isCompileError === true;
}

export function formatError(path: string, e: CompileError): string {
  return `${path}:${e.pos.line}:${e.pos.col}: error: ${e.message}`;
}
