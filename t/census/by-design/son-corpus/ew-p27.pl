use v5.42;
sub show { return defined($main::v) ? "d" : "u" } print show(); $main::v = 1; print show(), "\n";
