# kind: fault
# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $u;
    say(join(',', 1, "", 2));
}
{
    my $u;
    say(join(',', 1, $u, 2));
}
say(2);
