use v5.42;
my $a = $ENV{X} // "Az";
my $b = $ENV{Y} // "zz";
my $c = $ENV{Z} // "a9";
$a++;
$b++;
$c++;
print "$a $b $c\n";
