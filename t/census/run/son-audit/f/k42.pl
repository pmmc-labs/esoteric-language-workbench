use v5.42;
my $x=1; my $f=sub { $x }; { my $x=2; print $f->(); } print $f->(), "\n";
