# kind: refused
# perl warns: print (...) interpreted as function. The brackets don't
# close on the line they open on (T128).
use v5.42;
my $x = 1;
print ("a" .
"b") unless $x;
