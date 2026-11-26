use v5.42;
my $slot = 0;
sub slot :lvalue { $slot }
slot() = 42;
print slot(), "\n";
my $anon = sub :prototype($) { $_[0] * 2 };
print $anon->(21), "\n";
