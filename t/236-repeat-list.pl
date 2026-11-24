# kind: refused
# perl prints aaa, by repeating a list of one value three times: in say's list of
# arguments, brackets round the left of x make it a list (T101). Lists are step 9's.
use v5.42;
say(("a") x 3);
