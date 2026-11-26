use v5.42;
for my $i (1 .. 2) { *f = sub { $i } } print f(), "\n";
