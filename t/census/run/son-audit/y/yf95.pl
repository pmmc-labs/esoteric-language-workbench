use v5.42;
my %h; $h{$_ % 2} .= $_ for 1..5; print join(",", map { "$_=$h{$_}" } sort keys %h), "\n";
