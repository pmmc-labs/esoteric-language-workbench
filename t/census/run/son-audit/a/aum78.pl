use v5.42;
my %h; my @l = @{ $h{l} // [] }; print scalar(keys %h), "\n";
