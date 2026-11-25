# kind: refused
# perl takes it: last and next are expressions to it (T120, D62).
use v5.42;
my $i = 0;
my $n = 0;
while ($i++ < 3) {
    $n = $i == 2 ? last : $i;
}
