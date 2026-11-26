use v5.42;
our @a=(1,2); sub f { local @a=(7,8); $_[0] } print f($a[0]),"\n";
