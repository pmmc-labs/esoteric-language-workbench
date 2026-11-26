use v5.42;
my $x;
my $r = eval { field $x; 1 };
print defined $r ? "ran" : "died", "\n";
