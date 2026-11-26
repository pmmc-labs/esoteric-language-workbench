# kind: refused
# perl joins the slice: 1 2. Not in a string (D99).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say "@h{'a','b'}";
