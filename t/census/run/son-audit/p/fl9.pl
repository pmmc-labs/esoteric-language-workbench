use v5.42;
my @a = (1); my $i = 5; my $v = $a[$i] // "u"; print scalar(@a), " $v\n";
