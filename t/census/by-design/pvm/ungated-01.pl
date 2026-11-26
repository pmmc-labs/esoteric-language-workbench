use v5.42;
sub c { state $n = 0; $n = $n + 1; return $n }
my $r = eval { c() };
print defined $r ? "ran" : "died", "\n";
