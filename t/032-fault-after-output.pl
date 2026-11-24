# kind: fault
# What was printed before a fault stays printed (D12), and the fault names
# the line its statement starts on (D34), which here is not the line of
# the operator that overflowed.
use v5.42;
say 1 + 2;
say 4 * 5;
say 1
    + 9223372036854775807
    + 3;
say 6;
