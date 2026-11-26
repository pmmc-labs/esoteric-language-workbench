use v5.42;
sub t { die "t\n" } my @l = (1, eval { t() }, 2); print scalar(@l),"\n";
