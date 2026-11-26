use v5.42;
my $z=0; my $s = eval { 5 % $z }; print $@ =~ /zero/ ? "z":"n", "\n";
