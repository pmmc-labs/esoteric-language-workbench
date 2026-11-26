use v5.42;
my $code = sub { return "c[@_]" };
print $code->(1, 2), "\n";
print $code->(), "\n";
