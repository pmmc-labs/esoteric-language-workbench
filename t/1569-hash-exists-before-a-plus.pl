# kind: refused
# perl dies: exists argument is not a HASH or ARRAY element or a subroutine (T220).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say exists $h{a} + 1;
