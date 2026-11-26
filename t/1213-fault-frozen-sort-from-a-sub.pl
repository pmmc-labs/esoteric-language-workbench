# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a = (3, 1, 2);
sub poke() {
    $a[2] = 30;
    return 0;
}
say(1);
{
    my @r = ((sort { $a <=> $b } (@a)));
}
{
    my @r = ((sort { poke(); $a <=> $b } (@a)));
}
say(2);
