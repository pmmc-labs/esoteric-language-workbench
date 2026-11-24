# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(('[' . substr("", (-1), 1)) . ']');
say(substr("", (-1), 0));
say(2);
