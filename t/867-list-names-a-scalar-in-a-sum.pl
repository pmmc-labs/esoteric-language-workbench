# kind: refused
# Named anywhere in the list, whatever it stands in (D77, T162): here perl
# prints 2, and the language has one rule for every shape.
use v5.42;
my $p = 1;
for my $x ($p + 1) {
    $p++;
    say $x;
}
