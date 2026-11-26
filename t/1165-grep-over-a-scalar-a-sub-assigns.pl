# kind: refused
# perl: 9 (D77).
use v5.42;
my $p = 1;
sub bump() {
    $p = 9;
    return 0;
}
my @r = grep { bump(); 1 } ($p);
say @r;
