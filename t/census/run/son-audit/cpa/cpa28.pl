use v5.42;
my %h=(a=>1); sub g { my %c=%h; $c{a}++; $c{a} } print g(), g(), $h{a}, "\n";
