# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub none() {
    return;
}
sub show($p = 'default') {
    return $p;
}
say(1);
say(show(!none()));
say(show(none()));
say(2);
