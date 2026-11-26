# kind: refused
# perl joins the pieces after the key is worked out: kkv (T230).
use v5.42;
my %g;
my $i = "a";
$g{$i = "k"} = $i . "v";
say %g;
