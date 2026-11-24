# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(length('ab' x 1000));
say(length('ab' x 1073741824));
say(2);
