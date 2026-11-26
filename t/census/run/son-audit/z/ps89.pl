use v5.42;
my $str="aXbXc"; my @p; while ($str=~/([a-c])/g) { push @p,$1 } print "@p\n";
