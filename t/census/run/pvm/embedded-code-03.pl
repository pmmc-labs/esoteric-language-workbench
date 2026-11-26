use v5.42;
my $s = "abc";
my $n = 1;
my $k = 0;
$s =~ s{a}{ $n + length("))") }e;
$s =~ /b(?{ $k = length("}}}") })/;
my $r = qr/c(?{ $k = $k + length("}}") })/;
$s =~ $r;
print "$s $k\n";
