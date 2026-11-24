# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(index('abcabc', 'a', '0.9999999999999999'));
say(index('abcabc', 'a', '0.99999999999999995'));
say(2);
