use v5.42;
my %h=(a=>1); my @b=(values %h, $h{a}=9); print "@b\n";
