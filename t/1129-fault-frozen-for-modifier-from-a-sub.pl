# kind: fault
# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a = (1, 2, 3);
sub poke() {
    $a[2] = 30;
    return 0;
}
say(1);
say($_) for (@a);
poke() for (@a);
say(2);
