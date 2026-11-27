# kind: fault
# A sort block's value outside 32 bits, in a try: not caught (T173, D13).
use v5.42;
my @a = (1, 2);
say "before";
try { my @s = sort { 2 ** 40 } @a } catch ($e) { say "caught" }
