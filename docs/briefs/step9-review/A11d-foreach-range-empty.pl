use v5.42;
my @r = (5 .. -1e19);
say scalar(@r);
for my $i (5 .. -1e19) { say $i; }
say "not reached";
