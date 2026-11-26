use v5.42;
my %h=(a=>1); delete $h{a}; print((%h ? "t" : "f"), "\n");
