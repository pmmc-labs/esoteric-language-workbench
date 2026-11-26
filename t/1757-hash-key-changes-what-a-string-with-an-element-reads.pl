# kind: refused
# perl: 1!. Refused a little more widely than it has to be (T230).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my $i = "a";
$h{$i = "b"} = "$h{$i}!";
say $h{b};
