# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(('[' . substr('abcdef', '1.9999999999999998')) . ']');
say(substr('abcdef', '1.99999999999999999'));
say(2);
