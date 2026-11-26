use v5.42;
my $s = $ENV{X} // "a";
$s .= "b";
print "$s\n";
