# kind: refused
# perl prints 10 three times: the sub is tied to the first time round (T31).
use v5.42;
my $i = 0;
while ($i++ < 3) {
    my $n = $i * 10;
    sub get() { return $n; }
    say get();
}
