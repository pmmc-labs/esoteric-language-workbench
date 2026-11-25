# kind: refused
# perl runs it by itself, before anything else (T28).
use v5.42;
sub BEGIN() { say "begin"; }
say "x";
