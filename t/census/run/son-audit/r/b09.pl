use v5.42;
my $r = eval { die { code => 7 } }; print $@->{code}, "\n";
