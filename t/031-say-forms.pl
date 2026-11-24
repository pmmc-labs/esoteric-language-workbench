# The ways to write say's argument, and tokens hard against each other.
# With one blank before its bracket, say must end on the same line (T76).
use v5.42;
say(1 + 2);
say (1 + 2);
say (1 + 2) ;
say ((1 + 2) * 3);  # one blank, and the bracket and semicolon on the line
say((1 + 2) * 3);
say +(1 + 2) * 3;
say -(1 + 2) * 3;
say 3 * (1 + 2);
say +(1 + 2)
    * 3;
say
(1 + 2)
;
say  (1 +
      2);
say(
    1   # one
    +
    2   # and two
)
;
say 1 +
    2;
say 1
    - 2;
say 7 %+3;
say 7 %-3;
say 7 %(3);
say 2 *-3;
say 2 *(3);
say 1 -(2);
say 1 -2;
say 1+2;say(3);say (4);
