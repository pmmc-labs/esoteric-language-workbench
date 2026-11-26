use v5.42;
my %seen; my @u = grep { !$seen{$_}++ } qw(a b a c b); print "@u\n";
