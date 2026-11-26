use v5.42;
$_ = "t"; for (1..2) { } print "$_\n"; { local $_ = "u"; print } print "$_\n";
