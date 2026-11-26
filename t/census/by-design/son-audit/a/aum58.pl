use v5.42;
for my $s ("a") { local $_ = $s; sub up { $_ = uc } up(); print "$_\n" }
