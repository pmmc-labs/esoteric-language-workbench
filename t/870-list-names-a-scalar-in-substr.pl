# kind: refused
# perl: 5; substr's first argument is the variable, to a foreach (T162).
use v5.42;
my $p = 1;
for my $x (substr($p, 0, 1)) {
    $p = 5;
    say $x;
}
