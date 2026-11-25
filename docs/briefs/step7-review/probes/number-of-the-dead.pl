use v5.42;
# The same, where a number is wanted: the bytes are read by from_string.
my $y = "2";
my $s = "4" . $y;
my $t = "b" . $y;
my $u = "c" . $y;
say $s + 1;
