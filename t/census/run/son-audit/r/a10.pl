use v5.42;
my $c=0; my $f=sub { $c++ }; $f->(); $f->(); print "$c\n";
