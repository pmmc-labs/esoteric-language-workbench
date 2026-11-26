use v5.42;
my @out;
for my $i (1 .. 6) {
    next if $i == 2;
    next if $i == 4;
    push @out, $i;
}
print "@out\n";
