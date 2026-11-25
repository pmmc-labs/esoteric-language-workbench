# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub ends($p) {
    if ($p) {
        say('yes');
    }
}
say(1);
ends(1);
my $v = ends(0);
say(2);
