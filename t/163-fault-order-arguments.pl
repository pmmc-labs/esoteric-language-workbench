# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(substr('ab' x 2, '1' + 1));
say(substr('ab' x (-2), 'abc' + 1));
say(2);
