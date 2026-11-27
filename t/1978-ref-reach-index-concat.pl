# kind: refused
# perl runs it, and says nothing.
use v5.42;
my $r = [];
my $i = 0;
$r->[$i = 2] = $i . "v";
