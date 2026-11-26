use v5.42;
my %h=(a=>1); my %inv=reverse %h; $h{z}=2; print join(",", %inv), "\n";
