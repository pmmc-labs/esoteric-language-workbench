# kind: refused
# perl warns: Found = in conditional, should be == (T112, D53). Found
# by breaking the checker: no test had a for's test in it.
use v5.42;
my $i = 0;
for (; $i = 5; ) {
    last;
}
