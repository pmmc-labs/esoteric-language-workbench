use v5.42;
my $s = caller;
my @l = caller;
my @one = $s;
print scalar @one, " ", scalar @l, "\n";
