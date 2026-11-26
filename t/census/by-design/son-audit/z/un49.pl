use v5.42;
my $ok=eval { die "x\n"; 1 }; print defined $ok ? "d" : "u", "\n";
