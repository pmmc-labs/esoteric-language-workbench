# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(index('abc', 'c', 9223372036854775807));
say(index('abc', 'c', 1e+30));
say(2);
