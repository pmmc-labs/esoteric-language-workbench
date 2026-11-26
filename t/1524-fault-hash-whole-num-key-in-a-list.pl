# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %g = (0.5, 1);
    say((scalar(keys(%g)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($g{$_}) ? $g{$_} : 'undef')) . '>' } ((sort keys(%g))))));
}
{
    my %g = (1000000000000000.0, 1);
    say((scalar(keys(%g)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($g{$_}) ? $g{$_} : 'undef')) . '>' } ((sort keys(%g))))));
}
say(2);
