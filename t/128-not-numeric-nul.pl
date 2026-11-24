# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say("3\x{B}" + 1);
say("3\x{0}" + 1);
say(2);
