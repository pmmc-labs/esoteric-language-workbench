# kind: dies
# A message that ends in a newline has nothing added (T301).
use v5.42;
print "before\n";
die "stopped\n";
