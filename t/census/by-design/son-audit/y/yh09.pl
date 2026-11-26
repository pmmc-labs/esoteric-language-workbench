use v5.42;
sub c { wantarray ? 1 : 0 } my @a = ("s","l"); print $a[c()], @a[c()], "\n";
