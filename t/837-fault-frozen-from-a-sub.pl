# kind: fault
# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a = (1, 2, 3);
sub poke() {
    $a[2] = 30;
    return 0;
}
say(1);
for my $x (@a) {
    say($x);
}
for my $x (@a) {
    say($x);
    poke();
    last;
}
say(2);
