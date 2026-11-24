# Precedence and associativity, as perlop has them: unary minus and plus
# bind tighter than * and %, which bind tighter than + and -, and each of
# those two levels groups from the left.
use v5.42;
say 2 - 3 - 4;
say 2 + 3 * 4;
say -2 * -3;
say 2 * (3 + 4);
say 7 % 3 * 2;
say 2 * 7 % 3;
say 10 - 7 % 3;
say - 7 % 3;
say -(7 % 3);
say 3 - -3 * -3 % -2;
say 2 + -3 % 2 * 5 - 1;
say 1 - - 2;
say 1 + + + 2;
say 1 - - - 2;
say - -5;
say +-+-5;
say -(-(-(1)));
say +5;
say -0;
say 1+-2;
say 1-+2;
