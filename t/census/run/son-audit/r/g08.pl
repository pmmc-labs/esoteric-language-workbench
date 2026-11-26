use v5.42;
our $g=1; sub f { $g=5; 1 } my $r=[$g, f(), $g]; print "@$r\n";
