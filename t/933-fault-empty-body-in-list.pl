# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub empty() {
}
sub show($p = 'default') {
    return $p;
}
say(1);
{
    empty();
    say(show(empty() // 'scalar'));
}
say(show(1 ? empty() : 0));
say(2);
