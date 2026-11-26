use v5.42;
my $x=1; my $f=sub { $x+=$_[0] }; for my $i (1..3) { $f->($i) } print "$x\n";
