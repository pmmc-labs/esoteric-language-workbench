import type { Program } from "./parser.ts";

// Step 0 has no names, so nothing to resolve; the pass exists so later
// steps add to it rather than reshape the pipeline.
export function resolve(prog: Program): Program {
  return prog;
}
