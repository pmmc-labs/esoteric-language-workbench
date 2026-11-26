use v5.42;
my $g = $ENV{X} // "a\n";
eval { die $g, "b\n" };
my $wide = $@;
eval { die($g), "b\n" };
print "wide=", $wide, "narrow=", $@;
