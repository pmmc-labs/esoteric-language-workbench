# kind: refused
# perl makes $x the loop's own while it runs and gives it back after: this
# prints 1, 2 and then 0.
use v5.42;
my $x;
for $x (1, 2) {
    say $x;
}
say defined($x) ? 1 : 0;
