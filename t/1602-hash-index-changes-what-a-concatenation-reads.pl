# kind: refused
# an array's element too, since step 9: 2v (T230).
use v5.42;
my @a;
my $i = 0;
$a[$i = 2] = $i . "v";
say $a[2];
