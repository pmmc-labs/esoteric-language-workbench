use v5.42;
my @a=(1,2,3); sub inc { $_[0]++ } inc($a[-1]); print "@a\n";
