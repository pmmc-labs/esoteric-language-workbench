use v5.42;
my $t = 0; my $f = sub { $t += 1 }; $f->(); print "$t\n";
