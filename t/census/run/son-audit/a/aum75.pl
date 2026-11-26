use v5.42;
my %h; my $x = $h{a}{b} // 0; print scalar(keys %h), "\n";
