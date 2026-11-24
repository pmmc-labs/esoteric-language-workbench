# check: fails: differs from perl
# The .expected has lost its last newline: equal means every byte.
use v5.42;
say 42;
