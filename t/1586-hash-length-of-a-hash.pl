# kind: refused
# perl warns: length() used on %h (did you mean "scalar(keys %h)"?).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say length(%h);
