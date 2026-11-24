# `**` binds tighter than a minus sign before it and groups from the right;
# its own right operand may begin with a sign. `/` sits with `*` and `%`.
use v5.42;
say -2 ** 2;
say 2 ** 3 ** 2;
say 2 ** -1;
say 2 ** - 1;
say 2 ** +2;
say 2 ** -2 ** 2;
say - 2 ** - 2;
say((-2) ** 2);
say -2 ** -2 ** -2;
say 2 * 3 ** 2;
say 2 ** 3 * 2;
say 2 ** 0.5 ** 2;
say 4 / 2 * 3;
say 4 * 2 / 3;
say 7 / 2 % 2;
say 7 % 4 / 2;
say 1 / 3 * 3;
say 1 - 2 / 4;
say 6 / 4;
say 2 / 3 / 4;
say -6 / -4;
say 2
    **
    3;
