use v5.42;
my $s = "abc";
my $k = 0;
$s =~ /b(?{ $k = 5 })/;
print "$k\n";
