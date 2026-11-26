use v5.42;
my $i=0; my $f=sub { $i++ }; while ($i<3) { $f->() } print "$i\n";
