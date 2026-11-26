use v5.42;
my %h=(a=>1); sub f { "@_" } print f($h{a}, $h{a}++), "\n";
