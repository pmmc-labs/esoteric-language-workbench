# kind: refused
# through a sub: 2v (T230).
use v5.42;
my @a;
my $i = 0;
sub bump() { $i = 2; return 2 }
$a[bump()] = $i . "v";
say $a[2];
