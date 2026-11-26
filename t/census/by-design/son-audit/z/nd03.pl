use v5.42;
my %h; $h{$_ % 2} .= $_ for 1..4; print "$h{0}$h{1}\n";
