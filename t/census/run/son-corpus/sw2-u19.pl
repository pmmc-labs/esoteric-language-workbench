use v5.42;
my @a = map { [$_, $_ * 2] } 1 .. 3; print join(",", map { $_->[1] } @a), "\n";
