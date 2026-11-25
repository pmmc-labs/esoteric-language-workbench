# env: CURLY_GC_STRESS=0 CURLY_GC_POISON=0 CURLY_HEAP_CAP=16777216
# A gigabyte of strings in variables declared in a loop's block: each is
# gone when the block is entered again.
use v5.42;
my $count = 0;
for (my $i = 0; $i < 500000; $i++) {
    my $t = "c" x 1000;
    my $u = $t . $i;
    {
        my $v = $u . "!";
        $count += length $v;
    }
}
say $count;
