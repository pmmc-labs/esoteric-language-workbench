# kind: refused
# perl: the line of the for; refused all the same.
use v5.42;
my $x;
for my $i (1,
  $x // die "u") { say $i; }
