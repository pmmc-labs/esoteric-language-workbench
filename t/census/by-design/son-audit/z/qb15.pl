use v5.42;
$_=1; for my $v ($_) { local $_=5; print $v } print "\n";
