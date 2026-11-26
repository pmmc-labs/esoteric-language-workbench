use v5.42;
my @a = (1,2); sub f { $_[0]++ } f($_) for @a; map { f($_) } @a; print "@a\n";
