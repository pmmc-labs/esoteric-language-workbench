# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my $k = 1e+16;
    say(defined($h{$k}) ? (('[' . $h{$k}) . ']') : 'undef');
}
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my $k = 9007199254740991.0;
    say(defined($h{$k}) ? (('[' . $h{$k}) . ']') : 'undef');
}
say(2);
