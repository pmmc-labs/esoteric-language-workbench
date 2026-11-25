# kind: refused
# perl takes it, and the statement before the while doesn't see the
# variable: it is declared after it.
use v5.42;
my $i = 0;
print $i while (my $x = $i++) < 2;
