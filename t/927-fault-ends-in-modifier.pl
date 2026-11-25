# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub ends($p) {
    my $x = 1;
    $x = 7 if $p;
}
say(1);
ends(1) if 1;
if (ends(1)) {
    say('never');
}
say(2);
