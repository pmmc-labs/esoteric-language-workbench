use v5.42;
my $s = $ENV{X} // "ABC";
my @c = unpack("C3", $s);
print "@c\n";
