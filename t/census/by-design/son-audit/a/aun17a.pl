use v5.42;
local $_ = "a"; sub t { $_ = "b" } my $x = $_; t(); print "$x$_\n";
