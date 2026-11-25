# check: fails: printed more than
# limit: 20
# Where the language faults perl may only warn and carry on, so a loop
# that the fault alone would end never ends under perl; and one that
# prints as it goes would fill the checker's memory first. It is stopped.
use v5.42;
say "one";
print "x" x 1000, "\n" while 1;
