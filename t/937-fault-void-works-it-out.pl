# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub twice($p) {
    $p * 2;
}
sub tag($p) {
    return $p . 'a';
}
say(1);
{
    twice(4);
    tag('x');
}
twice((undef));
say(2);
