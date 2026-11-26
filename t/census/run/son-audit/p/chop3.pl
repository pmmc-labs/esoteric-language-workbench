use v5.42;
my %h = (k => "v\n"); chomp $h{k}; print "[$h{k}]\n";
