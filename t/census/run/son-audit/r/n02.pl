use v5.42;
my %h=(a=>1); my %c=%h; %h=(); print scalar(keys %c),"\n";
