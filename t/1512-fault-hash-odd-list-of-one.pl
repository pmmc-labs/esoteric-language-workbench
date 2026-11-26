# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h;
    %h = ();
    say((scalar(keys(%h)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h{$_}) ? $h{$_} : 'undef')) . '>' } ((sort keys(%h))))));
}
{
    my %h;
    %h = ('a');
    say((scalar(keys(%h)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h{$_}) ? $h{$_} : 'undef')) . '>' } ((sort keys(%h))))));
}
say(2);
