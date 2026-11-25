# kind: refused
# A my in a loop's test ends with the loop. perl doesn't compile it.
use v5.42;
my $i = 0;
while ((my $x = $i++) < 3) {
    say $x;
}
say $x;
