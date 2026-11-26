# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    say("<$h{a}>");
}
{
    my %h = (a => 1, b => 2, c => 3, d => 4);
    say("<$h{nope}>");
}
say(2);
