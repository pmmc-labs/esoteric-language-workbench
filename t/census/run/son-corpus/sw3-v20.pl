use v5.42;
my @a; $a[2] = "x"; print scalar(@a), defined $a[0] ? "d" : "u", "\n";
