# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %h = (a => 1, b => 2, c => 3, d => 4);
sub poke() {
    $h{a} = 30;
    return 0;
}
say(1);
{
    my @r = ((map { $h{a} } (values(%h))));
}
{
    my @r = ((map { poke(); $h{a} } (values(%h))));
}
say(2);
