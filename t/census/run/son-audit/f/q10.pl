use v5.42;
"ab"=~/(a)/; eval { "xy"=~/(y)/; }; print "$1\n";
