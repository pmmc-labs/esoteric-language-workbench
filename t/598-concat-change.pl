# kind: refused
# perl joins a row of dots as one operation and reads each piece
# late: this is 5a5 to perl, where one dot at a time gives 3a5 (T117, D57).
use v5.42;
my $x = 3;
say $x . "a" . ($x = 5);
