use v5.42;
my %h=(a=>1); my $r=\$h{a}; delete $h{a}; $$r=9; print exists $h{a} ? 1 : 0, "$$r\n";
