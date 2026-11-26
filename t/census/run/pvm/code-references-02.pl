use v5.42;
sub f ($) { 1 }
my $p = prototype \&f;
print "[$p]\n";
