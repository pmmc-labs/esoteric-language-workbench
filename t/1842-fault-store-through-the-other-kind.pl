# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my %h = (a => [1]);
$h{a}{b} = 2;
say(2);
