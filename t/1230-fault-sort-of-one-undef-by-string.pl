# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @u = ((undef));
    my @r = ((sort { ($a cmp $b) . "" } (@u)));
}
{
    my @u = ((undef));
    my @r = ((sort { $b cmp $a } (@u)));
}
say(2);
