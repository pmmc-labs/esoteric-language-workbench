# kind: refused
# perl takes it.
use v5.42;
my $i = 0;
while ($i++ < 3) {
    next while 0;
}
