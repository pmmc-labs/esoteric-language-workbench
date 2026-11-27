# kind: refused
# perl runs it: '\n'.
use v5.42;
for my $x ([1]) {
    say ref;
}
