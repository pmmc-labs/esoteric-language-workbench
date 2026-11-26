# kind: refused
# perl reads both late: 14 (T213).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say(($h{a} = 5) + ($h{a} = 7));
