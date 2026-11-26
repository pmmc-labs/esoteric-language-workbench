use v5.42;
our $s = "ab"; sub ch { $s =~ s/a/z/ } my $t = $s; ch(); print "$t $s\n";
