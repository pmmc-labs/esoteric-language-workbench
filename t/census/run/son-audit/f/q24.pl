use v5.42;
"ab"=~/(a)/; my $c=0; if ($c) { "xy"=~/(y)/ } else { "pq"=~/(q)/ } print "$1\n";
