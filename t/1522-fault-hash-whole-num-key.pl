# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my $k = 999999999999999.0;
    $h{$k} = 1;
}
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my $k = 1000000000000000.0;
    $h{$k} = 1;
}
say(2);
