use v5.42;
my $calls = 0;
sub id { $calls++; return $_[0] }
my $out = "";
for my $x (1, 2, 3, 9) {
    next unless id($x) && id($x) > 1 && id($x) < 9;
    $out .= $x;
}
print "$out $calls\n";
