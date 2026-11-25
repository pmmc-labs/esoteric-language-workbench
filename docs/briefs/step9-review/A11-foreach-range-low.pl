use v5.42;
# As a list this range is two values. A foreach over it dies.
my $lo = -9223372036854775807 - 1;
my @r = ($lo .. $lo + 1);
say $r[0], " ", $r[1];
for my $i (0, $lo .. $lo + 1) { say $i; }
for my $i ($lo .. $lo + 1) { say $i; }
say "not reached";
