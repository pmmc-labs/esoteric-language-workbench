use v5.42;
my %h; $h{$_}++ for qw(a b a); print join(",", map {"$_$h{$_}"} sort keys %h),"\n";
