use v5.42;
# $s is read again only by a test of truth, which reads the string's bytes
# without to_str. With the variables left out of the mark and the check in
# to_str alone, this prints what perl prints. (Two allocations stand between,
# not one: line 7's string is in t1 as well as in $s until line 8 has t1.)
my $y = "q";
my $s = "a" . $y;
my $t = "b" . $y;
my $u = "c" . $y;
if ($s) { say "true"; }
