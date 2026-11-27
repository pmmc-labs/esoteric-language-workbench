# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my %h;
say(exists($h{a}{b}) ? 1 : 0);
say(2);
