# kind: refused
# perl reads this one as written, and warns when it runs: an undef is no number (D48).
use v5.42;
say undef == 1;
