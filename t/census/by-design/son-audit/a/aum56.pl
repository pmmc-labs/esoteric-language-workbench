use v5.42;
our @l = (1,2); for (@l) { inner(); } sub inner { $_ = 9 } print "@l\n";
