use v5.42;
my $a = $ENV{X} // 0;
print "[", !$a, "][", !!$a, "]\n";
