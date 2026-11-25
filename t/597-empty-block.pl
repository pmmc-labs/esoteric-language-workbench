# kind: refused
# An empty pair of braces as a statement is an anonymous hash, to
# perl, which warns: Useless use of anonymous hash ({}) in void
# context (T116).
use v5.42;
say 1;
{ }
