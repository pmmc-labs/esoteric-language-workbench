# kind: refused
# perl runs it, and says nothing.
use v5.42;
my %h;
my $k = "a";
$h{x}{$k = "b"} = "$k!";
