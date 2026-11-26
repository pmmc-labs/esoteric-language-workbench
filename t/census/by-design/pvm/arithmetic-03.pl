use v5.42;
my $a = $ARGV[0] // 2;
my $b = $ARGV[1] // 3;
my $c = $ARGV[2] // 4;
my $default = $a + $b * $c;
my $grouped = ($a + $b) * $c;
print "$default $grouped\n";
