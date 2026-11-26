use v5.42;
my $s = "abc";
my $c = q{3*4};
$s =~ s/b/$c/ee;
print "$s\n";
