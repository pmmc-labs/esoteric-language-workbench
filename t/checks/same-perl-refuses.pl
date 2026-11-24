# check: fails: perl does not compile it
# Not Perl: the first half of D2.
use v5.42;
say 1 <=> 2 == -1;
