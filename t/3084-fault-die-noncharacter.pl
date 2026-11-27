# kind: fault
# A noncharacter in an uncaught message: perl warns (T307).
use v5.42;
use open ':std', ':encoding(UTF-8)';
say "before";
die "\x{fdd0}";
