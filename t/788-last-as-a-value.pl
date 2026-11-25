# kind: refused
# perl takes it: say is never reached, and the loop is left (T120).
use v5.42;
my $i = 0;
while ($i++ < 3) {
    say last;
}
