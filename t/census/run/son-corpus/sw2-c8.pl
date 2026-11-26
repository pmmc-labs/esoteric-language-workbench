use v5.42;
my $t = 1; my $f = sub { return $t * 2 }; print $f->(), "\n";
