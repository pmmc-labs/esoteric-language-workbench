use v5.42;
"ab"=~/(a)/; for my $s ("xy") { $s=~/(y)/; } print "$1\n";
