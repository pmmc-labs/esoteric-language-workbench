# kind: refused
# perl: 4. The freeze is step 12b (D98).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
for my $v (values %h) { say $v if $v > 3; }
