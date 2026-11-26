# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    for my $v (values(%h)) {
        say($h{a});
        last;
    }
}
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    for my $v (values(%h)) {
        @h{'a', 'b'} = (1, 2);
        last;
    }
}
say(2);
