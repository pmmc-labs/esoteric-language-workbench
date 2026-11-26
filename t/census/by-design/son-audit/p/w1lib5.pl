use v5.42;
my $f = sub { $main::g += 10 }; my $x = $main::g; for my $i (1..3) { print "$main::g\n"; $f->(); } print "$main::g\n";
