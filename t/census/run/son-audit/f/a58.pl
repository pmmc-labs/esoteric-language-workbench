use v5.42;
my @a=(3,1,2); @a=sort { $a<=>$b } @a; print "@a\n";
