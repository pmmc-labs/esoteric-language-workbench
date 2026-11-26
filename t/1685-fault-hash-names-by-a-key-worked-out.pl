# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my @b = (7);
    my @r = ((map { $h{a} } ($h{'a' . ""})));
}
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my @b = (7);
    my @r = ((map { $h{a} = 9; $h{a} } ($h{'a' . ""})));
}
say(2);
