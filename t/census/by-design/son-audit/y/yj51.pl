use v5.42;
$_ = "top"; sub f { $_ = "f" } sub g { local $_ = "g"; h() } sub h { $_ } print g(), $_; f(); print "$_\n";
