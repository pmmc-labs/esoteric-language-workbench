use v5.42;
my $x = $ARGV[0] // 2;
my $loose = defined $x + 1;
my $tight = (defined $x) + 1;
print "$loose $tight\n";
