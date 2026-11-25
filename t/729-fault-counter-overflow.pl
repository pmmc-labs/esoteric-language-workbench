# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $k = 0;
    {
        my $i = 9223372036854775805;
        while (($k++) < 2) {
            $i++;
            say($i);
        }
    }
}
{
    my $k = 0;
    {
        my $i = 9223372036854775805;
        while (($k++) < 5) {
            $i++;
            say($i);
        }
    }
}
say(2);
