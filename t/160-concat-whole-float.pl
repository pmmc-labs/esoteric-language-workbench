# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say('a' . 999999999999999.0);
say('a' . 1000000000000000.0);
say(2);
