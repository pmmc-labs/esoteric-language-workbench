use v5.42;
my %h=(a=>1); my $v = delete($h{a}) . (exists $h{a} ? "y":"n"); print "$v\n";
