# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(('[' . substr('abc', 3)) . ']');
say(substr('abc', 4));
say(2);
