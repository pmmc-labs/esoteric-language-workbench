# kind: refused
# With no loop at all, perl leaves the block and prints after (T32, D59).
use v5.42;
{
    last;
    say "not reached";
}
say "after";
