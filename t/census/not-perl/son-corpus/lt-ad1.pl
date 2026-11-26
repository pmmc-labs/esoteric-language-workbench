use v5.42;
my %h = (n => [1]); print scalar(@{ $h{z} }), "|", scalar(@{ $h{n} }), "\n";
