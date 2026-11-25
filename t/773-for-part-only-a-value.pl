# kind: refused
# perl warns: Useless use of addition (+) in void context (T122).
use v5.42;
my $i = 0;
for ($i + 1; $i < 3; $i++) {
    say $i;
}
