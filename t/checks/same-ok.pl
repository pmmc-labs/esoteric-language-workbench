# check: ok
# What a same test is: perl compiles it in silence, runs it in silence, and
# prints the .expected under every seed. Hashes are here, each sorted in
# one of the ways the reading rule knows.
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2);
say join ",", sort keys %h;
say join ",", sort { $a <=> $b } values %h;
say join ",", map { "$_=$h{$_}" } sort keys %h;
say join ",", sort map { $_ * 2 } grep { $_ > 1 } values %h;
for my $k (reverse sort keys %h) { say $k }
say scalar(keys %h);
my %copy;
%copy = (fig => 2);
my $r = \%h;
say join ",", sort keys %$r;
say exists $h{fig} ? "fig" : "no fig";
say 7 % 3;
printf "%s has %d\n", "apple", $h{apple};
