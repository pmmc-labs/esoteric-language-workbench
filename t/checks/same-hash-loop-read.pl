# check: fails: values without sort
# The loop's variable is read, each way it can be: the order shows.
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
for my $v (values %h) { say $v; last; }
for (values %h) { say $_; last; }
for my $v (values %h) { say "$v"; last; }
my @l = map { $_ } values %h;
say @l;
say $_ for values(%h);
my @g = grep { 1 } values %h;
say @g;
