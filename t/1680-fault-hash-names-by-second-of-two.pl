# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my @b = (7);
    my @r = ((map { $h{a} } (@b, @h{'c', 'd'})));
}
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my @b = (7);
    my @r = ((map { $h{a} = 9; $h{a} } (@b, @h{'c', 'd'})));
}
say(2);
