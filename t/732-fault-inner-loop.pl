# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    OUT: for (my $i = 0; $i < 3; $i++) {
        for (my $j = 0; $j < 3; $j++) {
            next OUT if $j == $i;
            say(6 / ($i - $j));
        }
    }
}
{
    OUT: for (my $i = 0; $i < 3; $i++) {
        for (my $j = 0; $j < 3; $j++) {
            next OUT if $j > $i;
            say(6 / ($i - $j));
        }
    }
}
say(2);
