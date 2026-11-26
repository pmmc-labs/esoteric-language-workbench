use v5.42;
sub f {} my %h; f(@h{qw(a b)}); print scalar(keys %h), "\n";
