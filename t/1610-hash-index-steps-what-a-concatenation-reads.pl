# kind: refused
# through what perl folds away: 1v (T230).
use v5.42;
my @a;
my $i = 0;
$a[$i++] = 0 || $i . "v";
say $a[0];
