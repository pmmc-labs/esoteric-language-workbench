use v5.42;
my $n = 0;
my $r = qr/a(?{ $n = 7 })b/;
my $s = "ab";
$s =~ $r;
print "$n\n";
