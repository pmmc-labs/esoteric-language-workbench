# kind: refused
# next leaves a bare block too, as last does: perl prints 123 (T32, D59).
use v5.42;
my $i = 0;
while ($i++ < 3) {
    { next if $i == 2; }
    print $i;
}
print "\n";
