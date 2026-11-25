# env: CURLY_GC_STRESS=0 CURLY_GC_POISON=0 CURLY_HEAP_CAP=16777216
# A gigabyte of strings, each put in the same variable in its turn: the one
# before is garbage as soon as the next is assigned.
use v5.42;
my $s = "";
for (my $i = 0; $i < 1000000; $i++) {
    $s = ("ab" x 500) . $i;
}
say length $s;
say substr($s, 995);
