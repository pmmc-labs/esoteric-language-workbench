use v5.42;
my @a=(1,2,3); { local $"=":"; print "@a\n"; } print "@a\n";
