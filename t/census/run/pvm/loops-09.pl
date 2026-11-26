use v5.42;
my %seen;
my $out = "";
for my $k (qw(a a b a c)) {
    next if $seen{$k}++;
    $out .= $k;
}
print "$out\n";
