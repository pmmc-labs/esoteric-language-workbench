use v5.42;
my $x="hello"; (my $c = $x) =~ tr/a-y/b-z/; print "$x$c\n";
