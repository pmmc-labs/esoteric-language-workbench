use v5.42;
my $z=0; my %h; eval { $h{a} = 1; $h{b} = 3 % $z; $h{c} = 1; }; print join("",sort keys %h),"\n";
