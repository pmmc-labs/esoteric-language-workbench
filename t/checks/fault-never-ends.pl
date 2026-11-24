# check: fails: perl did not finish
# kind: fault
# limit: 1
# The natural test of some faults never ends under perl (appending to an
# array inside a loop over it); this one only sleeps, to be cheap.
use v5.42;
say "one";
sleep 1 while 1;
