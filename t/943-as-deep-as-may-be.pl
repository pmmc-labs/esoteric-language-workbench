# The limit on recursion (D68), from below. It is the implementation's and
# not the language's: the open frames may count for 4 MB, each 16 bytes a
# slot and 1 KB besides. The file's frame here is 2 slots, 1,056 bytes,
# and a call of depth is 6 slots, 1,120: so 3,743 calls of it may be open
# at once, which depth(3742) makes, and depth(3743) is one too many. A
# change to what the compiler keeps in a frame moves these two numbers,
# and nothing else.
use v5.42;
no warnings 'recursion';
sub depth($n) {
    return $n == 0 ? 0 : 1 + depth($n - 1);
}
say depth(3742);
