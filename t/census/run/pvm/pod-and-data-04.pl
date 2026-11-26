use v5.42;
my @lines = <DATA>;
print @lines;
__DATA__
sub not_compiled { $x <=> }
q{ unbalanced
