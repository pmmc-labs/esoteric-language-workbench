use v5.42;
my $c = $ENV{X} // 0;
my @l = ($ENV{A} // "a", "b", "c");
OUTER: foreach my $x (@l) {
    foreach my $y (@l) {
        next OUTER if $y eq "b";
        last OUTER if $c;
        print $y;
    }
}
print "\n";
