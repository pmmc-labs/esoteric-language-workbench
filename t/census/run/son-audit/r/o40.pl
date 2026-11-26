use v5.42;
my %h; my $k="a"; $h{$k} = ($k="b"); print join(",",%h),"\n";
