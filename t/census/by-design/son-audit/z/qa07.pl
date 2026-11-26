use v5.42;
my @a=(1,2); sub f { my @l=@_; @a=(); "@l" } print f(@a), "\n";
