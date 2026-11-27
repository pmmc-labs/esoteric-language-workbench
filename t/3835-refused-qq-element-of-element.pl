# kind: refused
# perl prints 1: an element through a reference in qq waits for step 13d.
use v5.42;
my %h = (a => { b => 1 });
say qq($h{a}{b});
