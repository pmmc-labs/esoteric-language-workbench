use v5.42;
my $c = $ENV{X} // 0;
print "ran\n";
eval { exit $c };
print "trapped\n";
