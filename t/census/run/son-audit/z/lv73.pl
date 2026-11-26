use v5.42;
my %h; my $k="a"; $h{$k .= "b"} = $k; print join(",", %h), "\n";
