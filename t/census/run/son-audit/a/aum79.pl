use v5.42;
my %h; my $n = exists $h{a} && $h{a}{b}; print scalar(keys %h), "\n";
