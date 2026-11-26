use v5.42;
my $r = $ENV{R} // 0;
my @l = ($ENV{A} // "a", "b", "c", "d");
foreach my $x (@l) {
    redo if $r;
    next if $x eq "b";
    last if $x eq "d";
    print $x;
}
print "\n";
