# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = 9007199254740992.0;
    $v--;
    say(defined($v));
}
{
    my $v = 9007199254740994.0;
    $v--;
    say(defined($v));
}
say(2);
