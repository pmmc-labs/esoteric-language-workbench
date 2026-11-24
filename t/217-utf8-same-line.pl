# kind: refused
# perl doesn't compile it: `use utf8` is in force from the next line (T73).
use v5.42;
use utf8; say "é";
