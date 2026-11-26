# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2);
    my %h = (@a);
    say((scalar(keys(%h)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h{$_}) ? $h{$_} : 'undef')) . '>' } ((sort keys(%h))))));
}
{
    my @a = (1, 2, 3);
    my %h = (@a);
    say((scalar(keys(%h)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h{$_}) ? $h{$_} : 'undef')) . '>' } ((sort keys(%h))))));
}
say(2);
