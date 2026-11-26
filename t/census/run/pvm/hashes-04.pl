use v5.42;
my %h = (a => 1, b => 2);
print exists $h{a}, "\n";
print exists $h{z}, "\n";
my $gone = delete $h{a};
print $gone, "\n";
print scalar(keys %h), "\n";
