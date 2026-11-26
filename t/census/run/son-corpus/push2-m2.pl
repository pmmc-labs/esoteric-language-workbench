use v5.42;
sub mk { my @p; push @p, 1; push @p, 2; return "@p" } print mk(), mk(), "\n";
