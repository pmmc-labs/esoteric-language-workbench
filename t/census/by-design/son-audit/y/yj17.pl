use v5.42;
print get(), "\n"; my $n = 3; sub get { defined $n ? $n : "undef" }
