use v5.42;
my @a=(1,2,3); @a=grep { $_!=2 } @a; print "@a\n";
