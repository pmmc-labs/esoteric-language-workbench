use v5.42;
my @a=("a b","c"); my @w = map { split " " } @a; print scalar(@w),"\n";
