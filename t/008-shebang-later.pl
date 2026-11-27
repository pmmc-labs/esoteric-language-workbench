# kind: refused
# perl reads a `#!` line on whatever line it calls line 1, and a `# line`
# comment can make that any line (T72). perl prints 1 here and stops:
# `say 2;` has become the body of a loop over stdin, which is empty.
# From step 15 the `# line` comment is refused first, as a line directive
# (T74, D147); the `#!` line is refused all the same (see 007, and the
# lexer's unit tests).
use v5.42;
say 1;
# line 1
#!perl -n
say 2;
