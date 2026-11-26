# kind: refused
# perl reads the first key after the second has changed it: b is deleted twice, and a stays.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my $i = "a";
my @d = delete @h{$i, ($i = "b")};
say "@d", scalar(%h);
