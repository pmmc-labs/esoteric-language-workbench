# kind: refused
# perl prints ababab; with a variable on the left, `$s x3`, it doesn't compile (T57).
use v5.42;
say "ab" x3;
