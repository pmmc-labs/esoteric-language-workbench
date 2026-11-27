# kind: refused
# perl warns: Possible attempt to separate words with commas.
use v5.42;
say join "|", qw(a,b c);
