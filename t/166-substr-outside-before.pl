# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(('[' . substr('abc', (-5), 2)) . ']');
say(substr('abc', (-5), 1));
say(2);
