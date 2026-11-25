# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    for (my $i = 2; ($i > 0) && ((10 / $i) > 1); $i--) {
        say($i);
    }
}
{
    for (my $i = 2; (10 / $i) > 1; $i--) {
        say($i);
    }
}
say(2);
