# kind: refused
# perl chomps $_, which is undef here, and warns.
use v5.42;
chomp;
