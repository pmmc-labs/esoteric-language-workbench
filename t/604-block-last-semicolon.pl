# kind: refused
# perl takes the last statement of a block without its semicolon.
# Every statement ends with one here.
use v5.42;
if (1) {
    say 1
}
