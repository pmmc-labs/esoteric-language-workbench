use v5.42;
my $anon = sub :prototype($) { $_[0] * 2 };
print $anon->(21), "\n";
