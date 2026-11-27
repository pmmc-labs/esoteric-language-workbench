# kind: fault
# perl warns: Use of uninitialized value $s in scalar chomp (T272).
use v5.42;
my $s;
chomp($s);
say "not reached";
