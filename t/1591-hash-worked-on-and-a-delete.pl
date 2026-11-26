# kind: refused
# perl: 3.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
$h{a} += delete($h{b});
say $h{a};
