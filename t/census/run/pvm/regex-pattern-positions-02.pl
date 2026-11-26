use v5.42;
my $s = $ENV{X} // "abcabc";
$s =~ m/b/g;
my $a = pos($s);
pos($s) = 0;
$s =~ m/b/g;
my $b = pos($s);
print "$a $b\n";
