use v5.42;
my $x; BEGIN { $x = "begin" } print defined $x ? $x : "u", "\n";
