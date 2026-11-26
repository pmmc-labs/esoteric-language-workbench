use v5.42;
my $h = { a => 1 }; my $v = $h->{b}{c}; print exists $h->{b} ? "viv" : "none", "\n";
