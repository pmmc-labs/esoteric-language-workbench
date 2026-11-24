# check: fails: the .expected differs from perl
# Without `use open`, perl prints U+00E9 as the one byte E9, and says
# nothing (D39). The .expected here is the two bytes of UTF-8.
use v5.42;
say "\x{e9}";
