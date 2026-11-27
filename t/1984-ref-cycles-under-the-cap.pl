# env: CURLY_GC_STRESS=0 CURLY_GC_POISON=0 CURLY_HEAP_CAP=8388608
# Two hundred thousand hashes that each hold themselves, and as many pairs
# of arrays that hold each other, dropped as they are made, under a cap of
# 8 MB (D65, D26): the program ends only if a cycle nothing reaches is
# freed. perl, with reference counts, keeps them all, and has the memory.
use v5.42;
my $kept = 0;
for my $i (1 .. 200000) {
    my $c = {n => $i};
    $c->{self} = $c;
    my $p = [$i];
    my $q = [$p];
    $p->[1] = $q;
    $kept = $c->{self}{n} + $q->[0][1][0][0] - $i;
}
say $kept;
