# check: fails: differs from perl
# perl leaves with 3, and the .expected doesn't say so.
use v5.42;
say "leaving";
exit 3;
