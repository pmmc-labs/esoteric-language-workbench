# kind: refused
# perl warns: say (...) interpreted as function. The while is not on the
# line the brackets close on (T128).
use v5.42;
my $i = 0;
say ("a")
  while $i++ < 2;
