# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(('[' . substr('abcdef', 1, '2.0')) . ']');
say(substr('abcdef', 1, '-0.99999999999999995'));
say(2);
