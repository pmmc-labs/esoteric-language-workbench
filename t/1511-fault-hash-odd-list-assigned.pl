# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    %h = (a => 1, b => 2);
    say((scalar(keys(%h)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h{$_}) ? $h{$_} : 'undef')) . '>' } ((sort keys(%h))))));
}
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    %h = (a => 1, 'b');
    say((scalar(keys(%h)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h{$_}) ? $h{$_} : 'undef')) . '>' } ((sort keys(%h))))));
}
say(2);
