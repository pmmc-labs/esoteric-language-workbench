# kind: refused
# perl folds the whole right side to a constant, and warns: Found = in
# conditional (T112).
use v5.42;
my $x = 0;
my $y = 3;
say "a" if $x = "p" . (1 || $y);
say $x;
