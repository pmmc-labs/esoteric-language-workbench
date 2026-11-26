# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (3, 1, 2);
    my @r = ((sort { my $t = 6 / $a; $a <=> $b } (@a)));
}
{
    my @a = (3, 0, 2);
    my @r = ((sort { my $t = 6 / $a; $a <=> $b } (@a)));
}
say(2);
