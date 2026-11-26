use v5.42;
our %h=(a=>1); our %c=%h; $c{a}=2; print "$h{a}\n";
