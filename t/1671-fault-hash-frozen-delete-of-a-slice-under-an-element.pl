# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my @r = ();
    for my $v ($h{a}) {
        say($v);
        last;
    }
}
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    my @r = ();
    for my $v ($h{a}) {
        @r = (delete(@h{'b', 'c'}));
        last;
    }
}
say(2);
