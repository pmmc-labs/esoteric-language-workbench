# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $i = 0;
    while (($i++) < 2) {
        my $x;
        say($x . 'a') if $i == 3;
        $x = 'set';
    }
}
{
    my $i = 0;
    while (($i++) < 2) {
        my $x;
        say($x . 'a') if $i == 2;
        $x = 'set';
    }
}
say(2);
