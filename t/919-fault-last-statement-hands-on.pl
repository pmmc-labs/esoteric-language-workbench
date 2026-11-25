# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub ends($p) {
    if ($p) {
        say('yes');
    }
}
sub tail($p) {
    ends($p);
}
say(1);
tail(1);
my $v = tail(0);
say(2);
