# kind: refused
# perl dies: Use of freed value in iteration.
use v5.42;
my $r = [1, 2];
for my $x ($r->[0], $r->[1]) {
    $r = [7];
}
