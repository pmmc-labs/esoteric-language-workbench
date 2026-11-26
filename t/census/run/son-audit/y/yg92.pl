use v5.42;
my @v = (1, 2.5, "a", undef, "", 0, "0", "0.0", "00", " ", "0E0"); print join("", map { $_ ? "t" : "f" } @v), "\n";
