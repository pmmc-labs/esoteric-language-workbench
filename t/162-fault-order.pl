# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(('1' + 1) . ('a' x 1));
say(('abc' + 1) . ('a' x (-1)));
say(2);
