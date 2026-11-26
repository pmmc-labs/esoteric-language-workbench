use v5.42;
my $x = eval { die { code=>5 } }; print ref($@), $@->{code}, defined $x ? 1:0, "\n";
