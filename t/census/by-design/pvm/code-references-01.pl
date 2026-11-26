use v5.42;
sub twice { return $_[0] * 2 }
my $c = \&twice;
print $c->(21), "\n";
