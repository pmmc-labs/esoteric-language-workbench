# kind: refused
# perl does not compile it: syntax error (T313, D144).
use v5.42;
{ defer { say "d"; } say "b"; }
