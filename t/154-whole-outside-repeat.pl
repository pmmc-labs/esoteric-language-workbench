# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(('[' . ("" x 4611686018427387904)) . ']');
say("" x 1e+30);
say(2);
