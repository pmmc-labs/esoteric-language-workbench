# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my @r = ((map { $h{a} } (values(%h))));
    $h{a} = 9;
    say((scalar(keys(%h)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h{$_}) ? $h{$_} : 'undef')) . '>' } ((sort keys(%h))))));
}
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my @r = ((map { $h{a} = 9; $h{a} } (values(%h))));
}
say(2);
