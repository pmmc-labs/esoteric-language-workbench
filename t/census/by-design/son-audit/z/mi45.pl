use v5.42;
my %h=(a=>1); print "v=$h{a} $h{'a'} @h{'a'} @{[ %h ]}\n";
