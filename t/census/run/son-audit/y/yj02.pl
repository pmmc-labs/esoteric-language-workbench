use v5.42;
my $x=1; my $f = sub { $x++ }; $f->(); $f->(); print "$x\n";
