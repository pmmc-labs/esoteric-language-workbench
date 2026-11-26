use v5.42;
my %h; my $n = defined $h{a}{b} ? 1 : 0; print scalar(keys %h), "\n";
