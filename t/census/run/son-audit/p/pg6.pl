use v5.42;
our $g = 1; my $f = sub { $g = 7 }; my $a = $g; $f->(); print "$a $g\n";
