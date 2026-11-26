use v5.42;
my @a; $a[3] = 1; print scalar(@a), defined $a[0] ? "d" : "u", "\n";
