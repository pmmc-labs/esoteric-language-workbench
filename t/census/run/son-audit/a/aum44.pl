use v5.42;
my @a=(1); my $f = sub { @a = (7,8); 0 }; print "@a", $f->(), "@a", "\n";
