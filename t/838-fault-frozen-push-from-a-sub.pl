# kind: fault
# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a = (1, 2, 3);
sub grow() {
    push(@a, 9);
    return 0;
}
say(1);
for my $x (@a) {
    say($x);
}
for my $x (@a) {
    say($x);
    grow();
    last;
}
say(2);
