use v5.42;
my $s = "abc";
my $n = 1;
$s =~ s/a/$n+1/e;
print "$s\n";
