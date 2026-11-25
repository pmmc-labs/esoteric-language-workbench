# kind: refused
# perl takes it (T122, D60).
use v5.42;
my $i = 0;
for (; (my $c = $i) < 3; $i++) {
    say $c;
}
