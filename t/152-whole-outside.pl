# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(('[' . substr('abc', 0, 9223372036854775807)) . ']');
say(substr('abc', 0, 1e+30));
say(2);
