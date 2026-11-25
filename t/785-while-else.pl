# kind: refused
# perl doesn't compile it either.
use v5.42;
my $i = 0;
while ($i++ < 3) {
    print $i;
} else {
    say "x";
}
