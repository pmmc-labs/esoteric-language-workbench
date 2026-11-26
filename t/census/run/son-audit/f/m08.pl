use v5.42;
my $s="axx"; { local $/="x"; chomp $s; } print "$s\n";
