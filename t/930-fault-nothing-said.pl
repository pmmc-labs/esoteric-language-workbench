# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub none() {
    return;
}
say(1);
my $v = none();
say(none());
say(2);
