# kind: refused
# perl prints 1: a dereference in a heredoc waits for step 13d.
use v5.42;
my $r = [1];
print <<"END";
$r->[0]
END
