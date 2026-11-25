# kind: refused
# To perl a bare block is a loop that runs once: this last leaves the
# inner braces, and perl prints here three times (T32, D59).
use v5.42;
my $i = 0;
while ($i++ < 3) {
    {
        last;
    }
    say "here";
}
