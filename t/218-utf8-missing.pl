# kind: refused
# perl doesn't compile it: a source past ASCII needs `use utf8` (T73).
use v5.42;
say "é";
