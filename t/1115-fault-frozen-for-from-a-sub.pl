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
{
    for (@a) {
        say($_);
    }
}
{
    for (@a) {
        poke();
        last;
    }
}
say(2);
