use v5.42;
my $a = $ARGV[0] // 2;
my $b = $ARGV[1] // 3;
my $c = $ARGV[2] // 2;
my $right = $a ** $b ** $c;
my $left = ($a ** $b) ** $c;
my $minus = $a - $b - $c;
print "$right $left $minus\n";
