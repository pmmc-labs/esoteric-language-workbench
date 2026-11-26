use v5.42;
my @a=("ab"); sub t { $a[0] =~ tr/a/z/ } my @c=@a; t(); print "@c@a\n";
