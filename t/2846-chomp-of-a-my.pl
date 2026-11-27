# kind: refused
# perl declares $t, assigns it and chomps it.
use v5.42;
my $s = "ab\n";
chomp(my $t = $s);
