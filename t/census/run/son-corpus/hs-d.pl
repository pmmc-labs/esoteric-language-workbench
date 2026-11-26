use v5.42;
my %h = (a => 1); my $k = "zz"; $k = $k . ""; print $h{$k} // "u", "\n";
