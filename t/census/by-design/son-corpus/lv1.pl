use v5.42;
my $slot = 0;
sub slot :lvalue { $slot }
slot() = 42;
print slot(), "\n";
