use v5.42;
# The statement with the most temporaries in the program (one) ends in an
# operator that allocates with that temporary as its operand. If the last
# slot of the frame is left out of the mark, t1 dies inside rt_concat_to.
my $p = "a";
my $s = "s";
$s .= $p . "b";
say $s;
