use v5.42;
"ab"=~/(a)/; my $x=$1; "ab"=~/(b)/; print "$x$1\n";
