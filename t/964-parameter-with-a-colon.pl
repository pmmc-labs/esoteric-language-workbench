# kind: refused
# perl: A signature parameter must start with '$', '@' or '%' (T55).
use v5.42;
sub n(:$x) { return 1; }
