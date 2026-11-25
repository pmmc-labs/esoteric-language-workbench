use v5.42;
bump(); my $x += 10; say $x;
tag(); my $s .= "a"; say $s;
one(); my $d //= 10; say $d;
sub bump() { $x++ }
sub tag() { $s = "q" }
sub one() { $d = 1 }
