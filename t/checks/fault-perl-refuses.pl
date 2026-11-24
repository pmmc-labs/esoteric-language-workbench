# check: fails: perl does not compile it
# kind: fault
# perl can't compile it, so it prints nothing, and nothing is the start of
# anything: a check that only compared stdout would pass this.
use v5.42;
say 1 <=> 2 == -1;
