use v5.42;
my $f = $ENV{X} // $^X;
print "[", (-e $f), "][", (-e($f)), "]\n";
