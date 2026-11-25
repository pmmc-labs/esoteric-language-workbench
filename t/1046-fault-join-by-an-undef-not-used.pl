# kind: fault
# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $u;
    say(join("", 1));
}
{
    my $u;
    say(join($u, 1));
}
say(2);
