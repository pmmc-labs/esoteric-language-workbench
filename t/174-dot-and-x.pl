# The dot and x, by where they stand (D44, T90): after a value a dot
# joins, whatever follows it, and x repeats; where a value is wanted a dot
# begins a number.
use v5.42;
say "a".5;
say "a" .5;
say "a". 5;
say 1 .5;
say 1 . .5;
say .5 . .5;
say "a" . -1;
say "a" . - 1;
say "a" . +1;
say 1 . 2 . 3;
say "a" . "b" . "c";
say 1 + 2 . 3;
say 1 . 2 + 3;
say 1 . 2 * 3;
say "1" . 1 + 2 . "b";
say 2 ** 3 . 1;
say -2 . 1;
say "a"x 3;
say "a" x 3;
say "a" x(3);
say "a" x (3);
say "a" x"2";
say "a" x "2";
say 2 x 3;
say 1.5 x 2;
say "a" x 2 x 3;
say "ab" x 2 . "c";
say "a" . "b" x 2;
say 2 * 3 x 2;
say 2 x 3 * 2;
say 2 + 3 x 2;
say 2 x 3 + 2;
say "1" x 1 + 1;
say "5" x 2 + 1;
say -"2" x 2;
say - "2" x 2;
say -2 x 2;
say 2 x 2 ** 2;
say "a" x 2.7;
say "a" x .5 . "|";
say "x" x 3;
say 'x' x 3 . 'x';
say "x" . "x" x 2;
say "a"
    . "b"
    x 2;
